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
    margin = fields.Float(string='Margin')#,compute="_compute_margin")
    sheet_width = fields.Integer(string='Sheet Width(mm)')
    sheet_height = fields.Integer(string='Sheet Height(mm)')
    thickness = fields.Float(string='Thickness(microns)')
    staticPrice = fields.Boolean('Static Price')
    
    @api.onchange('margin')
    def calcPriceChange(self):
        for record in self:
            record.list_price = ((record.margin / 100) + 1) * record.standard_price
            
    @api.onchange('list_price')
    def calcListPriceChange(self):
        for record in self:
            if record.list_price:
                record.margin = ((record.list_price / record.standard_price) - 1) * 100 if record.standard_price else 0.0
            elif record.margin:
                record.standard_price = record.list_price / ((record.margin / 100) + 1)
                
    @api.onchange('standard_price')
    def calcStandardPriceChange(self):
        for record in self:
            if record.list_price:
                record.margin = ((record.list_price / record.standard_price) - 1) * 100 if record.standard_price else 0.0
            elif record.margin:
                record.list_price = ((record.margin / 100) + 1) * record.standard_price
                
        
    @api.onchange('sheetSize')
    def calc_sheet_dimen(self):
        for record in self:
            if record.sheetSize:
                record.sheet_width = record.sheetSize.width
                record.sheet_height = record.sheetSize.height

class Products(models.Model):
    _inherit = 'product.product'
    
    def _get_name(self):
        product = self
        name = product.name
        if product.sheetSize:
            name = "%s (%d X %d) - %d G.S.M"%(name,product.sheet_width,product.sheet_height,product.grammage)            
            #name = name + "  " + product.sheetSize.name
        return name
    
    @api.multi
    def name_get(self):
        res = []
        for product in self:
            name = product._get_name()
            res.append((product.id, name))
        return res