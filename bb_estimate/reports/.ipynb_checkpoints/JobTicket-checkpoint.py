# -*- coding: utf-8 -*-
from odoo import api, models


class MrpCostStructure(models.AbstractModel):
    _name = "report.job_ticket"
    
#     @api.multi
#     def get_lines(self, productions):
#         res = []
#         return res
    
#     @api.model
#     def get_report_values(self, docids, data=None):
#         productions = self.env['mrp.production']\
#             .browse(docids)\
#             .filtered(lambda p: p.state != 'cancel')
#         res = self.get_lines(productions)
#         return {'lines': res}