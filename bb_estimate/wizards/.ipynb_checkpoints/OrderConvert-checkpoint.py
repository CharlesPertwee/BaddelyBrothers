# -*- coding: utf-8 -*-
import odoo
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError

class OrderConvert(models.TransientModel):
    _name = "bb_estimate.wizard_order_convert"
    
    def GetQuantities(self):
        if 'default_EstimateId' in self._context.keys():
            estimate = self.env['bb_estimate.estimate'].browse(self._context['default_EstimateId'])
            if estimate:
                values = [(str(x),'Quantity: %d, Price: %.2f'%(estimate['quantity_'+str(x)],estimate['total_price_'+str(x)])) for x in range(1,5) if estimate['quantity_'+str(x)] > 0]
                return values
        
    EstimateId = fields.Many2one('bb_estimate.estimate', string="Estimate")
    QuantityRequired = fields.Selection(GetQuantities,string='Quantity Required', required=True)
    
    TotalQuantity = fields.Integer('Total Quantity',compute="changeQuanitity")
    TotalPrice = fields.Float('Total Price',compute="changeQuanitity")
    
    RunOnQuantity = fields.Integer('Run on Quantity',related="EstimateId.run_on")
    RunOnPrice = fields.Float('Run on Price(GBP)',related="EstimateId.total_price_run_on")
    RunOnRequired = fields.Integer('Run on Quantity Required', required=True)
    
    ExtrasApplied = fields.Boolean('Extras Applied to the Estimate')
    HasExtra = fields.Boolean('Has Extra',related="EstimateId.hasExtra")
    
    @api.depends('EstimateId')
    def getEstimateExtra(self):
        for record in self:
            if record.HasExtra:
                raise ValidationError("This order contains Extra's. If you want to remove them then, this is the moment.")
                
    @api.onchange('QuantityRequired','RunOnRequired')
    def changeQuanitity(self):
        ratio = 0.0
        for record in self:
            if record.EstimateId and record.EstimateId['run_on'] > 0:
                ratio = record.RunOnRequired / record.EstimateId['run_on']
                
            if record.QuantityRequired:
                record.TotalQuantity = record.EstimateId['quantity_'+record.QuantityRequired] + record.RunOnRequired
                record.TotalPrice = record.EstimateId['total_price_'+record.QuantityRequired] + (record.RunOnPrice * ratio)
            elif record.RunOnRequired:
                record.TotalQuantity = record.RunOnRequired
                record.TotalPrice = record.RunOnPrice + (record.RunOnPrice * ratio)
            
    def CreateOrder(self):
        processes = self.EstimateId.estimate_line.search([('estimate_id','=',self.EstimateId.id),('option_type','=','process')])
        materials = self.EstimateId.estimate_line.search([('estimate_id','=',self.EstimateId.id),('option_type','=','material')])
        
        runOnRatio = 0.0
        
        if self.RunOnRequired > 0 and self.EstimateId['run_on'] > 0:
            runOnRatio = (self.RunOnRequired / self.EstimateId['run_on'])
        
        totalPrice = self.TotalPrice #+ (self.RunOnPrice * runOnRatio)
        
        routing = self.env['mrp.routing'].sudo()
        bom = self.env['mrp.bom'].sudo()
        operation = self.env['mrp.routing.workcenter'].sudo()
        components = self.env['mrp.bom.line'].sudo()
        order = self.env['mrp.production'].sudo()
        sales = self.env['sale.order'].sudo()

        #routes
        newRoute = {
            'name': 'Route_%s'%(self.EstimateId.estimate_number),
            'active': True,
            'code' : self.EstimateId.estimate_number,
        }
        
        routeId = routing.create(newRoute)
        if routeId:
            for process in processes:
                newOperation = {
                    'name' : '%s_%s'%(process.estimate_id.estimate_number,process.lineName),
                    'workcenter_id': process.workcenterId.id,
                    'sequence' : process.Sequence,
                    'routing_id' : routeId.id,
                    'time_mode' : 'manual',
                    'time_cycle_manual' : (process['quantity_required_'+self.QuantityRequired] + (process['quantity_required_run_on'] * runOnRatio)),
                    'batch' : 'no',
                    'EstimateLineId' : process.id
                }
                operation.create(newOperation)
        
        #bom
        newBom = {
            'routing_id' : routeId.id,
            'active' : True,
            'code' : self.EstimateId.estimate_number,
            'product_tmpl_id' : self.EstimateId.product_type.product_tmpl_id.id,
            'product_qty' : self.TotalQuantity,#self.EstimateId['quantity_'+self.QuantityRequired],
            'ready_to_produce' : 'all_available',
        }
        
        if self.EstimateId.product_type.uom_id:
            newBom['product_uom_id'] = self.EstimateId.product_type.uom_id.id
        
        bomId = bom.create(newBom)
        
        if bomId:
            for material in materials:
                newMaterial = {
                    'sequence': material.Sequence,
                    'product_id':material.material.id,
                    'product_qty' : material['quantity_required_'+self.QuantityRequired] + (material['quantity_required_run_on'] * runOnRatio),
                    'routing_id' : routeId.id,
                    'bom_id' : bomId.id,
                    'EstimateLineId': material.id
                }
                if material.material.uom_id:
                    newMaterial['product_uom_id'] = material.material.uom_id.id
                components.create(newMaterial)

        newOrder = {
            'name' : self.env['ir.sequence'].next_by_code('bb_estimate.jobticket'),
            'origin' : self.EstimateId.estimate_number,#'Estimate Workflow',
            'bom_id' : bomId.id,
            'routing_id': routeId.id,
            'product_qty' : self.TotalQuantity,
            'product_tmpl_id' : self.EstimateId.product_type.product_tmpl_id.id,
            'product_id' : self.EstimateId.product_type.id,
            'product_uom_id':  self.EstimateId.product_type.uom_id.id,
            'Estimate' : self.EstimateId.id
        }
        
        mo = order.create(newOrder)
        
        data = {
            'selectedQuantity': self.QuantityRequired,
            'selectedRunOn': self.RunOnRequired,
            'selectedPrice': totalPrice,
            'selectedRatio' : runOnRatio
        }
        
        if mo:
            data['manufacturingOrder'] = mo.id
            data['isLocked'] = True
        if routeId:
            data['routings'] = routeId.id
        if bomId:
            data['bom'] = bomId.id
        
        
        #Sales Order
        salesProduct = {
            'product_id': self.EstimateId.product_type.id,
            'product_uom_qty': self.TotalQuantity,
            'price_unit': totalPrice/self.TotalQuantity,

        }
        newSales = {
            'partner_id': self.EstimateId.partner_id.id,
            'partner_invoice_id': self.EstimateId.invoice_account.id,
            'partner_shipping_id': self.EstimateId.Delivery.id,
            'amount_untaxed': totalPrice,
            #'carrier_id': self.EstimateId.DeliveryMethod.id,
            'Estimate' : self.EstimateId.id,
            'JobTicket': mo.id,
            'user_id': self.EstimateId.estimator.id,
            'order_line':[(0,0,salesProduct)]
        }

        salesId = sales.create(newSales)
        if salesId:
            salesId.action_confirm()
            data['salesOrder'] = salesId.id
            
        self.EstimateId.write(data)