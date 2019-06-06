# -*- coding: utf-8 -*-

from odoo import models, fields, api

class EstimageStage(models.Model):
    _name = 'bb_estimate.stage'
    
    name = fields.Char('Name', required=True)
    isOrder = fields.Boolean('Show MO button')
    