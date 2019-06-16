# -*- coding: utf-8 -*-

from collections import namedtuple
import json
import time

from itertools import groupby
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from operator import itemgetter
import math

class PickingType(models.Model):
    _inherit = "stock.picking"
    
    def _estimate_pack(self,sale):
        package = False
        picks = self.filtered(lambda p: p.state not in ('done', 'cancel'))
        if picks:
            return {
                    'view_type' : 'form',
                    'view_mode' : 'form',
                    'name': 'Packages',
                    'res_model' : 'bb_estimate.picking',
                    'type' : 'ir.actions.act_window',
                    'context' : "{'default_Pick' : active_id}",
                    'target' : 'new',
                }
        return None
        
    def put_in_pack(self):
        res = self.check_destinations()
        if res.get('type'):
            return res
        sale = self.env['sale.order'].sudo().search([('name','=',self.origin)])
        if sale:
            sale = sale[0]
        if sale.Estimate:
            return self._estimate_pack(sale)
        else:
            return self._put_in_pack()