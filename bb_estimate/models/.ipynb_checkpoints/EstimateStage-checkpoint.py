# -*- coding: utf-8 -*-

from odoo import models, fields, api

class EstimageStage(models.Model):
    _name = 'bb_estimate.stage'
    _description = 'Estimate Stage'
    
    name = fields.Char('Name', required=True)
    isOrder = fields.Boolean('Conversion Stage')
    ConvertedStage = fields.Boolean('Converted Stage')
    LeadStage = fields.Many2one('crm.stage','Enquiry Stage')