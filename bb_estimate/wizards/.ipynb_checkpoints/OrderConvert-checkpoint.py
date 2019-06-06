# -*- coding: utf-8 -*-

from odoo import models, fields, api

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
    
    RunOnQuantity = fields.Integer('Run on Quantity',readonly=True)
    RunOnPrice = fields.Float('Run on Price(GBP)',readonly=True)
    RunOnRequired = fields.Integer('Run on Quantity Required', required=True)
    
    ExtrasApplied = fields.Boolean('Extras Applied to the Estimate')
    HasExtra = fields.Boolean('Has Extra',compute="getEstimateExtra")
    
    @api.depends('EstimateId')
    def getEstimateExtra(self):
        for record in self:
            if record.EstimateId:
                record.HasExtra = record.EstimateId.hasExtra
                record.RunOnQuantity = record.EstimateId.run_on
                record.RunOnPrice = record.EstimateId.total_price_run_on
    
    @api.onchange('QuantityRequired','RunOnRequired')
    def changeQuanitity(self):
        ratio = 1.0
        for record in self:
            if record.EstimateId and record.EstimateId['run_on']:
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
        
        routing = self.env['mrp.routing'].sudo()
        bom = self.env['mrp.bom'].sudo()
        operation = self.env['mrp.routing.workcenter'].sudo()
        components = self.env['mrp.bom.line'].sudo()
        order = self.env['mrp.production'].sudo()
        
        #routes
        newRoute = {
            'name': 'route_%s'%(self.EstimateId.estimate_number),
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
                    'time_cycle_manual' : process['quantity_required_'+self.QuantityRequired],
                    'batch' : 'no',
                }
                operation.create(newOperation)
        
        #bom
        newBom = {
            'routing_id' : routeId.id,
            'active' : True,
            'code' : self.EstimateId.estimate_number,
            'product_tmpl_id' : self.EstimateId.product_type.product_tmpl_id.id,
            'product_qty' : self.EstimateId['quantity_'+self.QuantityRequired],
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
                    'product_qty' : material['quantity_required_'+self.QuantityRequired],
                    'routing_id' : routeId.id,
                    'bom_id' : bomId.id,
                }
                if material.material.uom_id:
                    newMaterial['product_uom_id'] = material.material.uom_id.id
                components.create(newMaterial)
        newOrder = {
            'name' : self.EstimateId.estimate_number,
            'origin' : 'Estimate Workflow',
            'bom_id' : bomId.id,
            'routing_id': routeId.id,
            'product_qty' : self.TotalQuantity,
            'product_tmpl_id' : self.EstimateId.product_type.product_tmpl_id.id,
            'product_id' : self.EstimateId.product_type.id,
            'product_uom_id':  self.EstimateId.product_type.uom_id.id
            
        }
        mo = order.create(newOrder)
        data = {}
        if mo:
            data['manufacturingOrder'] = mo.id
        if routeId:
            data['routings'] = routeId.id
        if bomId:
            data['bom'] = bomId.id
        self.EstimateId.write(data)
        