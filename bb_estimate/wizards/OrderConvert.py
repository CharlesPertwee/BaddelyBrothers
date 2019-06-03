# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OrderConvert(models.TransientModel):
    _name = "bb_estimate.wizard_order_convert"
    
    EstimateId = fields.Many2one('bb_estimate.estimate', string="Estimate",readonly=True)
    QuantityRequired = fields.Selection([('','')],string='Quantity Required',compute="getEstimateQuantity", required=True)
    
    TotalQuantity = fields.Integer('Total Quantity',readonly=True)
    TotalPrice = fields.Float('Total Price',readonly=True)
    
    RunOnQuantity = fields.Integer('Run on Quantity',readonly=True)
    RunOnPrice = fields.Float('Run on Price(GBP)',readonly=True)
    RunOnRequired = fields.Integer('Run on Quantity Required', required=True)
    
    ExtrasApplied = fields.Boolean('Extras Applied to the Estimate')
    HasExtra = fields.Boolean('Has Extra',compute="getEstimateExtra")
    
    @api.depends('HasExtra')
    def getEstimateExtra(self):
        for record in self:
            if record.EstimateId.HasExtra:
                record.HasExtra = True
                
    def CreateOrder(self):
        pass