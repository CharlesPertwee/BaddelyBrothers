# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductSize(models.Model):
    _name = 'bb_products.material_size'
    
    name = fields.Char('Size Name')
    width = fields.Integer('Width(m.m)')
    height = fields.Integer('Height(m.m)')
    flatWidth = fields.Integer('Flat / Working Width(m.m)')
    flatHeight = fields.Integer('Flat / Working Height(m.m)')
    isEnvelopeEstimate = fields.Boolean('Is EnvelopeSize?')
    isPrintSize = fields.Boolean('Is Print Size?')
    isEnquirySize = fields.Boolean('Available for Enquiries?')
    knifeNumber = fields.Char('Knife Number')