# -*- coding: utf-8 -*-
import odoo
import datetime
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError

class ProductDeletion(models.TransientModel):
    _name = "product.delete_by_date"
    deletionDate = fields.Date(string="Delete Before Date",required=True)
    
    def DeleteProducts(self):
        if self.deletionDate > datetime.date.today():
            raise ValidationError("You can't enter the future date.")
        
        products = self.env['product.template'].sudo().search([('active','=',True),('lastUsedEstimateDate','!=',False),('lastUsedEstimateDate','<',self.deletionDate)])
        products.write({'active':False})
        
        if len(products) == 0:
            raise ValidationError("%s Products Archived."%(len(products)))
