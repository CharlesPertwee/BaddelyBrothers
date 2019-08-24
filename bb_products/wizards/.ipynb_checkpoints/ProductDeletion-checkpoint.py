# -*- coding: utf-8 -*-
import odoo
import datetime
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError

class ProductDeletion(models.TransientModel):
    _name = "product.delete_by_date"
    
    deleteBy = fields.Selection([('Date','Date Before'),('Month','No of Months Before')], string="Delete By", default = "Date")
    deletionDate = fields.Date(string="Delete Before Date",required=True)
    deletionMonth = fields.Integer(string="Delete Before Month")
    
    def DeleteProducts(self):
        products = self.env['product.template'].sudo().search([('active','=',True)])
        noUsedProducts = True
        if self.deleteBy == "Date":
            date = datetime.datetime(self.deletionDate.year, self.deletionDate.month, self.deletionDate.day)
            if date > datetime.datetime.now():
                raise ValidationError("You can't enter the future date.")
            
            for product in products:
                if product.lastUsedEstimateDate and (product.lastUsedEstimateDate < self.deletionDate):
                    noUsedProducts = False
                    product.write({'active':False})
            
            if noUsedProducts:
                raise ValidationError("No products found.")
                    
        if self.deleteBy == "Month":
            if self.deletionMonth <= 0:
                raise ValidationError("Invalid month entry")
            
            deletionDate = datetime.datetime.now() - datetime.timedelta(days= self.deletionMonth * 30)
            
            for product in products:
                if product.lastUsedEstimateDate:
                    date = datetime.datetime(product.lastUsedEstimateDate.year, product.lastUsedEstimateDate.month, product.lastUsedEstimateDate.day)
                    if product.lastUsedEstimateDate and (date < deletionDate):
                        noUsedProducts = False
                        product.write({'active':False})
                    
            if noUsedProducts:
                raise ValidationError("No products found.")