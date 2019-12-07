# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.tools import float_round

class ProductsSales(models.Model):
    _inherit = 'product.template'
    _name = 'product.template'
    
    roundOff = fields.Integer(string='Round Off', default=100)
    website_price = fields.Float('Website price', compute='_website_price', digits=dp.get_precision('Website Price'))
    website_public_price = fields.Float('Website public price', compute='_website_price', digits=dp.get_precision('Website Price'))
    
#     @api.multi
#     def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
#         combination = super(ProductsSales,self)._get_combination_info()
#         combination['price'] = float_round(combination['price'], precision_rounding=2)#dp.get_precision('Website Price'))
#         combination['list_price'] = float_round(combination['list_price'], precision_rounding=2)#dp.get_precision('Website Price'))
#         return combination
        
class Product(models.Model):
    _inherit = 'product.product'
    
    website_price = fields.Float('Website price', compute='_website_price', digits=dp.get_precision('Website Price'))
    website_public_price = fields.Float('Website public price', compute='_website_price', digits=dp.get_precision('Website Price'))
    
