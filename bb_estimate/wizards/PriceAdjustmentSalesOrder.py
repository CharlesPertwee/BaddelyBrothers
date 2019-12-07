import odoo
from odoo import models, fields, api

class PriceAdjustment(models.TransientModel):
    _name = 'bb_estimate.adjust_price_so'
    
    SalesOrder = fields.Many2one('sale.order', string="Sales Order")
    Quantity = fields.Integer('Quantity',compute='_computePrices')
    Price = fields.Float('Price ')#,related="SalesOrder.amount_untaxed")
    AdjustedPrice = fields.Float('Adjusted Price')
    AdjustPricePercent = fields.Float('Adjusted Percentage')
    PriceDelta = fields.Float('Price Delta')
    
    @api.onchange('SalesOrder')
    def _computePrices(self):
        for record in self:
            if record.SalesOrder:
                record.Price = record.SalesOrder.amount_untaxed
                record.AdjustedPrice = record.SalesOrder.amount_untaxed
            if record.SalesOrder.order_line:
                record.Quantity = record.SalesOrder.order_line[0].product_uom_qty
    
    @api.onchange('AdjustedPrice')
    def computePrices(self):
        for record in self:
            if record.AdjustedPrice:
                record.AdjustPricePercent = ((record.AdjustedPrice / record.Price) - 1) * 100.0
                record.PriceDelta = record.AdjustedPrice - record.Price
    
    @api.onchange('AdjustPricePercent')
    def computePercentage(self):
        for record in self:
            if record.AdjustPricePercent:
                record.AdjustedPrice = record.Price * ((100 + record.AdjustPricePercent) / 100.0)
                record.PriceDelta = record.AdjustedPrice - record.Price
    
    def Confirm(self):
        if self.SalesOrder.order_line:
            record = self.SalesOrder.order_line[0]
            otherSum = sum([x.price_subtotal for x in self.SalesOrder.order_line if x.id != record.id])
            price = (self.AdjustedPrice - otherSum)
            current = self.SalesOrder.amount_untaxed 
            
            record.write(
                {
                    'price_unit': (price / self.Quantity)
                }
            )
            self.env['bb_estimate.price_history'].create(
                {
                    'CurrentPrice1':current,
                    'ChangedPrice1':self.SalesOrder.amount_untaxed,
                    'SalesOrder':self.SalesOrder.id
                    
                }
            )
            self.SalesOrder.message_post(body="Adjusted Price for Sales Order")