# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductsTemplate(models.Model):
    _inherit = 'product.template'
    _name = 'product.template'

    estimateAvailable = fields.Boolean(string='Available in Estimating?')
    grammage = fields.Char(string='Grammage (G.S.M)')
    sheetSize = fields.Char(string='Sheet Size')
    margin = fields.Float(string='Margin', compute='_compute_margin')


    def _compute_margin(self):
        margin = 0
        if self.standard_price == 0:
            margin = 100
        else:
            margin = ((self.list_price - self.standard_price)/self.standard_price) * 100

        self.margin = margin


    