# -*- coding: utf-8 -*-

from odoo import models, fields, api

class EstimateLine(models.Model):
    _name = 'bb_estimate.estimate_line'
    
    workcenterId = fields.Many2one('mrp.workcenter', string="Process")
    material = fields.Many2one('product.product', string="Materials")
    estimate_id = fields.Many2one('bb_estimate.estimate','Estimate')