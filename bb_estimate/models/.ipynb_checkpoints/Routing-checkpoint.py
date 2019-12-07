# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round

class Routing(models.Model):
    _inherit = 'mrp.routing.workcenter'
    
    EstimateLineId = fields.Many2one('bb_estimate.estimate_line')