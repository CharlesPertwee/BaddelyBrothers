# -*- coding: utf-8 -*-

from odoo import models, fields, api
class ProductsTemplate(models.Model):
    _inherit = 'product.template'
    _name = 'product.template'
    
    productType = fields.Selection([('Stock','Stock Material'),('Trade Counter','Trade Counter'),('Non-Stock','Non Stockable Product'),('Finished','Finished Product'),('Package','Package'),('Delivery','Delivery')],string="Material Type",default="Trade Counter")
    isEnvelope = fields.Boolean('Is Envelope?')
    customerDescription = fields.Char('Standard customer Description')
    jobTicketDescription = fields.Char('Standard Job Ticket Text')
    estimateAvailable = fields.Boolean(string='Available in Estimating?')
    grammage = fields.Char(string='Grammage (G.S.M)')
    sheetSize = fields.Many2one('bb_products.material_size', string='Sheet Size')
    margin = fields.Float(string='Margin', compute='_compute_margin')
    sheet_width = fields.Integer(string='Sheet Width(mm)')
    sheet_height = fields.Integer(string='Sheet Height(mm)')
    thickness = fields.Float(string='Thickness(microns)')
    staticPrice = fields.Boolean('Static Price')
    
    def _compute_margin(self):
        for record in self:
            margin = 0
            if record.standard_price == 0:
                margin = 100
            else:
                margin = ((record.list_price - record.standard_price)/record.standard_price) * 100

            record.margin = margin
        
    @api.onchange('sheetSize')
    def calc_sheet_dimen(self):
        for record in self:
            if record.sheetSize:
                record.sheet_width = record.sheetSize.width
                record.sheet_height = record.sheetSize.height