# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductsSales(models.Model):
    _inherit = 'product.template'
    _name = 'product.template'
    
    roundOff = fields.Integer(string='Round Off', default=100)