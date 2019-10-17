# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError

class ProductsTemplate(models.Model):
    _inherit = 'product.template'
    _name = 'product.template'
    
        
    @api.constrains('isEnvelope')
    def checkEnvelopeProductUse(self):
        if any(self.env['bb_estimate.estimate'].sudo().search([('product_type','=',self.id)])):
            raise ValidationError("Cannot modify isEnvelope, its been used in Estimate")