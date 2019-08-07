# -*- coding: utf-8 -*-
import odoo, math
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError
from odoo.tools import float_compare, float_round, float_is_zero

class ChangeLog(models.TransientModel):
    _name = 'bb_estimate.change_log'
    
    EstimateId = fields.Many2one('bb_estimate.estimate', string="Estimate")
    EstimateLineId =  fields.Many2one('bb_estimate.estimate_line', string="Estimate")
    product_id = fields.Many2one('product.product',related="EstimateLineId.material")
    workcenter_id = fields.Many2one('mrp.workcenter',related="EstimateLineId.workcenterId")
    AmmendId =  fields.Many2one('bb_estimate.wizard_amend_qty', string="Ammendement")
    LineName = fields.Char('Name',related="EstimateLineId.lineName")
    CurrentRequired = fields.Float('Old')
    NewRequired = fields.Float('New')
    POQty = fields.Integer('PO Qty')
    POComment = fields.Char('POs')
    
class AmmendQty(models.TransientModel):
    _name = "bb_estimate.wizard_amend_qty"
    
    EstimateId = fields.Many2one('bb_estimate.estimate', string="Estimate")
    ChangeLog = fields.One2many('bb_estimate.change_log','AmmendId','Lines')
    
    Quantity = fields.Integer('Selected Quantity', compute="_computeData")
    RunOn = fields.Integer('Selected Run On', compute="_computeData")
    TotalPrice = fields.Float('Total Price', compute="_computeData")
    
    AmmendedQty = fields.Integer('Quantity')
    AmmendedPrice = fields.Float('New Price', compute="_computeNewPrice")
    
    @api.onchange('EstimateId')
    def _setQty(self):
        if self.EstimateId:
            self.AmmendedQty = self.EstimateId['quantity_'+ self.EstimateId.selectedQuantity] * self.EstimateId.SelectedQtyRatio
            lines = []
            for x in self.EstimateId.estimate_line:
                data = {
                          'EstimateId': self.EstimateId.id,
                          'EstimateLineId': x.id,
                          'CurrentRequired': (x['quantity_required_%s'%(self.EstimateId.selectedQuantity)] * self.EstimateId.SelectedQtyRatio) + (x.quantity_required_run_on * self.EstimateId.selectedRatio),
                          'NewRequired' : x['quantity_required_%s'%(self.EstimateId.selectedQuantity)] + (x.quantity_required_run_on * self.EstimateId.selectedRatio),
                          'POQty' : 0
                      }
                if x.option_type == 'material':
                    data['CurrentRequired'] = math.ceil(data['CurrentRequired'])
                lines.append((0,0,data))
            self.ChangeLog = lines
    
    @api.depends('EstimateId')
    def _computeData(self):
        if self.EstimateId:
            self.Quantity = self.EstimateId['quantity_'+ self.EstimateId.selectedQuantity] * self.EstimateId.SelectedQtyRatio
            self.RunOn = self.EstimateId.selectedRunOn
            self.TotalPrice = (self.EstimateId['total_price_%s'%(self.EstimateId.selectedQuantity)] * self.EstimateId.SelectedQtyRatio) + (self.EstimateId.total_price_run_on * self.EstimateId.selectedRatio)
    
    @api.onchange('AmmendedQty','EstimateId')
    def _computeNewPrice(self):
        if self.EstimateId:
            ratio = self.AmmendedQty / (self.EstimateId['quantity_'+ self.EstimateId.selectedQuantity])
            self.AmmendedPrice = (self.EstimateId['total_price_%s'%(self.EstimateId.selectedQuantity)] * ratio) + (self.EstimateId.total_price_run_on * self.EstimateId.selectedRatio)
            if len(self.ChangeLog) > 0:
                for x in self.ChangeLog:
                    x.NewRequired = (x.EstimateLineId['quantity_required_%s'%(self.EstimateId.selectedQuantity)] * ratio) + (x.EstimateLineId.quantity_required_run_on * self.EstimateId.selectedRatio)
                    if x.product_id:
                        x.NewRequired = math.ceil(x.NewRequired)
                    if x.EstimateLineId.generatesPO:
                        diff = x.NewRequired - x.CurrentRequired
                        if diff > 0:
                            multiplier = x.EstimateLineId.param_material_vendor.multiplier if x.EstimateLineId.param_material_vendor.multiplier > 0 else 1
                            qty = (math.ceil(diff / multiplier) * multiplier)
                            qty = qty if qty > x.EstimateLineId.param_material_vendor.minQuantity else x.EstimateLineId.param_material_vendor.minQuantity
                            x.POQty = qty
                            if self.EstimateId.manufacturingOrder:
                                Open = sum([a.product_qty for a in filter(lambda q: (q.order_id.state not in ['purchase','done','cancel']) and (q.product_id.id == x.product_id.id) ,self.EstimateId.manufacturingOrder.Purchases.mapped('order_line'))])
                                Closed = sum([a.product_qty for a in filter(lambda q: (q.order_id.state in ['purchase','done','cancel']) and (q.product_id.id == x.product_id.id) ,self.EstimateId.manufacturingOrder.Purchases.mapped('order_line'))])
                                x.POComment = 'Open PO:%s, Closed PO: %s'%(Open,Closed)
                        else:
                            x.POQty = 0
                            
                        

    def Confirm(self):
        if self.EstimateId:
            ratio = self.AmmendedQty / (self.EstimateId['quantity_'+ self.EstimateId.selectedQuantity])
            mo = self.EstimateId.manufacturingOrder
            so = self.EstimateId.salesOrder
            bom = self.EstimateId.bom
            routings = self.EstimateId.routings
            self.update_mo(mo,ratio)
            self.update_so(so)
            self.EstimateId.write({'SelectedQtyRatio': ratio})
            
            values = {
                'production_order': mo,
                'sales_order': so,
                'data': self,
            }
            body = self.env.ref('bb_estimate.qty_amend').render(values=values)
            self.EstimateId.message_post(body=body)
            
   
    def update_so(self,so):
        if so.order_line:
            record = so.order_line[0]
            otherSum = sum([x.price_subtotal for x in so.order_line if x.id != record.id])
            price = (self.AmmendedPrice - otherSum)
            current = so.amount_untaxed 
            
            record.write(
                {
                    'price_unit': (price / self.AmmendedQty)
                }
            )
    
    @api.model
    def _update_product_to_produce(self, production, qty, old_qty):
        production_move = production.move_finished_ids.filtered(lambda x: x.product_id.id == production.product_id.id and x.state not in ('done', 'cancel'))
        if production_move:
            production_move.write({'product_uom_qty': qty})
        else:
            production_move = production._generate_finished_moves()
            production_move = production.move_finished_ids.filtered(lambda x: x.state not in ('done', 'cancel') and production.product_id.id == x.product_id.id)
            production_move.write({'product_uom_qty': qty})
        return {production_move: (qty, old_qty)}

    @api.multi
    def update_mo(self,production,ratio):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        produced = sum(production.move_finished_ids.filtered(lambda m: m.product_id == production.product_id).mapped('quantity_done'))
        
        if (self.AmmendedQty + self.RunOn) < produced:
            format_qty = '%.{precision}f'.format(precision=precision)
            raise UserError(_("You have already processed %s. Please input a quantity higher than %s ") % (format_qty % produced, format_qty % produced))
        
        old_production_qty = production.product_qty
        production.write({'product_qty': self.AmmendedQty + self.RunOn})
        done_moves = production.move_finished_ids.filtered(lambda x: x.state == 'done' and x.product_id == production.product_id)
        qty_produced = production.product_id.uom_id._compute_quantity(sum(done_moves.mapped('product_qty')), production.product_uom_id)
        factor = production.product_uom_id._compute_quantity(production.product_qty - qty_produced, production.bom_id.product_uom_id) / production.bom_id.product_qty
        materials, process = ({x.EstimateLineId.id:x for x in self.ChangeLog if (x.product_id and x.EstimateLineId.option_type == 'material')},{x.EstimateLineId.id:x for x in self.ChangeLog if (x.workcenter_id and x.EstimateLineId.option_type == 'process')})
        computed = []
        if production.bom_id:
            production.bom_id.write({'product_qty': (self.AmmendedQty + self.RunOn)})
            for bom_line in production.bom_id.bom_line_ids:
                line = self.ChangeLog.search([('EstimateLineId.estimate_id','=',self.EstimateId.id),('product_id','=',bom_line.product_id.id),('EstimateLineId.option_type','=','material'),('EstimateLineId.id','not in', computed)],limit=1)
                bom_line.write({'product_qty':materials[line.EstimateLineId.id].NewRequired})
                computed.append(line.EstimateLineId.id)
                
        
        computed = []
        if production.routing_id:
            for route in production.routing_id.operation_ids:
                line = self.ChangeLog.search([('EstimateLineId.estimate_id','=',self.EstimateId.id),('workcenter_id','=',route.workcenter_id.id),('EstimateLineId.option_type','=','process'),('EstimateLineId.id','not in', computed)],limit=1)
                route.write({'time_cycle_manual':process[line.EstimateLineId.id].NewRequired})
                computed.append(line.EstimateLineId.id)
        
        boms, lines = production.bom_id.explode(production.product_id, factor, picking_type=production.bom_id.picking_type_id)
        
        documents = {}
        for line, line_data in lines:
            move = production.move_raw_ids.filtered(lambda x: x.bom_line_id.id == line.id and x.state not in ('done', 'cancel'))
            if move:
                line_data['qty'] = line.product_qty
                move = move[0]
                old_qty = move.product_uom_qty
                #values = move._prepare_procurement_values()
                #origin = (move.group_id and move.group_id.name or (move.origin or move.picking_id.name or "/"))
                #self.env['procurement.group'].run(move.product_id, move.product_uom_qty, move.product_uom, move.location_id, move.rule_id and move.rule_id.name or "/", origin, values)
            else:
                old_qty = 0
            iterate_key = production._get_document_iterate_key(move)
            if iterate_key:
                document = self.env['stock.picking']._log_activity_get_documents({move: (line_data['qty'], old_qty)}, iterate_key, 'UP')
                for key, value in document.items():
                    if documents.get(key):
                        documents[key] += [value]
                    else:
                        documents[key] = [value]
            production._update_raw_move(line, line_data)
        
        computed = []
        
        for key in documents.keys():
            for x in documents[key]:
                for line in x[0].keys():
                    move = x[0][line][0]
                    qtys = x[0][line][1]
                    
                    log = [x for x in filter(lambda x: (move.product_id.id == x.product_id.id) and (x.EstimateLineId.option_type == 'material') and (x.EstimateLineId.id not in computed), self.ChangeLog)]
                    if len(log) > 0:
                        log = log[0]
                        if log.POQty > 0:
                            computed.append(log.EstimateLineId.id)
                            values = move._prepare_procurement_values()
                            origin = (move.group_id and move.group_id.name or (move.origin or move.picking_id.name or "/"))
                            self.env['procurement.group'].run(move.product_id, log.POQty, move.product_uom, move.location_id, move.rule_id and move.rule_id.name or "/", origin, values)
        
        #production._log_manufacture_exception(documents)
        operation_bom_qty = {}
        
        for bom, bom_data in boms:
            for operation in bom.routing_id.operation_ids:
                operation_bom_qty[operation.id] = bom_data['qty']
        
        finished_moves_modification = self._update_product_to_produce(production, production.product_qty - qty_produced, old_production_qty)
        production._log_downside_manufactured_quantity(finished_moves_modification)
        moves = production.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
        moves._action_assign()
        
        for wo in production.workorder_ids:
            operation = wo.operation_id
            if operation_bom_qty.get(operation.id):
                wo.duration_expected = operation.time_cycle_manual
            quantity = wo.qty_production - wo.qty_produced
            
            if production.product_id.tracking == 'serial':
                quantity = 1.0 if not float_is_zero(quantity, precision_digits=precision) else 0.0
            else:
                quantity = quantity if (quantity > 0) else 0
            
            if float_is_zero(quantity, precision_digits=precision):
                wo.final_lot_id = False
                wo.active_move_line_ids.unlink()
            wo.qty_producing = quantity
            
            if wo.qty_produced < wo.qty_production and wo.state == 'done':
                wo.state = 'progress'
            
            if wo.qty_produced == wo.qty_production and wo.state == 'progress':
                wo.state = 'done'
            
            # assign moves; last operation receive all unassigned moves
            # TODO: following could be put in a function as it is similar as code in _workorders_create
            # TODO: only needed when creating new moves
            
            moves_raw = production.move_raw_ids.filtered(lambda move: move.operation_id == operation and move.state not in ('done', 'cancel'))
            
            if wo == production.workorder_ids[-1]:
                moves_raw |= production.move_raw_ids.filtered(lambda move: not move.operation_id)
            moves_finished = production.move_finished_ids.filtered(lambda move: move.operation_id == operation) #TODO: code does nothing, unless maybe by_products?
            moves_raw.mapped('move_line_ids').write({'workorder_id': wo.id})
            (moves_finished + moves_raw).write({'workorder_id': wo.id})
            if quantity > 0 and wo.move_raw_ids.filtered(lambda x: x.product_id.tracking != 'none') and not wo.active_move_line_ids:
                wo._generate_lot_ids()
        return {}
            