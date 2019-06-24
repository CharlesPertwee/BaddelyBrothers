import odoo
from odoo import models, fields, api

class PriceAdjustment(models.TransientModel):
    _name = 'bb_estimate.adjust_price'
    
    Estimate = fields.Many2one('bb_estimate.estimate', string="Estimate")
    EstimateQuantity1 = fields.Integer('Estimate Quantity 1',related="Estimate.quantity_1")
    EstimateQuantity2 = fields.Integer('Estimate Quantity 2',related="Estimate.quantity_2")
    EstimateQuantity3 = fields.Integer('Estimate Quantity 3',related="Estimate.quantity_3")
    EstimateQuantity4 = fields.Integer('Estimate Quantity 4',related="Estimate.quantity_4")
    EstimateQuantityRunOn = fields.Integer('Estimate Quantity run on',related="Estimate.run_on")
    
    EstimatePrice1 = fields.Float('Price 1',related="Estimate.total_price_1" ,digits=(16,2))
    EstimatePrice2 = fields.Float('Price 2',related="Estimate.total_price_2" ,digits=(16,2))
    EstimatePrice3 = fields.Float('Price 3',related="Estimate.total_price_3", digits=(16,2))
    EstimatePrice4 = fields.Float('Price 4',related="Estimate.total_price_4", digits=(16,2))
    EstimatePriceRunOn = fields.Float('Price run on',related="Estimate.total_price_run_on", digits=(16,2))
    
    AdjustedPrice1 = fields.Float('Adjusted Price 1', digits=(16,2))
    AdjustedPrice2 = fields.Float('Adjusted Price 2', digits=(16,2))
    AdjustedPrice3 = fields.Float('Adjusted Price 3', digits=(16,2))
    AdjustedPrice4 = fields.Float('Adjusted Price 4', digits=(16,2))
    AdjustedPriceRunOn = fields.Float('Adjusted Price run on', digits=(16,2))
    
    AdjustPricePercent1 = fields.Float('Adjusted Percentage 1')
    AdjustPricePercent2 = fields.Float('Adjusted Percentage 2')
    AdjustPricePercent3 = fields.Float('Adjusted Percentage 3')
    AdjustPricePercent4 = fields.Float('Adjusted Percentage 4')
    AdjustPricePercentRunOn = fields.Float('Adjusted Percentage run on')
    
    PriceDelta1 = fields.Float('Price Delta 1')
    PriceDelta2 = fields.Float('Price Delta 2')
    PriceDelta3 = fields.Float('Price Delta 3')
    PriceDelta4 = fields.Float('Price Delta 4')
    PriceDeltaRunOn = fields.Float('Price Delta run on')
    
    PricePer1000_1 = fields.Float('Price Per 1000 1', digits=(16,2))
    PricePer1000_2 = fields.Float('Price Per 1000 2', digits=(16,2))
    PricePer1000_3 = fields.Float('Price Per 1000 3', digits=(16,2))
    PricePer1000_4 = fields.Float('Price Per 1000 4', digits=(16,2))
    PricePer1000_RunOn = fields.Float('Price Per 1000 run on', digits=(16,2))
    
    @api.onchange('Estimate')
    def _computePrices(self):
        for record in self:
            if record.Estimate:
                record.PricePer1000_1 = record.Estimate.total_price_1000_1
                record.PricePer1000_2 = record.Estimate.total_price_1000_2
                record.PricePer1000_3 = record.Estimate.total_price_1000_3
                record.PricePer1000_4 = record.Estimate.total_price_1000_4
                record.PricePer1000_RunOn = record.Estimate.total_price_1000_run_on
                
                record.AdjustedPrice1 = record.Estimate.total_price_1
                record.AdjustedPrice2 =  record.Estimate.total_price_2
                record.AdjustedPrice3 =  record.Estimate.total_price_3
                record.AdjustedPrice4 = record.Estimate.total_price_4
                record.AdjustedPriceRunOn = record.Estimate.total_price_run_on
    
    def PriceComputation(self,qty):
        for record in self:
            if record['AdjustedPrice'+qty]:
                record['AdjustPricePercent'+qty] = ((record['AdjustedPrice'+qty] / record['EstimatePrice'+qty]) - 1) * 100.0
                record['PriceDelta'+qty] = record['AdjustedPrice'+qty] - record['EstimatePrice'+qty]
            if record['EstimateQuantity'+qty] > 0:
                record['PricePer1000_'+qty] = (record['AdjustedPrice'+qty] / record['EstimateQuantity'+qty]) * 1000
    
    def PercenageComputation(self,qty):
        for record in self:
            if record['AdjustPricePercent'+qty]:
                record['AdjustedPrice'+qty] = record['EstimatePrice'+qty] * ((100 + record['AdjustPricePercent'+qty]) / 100.0)
                record['PriceDelta'+qty] = record['AdjustedPrice'+qty] - record['EstimatePrice'+qty]
            if record['EstimateQuantity'+qty]> 0:
                record['PricePer1000_'+qty] = (record['AdjustedPrice'+qty] / record['EstimateQuantity'+qty]) * 1000
    
    @api.onchange('AdjustedPrice1')
    def computePrices1(self):
        self.PriceComputation('1')
    
    @api.onchange('AdjustPricePercent1')
    def computePercentage1(self):
        self.PercenageComputation('1')
                
    @api.onchange('AdjustedPrice2')
    def computePrices2(self):
        self.PriceComputation('2')
    
    @api.onchange('AdjustPricePercent2')
    def computePercentage2(self):
        self.PercenageComputation('2')

    @api.onchange('AdjustedPrice3')
    def computePrices3(self):
        self.PriceComputation('3')
    
    @api.onchange('AdjustPricePercent3')
    def computePercentage3(self):
        self.PercenageComputation('3')
    
    @api.onchange('AdjustedPrice4')
    def computePrices4(self):
        self.PriceComputation('4')
    
    @api.onchange('AdjustPricePercent4')
    def computePercentage4(self):
        self.PercenageComputation('4')
    
    @api.onchange('AdjustedPriceRunOn')
    def computePricesRunOn(self):
        self.PriceComputation('RunOn')
    
    @api.onchange('AdjustPricePercentRunOn')
    def computePercentageRunOn(self):
        self.PercenageComputation('RunOn')
                
    def Confirm(self):
        if self.Estimate:
            self.Estimate.write(
                {
                    'total_price_1':self.AdjustedPrice1,
                    'total_price_2':self.AdjustedPrice2,
                    'total_price_3':self.AdjustedPrice3,
                    'total_price_4':self.AdjustedPrice4,
                    'total_price_run_on':self.AdjustedPriceRunOn,
                    'total_price_1000_1':self.PricePer1000_1,
                    'total_price_1000_2':self.PricePer1000_2,
                    'total_price_1000_3':self.PricePer1000_3,
                    'total_price_1000_4':self.PricePer1000_4,
                    'total_price_1000_run_on':self.PricePer1000_RunOn,
                }
            )
            self.Estimate.message_post(body="Adjusted Price for estimate")