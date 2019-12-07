from collections import defaultdict

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round

class PriceHistory(models.Model):
    _name = 'bb_estimate.price_history'
    _description = 'Price History'
    _order = "id desc"
    
    CurrentPrice1 = fields.Float('Price 1')
    CurrentPrice2 = fields.Float('Price 2')
    CurrentPrice3 = fields.Float('Price 3')
    CurrentPrice4 = fields.Float('Price 4')
    CurrentPriceRunOn = fields.Float('Price Run On')
    
    ChangedPrice1 = fields.Float('Changed Price 1')
    ChangedPrice2 = fields.Float('Changed Price 2')
    ChangedPrice3 = fields.Float('Changed Price 3')
    ChangedPrice4 = fields.Float('Changed Price 4')
    ChangedPriceRunOn = fields.Float('Changed Price Run On')
    
    Estimate = fields.Many2one('bb_estimate.estimate')
    SalesOrder = fields.Many2one('sale.order')
    
    