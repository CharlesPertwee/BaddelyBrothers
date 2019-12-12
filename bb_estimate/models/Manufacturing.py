# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round
    
class Manufacture(models.Model):
    _inherit = 'mrp.production'
    
    def GetOptions(self,key):
        values = [(x.value,x.value) for x in self.env['bb_estimate.specification'].search([('name','=',key)])]
        return values
    
    def GetSpecs(self):
        return self.GetOptions('Specification')
    def GetJob(self):
        return self.GetOptions('JobType')
    def GetDie(self):
        return self.GetOptions('Die')
    
    Project = fields.Many2one('project.project','Project')
    
    Estimate = fields.Many2one('bb_estimate.estimate','Originating Estimate',ondelete='restrict')
    NoOfCopiesRequired = fields.Char('No. File Copies Reqd', size=5)
    NoOfCustomerCopies = fields.Char('Customer Files', size=5)
    OversRequired = fields.Char('No. Overs Reqd', size=5)
    ChargeOvers = fields.Boolean('Charge for Overs')
    
    SpecifcationType = fields.Selection(GetSpecs,string="Spec Type")
    JobType = fields.Selection(GetJob,string="Job Type")
    DieType = fields.Selection(GetDie,string="Return Die / Block To :")
    
    customerRef = fields.Char('Customer Reference')
    previousJobRef = fields.Char('Previous Job Ticket')
    Purchases = fields.Many2many('purchase.order',string='Purchase')  
    analytic_account = fields.Many2one('account.analytic.account','Analytic Account')  
    
    def write(self,vals):
        if 'customerRef' in vals.keys():
            if self.Estimate:
                sale_order = self.Estimate.salesOrder
                delivery = self.env['stock.picking'].sudo().search([('origin','=',sale_order.name)])
                sale_order.write({'client_order_ref':vals['customerRef']})
                delivery.write({'customerRef':vals['customerRef']})
                
        return super(Manufacture,self).write(vals)
    

        
  
    def ConfirmOrder(self):
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'name': 'Confirm',
                'res_model' : 'bb_estimate.confirm_mo',
                'type' : 'ir.actions.act_window',
                'context' : "{'default_ProductionId' : active_id}",
                'target' : 'new',
            }
    
    def _workorders_create(self, bom, bom_data):
        """
        :param bom: in case of recursive boms: we could create work orders for child
                    BoMs
        """
        workorders = self.env['mrp.workorder']
        bom_qty = bom_data['qty']
        
        estimate = self.env['bb_estimate.estimate'].sudo().search([('estimate_number','=',bom.code)])
        if estimate:
            estimate = estimate[0]
            
        # Initial qty producing
        if self.product_id.tracking == 'serial':
            quantity = 1.0
        else:
            quantity = self.product_qty - sum(self.move_finished_ids.mapped('quantity_done'))
            quantity = quantity if (quantity > 0) else 0
        
        computedOperations = []
        materials = []
            
        if estimate:
            estimate_materials = estimate.estimate_line.search([('estimate_id','=',estimate.id),('option_type','=','material'),('isExtra','=',False)])
            for x in estimate_materials:
                materials.append((0,0,{
                    'EstimateLineId': x.id,
                    'MaterialAllocated' : (x['quantity_required_'+estimate.selectedQuantity] * estimate.SelectedQtyRatio) + (x.quantity_required_run_on * estimate.selectedRatio)
                }))
        for operation in bom.routing_id.operation_ids:
            # create workorder
            cycle_number = float_round(bom_qty / operation.workcenter_id.capacity, precision_digits=0, rounding_method='UP')
            if estimate:
                estimate_line = estimate.estimate_line.search([('estimate_id','=',estimate.id),('isExtra','=',False),('option_type','=','process'),('workcenterId','=',operation.workcenter_id.id),('id','not in',computedOperations)])
                if estimate_line:
                    estimate_line = estimate_line[0]
                computedOperations.append(estimate_line.id)
                duration_expected = (estimate_line['quantity_required_'+estimate.selectedQuantity] * estimate.SelectedQtyRatio) + (estimate_line.quantity_required_run_on * estimate.selectedRatio)
            else:
                duration_expected = (operation.workcenter_id.time_start +
                                 operation.workcenter_id.time_stop +
                                 cycle_number * operation.time_cycle * 100.0 / operation.workcenter_id.time_efficiency)
            
            
            newWorkOrder ={
                'name': operation.name,
                'production_id': self.id,
                'workcenter_id': operation.workcenter_id.id,
                'operation_id': operation.id,
                'duration_expected': duration_expected,
                'state': len(workorders) == 0 and 'ready' or 'pending',
                'qty_producing': quantity,
                'capacity': operation.workcenter_id.capacity,
                'ActualTime' : duration_expected
            }
            if len(materials) > 0:
                newWorkOrder['EstimateMaterials'] = materials
            workorder = workorders.create(newWorkOrder)
            if workorders:
                workorders[-1].next_work_order_id = workorder.id
            workorders += workorder

            # assign moves; last operation receive all unassigned moves (which case ?)
            moves_raw = self.move_raw_ids.filtered(lambda move: move.operation_id == operation)
            if len(workorders) == len(bom.routing_id.operation_ids):
                moves_raw |= self.move_raw_ids.filtered(lambda move: not move.operation_id)
            moves_finished = self.move_finished_ids.filtered(lambda move: move.operation_id == operation) #TODO: code does nothing, unless maybe by_products?
            moves_raw.mapped('move_line_ids').write({'workorder_id': workorder.id})
            (moves_finished + moves_raw).write({'workorder_id': workorder.id})

            workorder._generate_lot_ids()
            
        #Hide the Ammend Qty Button from Estimate, If estimate is present.
        if estimate:
            estimate.write({'AppendLog':True})
        return workorders
