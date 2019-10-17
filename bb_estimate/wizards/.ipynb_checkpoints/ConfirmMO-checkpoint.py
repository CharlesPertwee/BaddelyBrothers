# -*- coding: utf-8 -*-
import odoo
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError

class ConfirmationLines(models.TransientModel):
    _name = 'bb_estimate.confirm_lines'
    
    WorkOrder = fields.Many2one('mrp.workorder',string='Work Order')
    Material = fields.Many2one('stock.move',string='Material')
    Confirmation = fields.Many2one('bb_estimate.confirm_mo',string="Confirmation")
    name = fields.Char('Name',compute="_computeName")
    
    EstimatedTime = fields.Float('Estimated Time (Hrs)',related="WorkOrder.duration_expected")
    ActualTime = fields.Float('Actual Time (Hrs)')
    
    EstimateMaterial = fields.Float('Estimated Material',related="Material.product_uom_qty")
    ActualMaterial = fields.Integer('Actual Material')
    
    def _computeName(self):
        for record in self:
            if record.Material:
                record.name = record.Material.product_id.name
            if record.WorkOrder:
                record.name = record.WorkOrder.name

class ConfirmMo(models.TransientModel):
    _name = 'bb_estimate.confirm_mo'
    
    ProductionId = fields.Many2one('mrp.production')
    MaterialLines = fields.One2many('bb_estimate.confirm_lines','Confirmation','Lines')
    WorkOrders = fields.One2many('bb_estimate.confirm_lines','Confirmation','Lines')
    
    @api.onchange('ProductionId')
    def _computeLines(self):
        for record in self:
            if record.ProductionId:
                materials = []
                for x in record.ProductionId.move_raw_ids:
                    materials.append((0,0,
                                      {
                                          'Material' : x,
                                          'ActualMaterial' : x.product_uom_qty
                                      }))
                record.MaterialLines = materials
                
                processes = []
                for x in record.ProductionId.workorder_ids:
                    processes.append((0,0,
                                      {
                                          'WorkOrder' : x,
                                          'ActualTime' : x.duration_expected
                                      }))
                record.WorkOrders = processes
                
                #record.WorkOrders = record.ProductionId.workorder_ids
        
    def Confirm(self):
        if self.ProductionId.workorder_ids:
            process = self.ProductionId.workorder_ids.filtered(lambda x: len(x.move_raw_ids) > 0)[0]
            computed = []
            for mat in self.MaterialLines:
                if mat.Material:
                    record = process.EstimateMaterials.search([('WorkOrderId','=',process.id),('product_id','=',mat.Material.product_id.id),('id','not in',computed)],limit=1)
                    record.write({'MaterialUsed': mat.ActualMaterial})
                    computed.append(record.id)
        
        for wo in self.WorkOrders:
            if wo.WorkOrder:
                wo.WorkOrder.write({'ActualTime': wo.ActualTime})
                if wo.WorkOrder.button_start():
                    wo.WorkOrder.do_finish()
                