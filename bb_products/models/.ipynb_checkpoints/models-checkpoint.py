# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductsTemplate(models.Model):
    _inherit = 'product.template'
    _name = 'product.template'

    estimateAvailable = fields.Boolean(string='Available in Estimating?')
    grammage = fields.Char(string='Grammage (G.S.M)')
    sheetSize = fields.Many2one('bb_products.material_size', string='Sheet Size')
    margin = fields.Float(string='Margin', compute='_compute_margin')
    sheet_width = fields.Integer(string='Sheet Width(mm)')
    sheet_height = fields.Integer(string='Sheet Height(mm)')
    thickness = fields.Float(string='Thickness(microns)')
    customerDescription = fields.Char('Standard customer Description')
    jobTicketDescription = fields.Char('Standard Job Ticket Text')
    
    def _compute_margin(self):
        margin = 0
        if self.standard_price == 0:
            margin = 100
        else:
            margin = ((self.list_price - self.standard_price)/self.standard_price) * 100

        self.margin = margin
        
    @api.onchange('sheetSize')
    def calc_sheet_dimen(self):
        for record in self:
            if record.sheetSize:
                record.sheet_width = record.sheetSize.width
                record.sheet_height = record.sheetSize.height
    


    