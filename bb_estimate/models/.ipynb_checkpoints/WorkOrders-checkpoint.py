# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from datetime import datetime

class WorkOrder(models.Model):
    _inherit = 'mrp.workorder'
    
    EstimateMaterials = fields.One2many('bb_estimate.work_material','WorkOrderId','Materials')
    ActualTime = fields.Float('Actual Time(hrs)')
    
class WorkOrderMaterial(models.Model):
    _name = 'bb_estimate.work_material'
    _description = 'Material usage for work orders'
    
    EstimateLineId = fields.Many2one('bb_estimate.estimate_line','Estimate Line',domain="[('option_type','=','material')]")
    name = fields.Char('Material Name',related="EstimateLineId.lineName")
    
    MaterialAllocated = fields.Integer('Estimate Material')
    MaterialUsed = fields.Integer('Actual Used!')
    
    WorkOrderId = fields.Many2one('mrp.workorder','Worder Order')
    