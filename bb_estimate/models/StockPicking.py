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
    
    Project = fields.Many2one('project.project','Project')
    customerRef = fields.Char('Customer Reference')
    consignmentNumber = fields.Char('Consignment Number')
    
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         res = super(PickingType, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
#         raise Exception(res)
#         if res.get('picking_type_code'):
#             raise Exception("THIS")
#             if res.get('toolbar', False) and res.get('toolbar').get('print', False):
#                 reports = res.get('toolbar').get('print')
#                 type = self._context.get('type')
#                 if type == 'in_invoice':
#                     _reports = [x for x in reports if not x['report_name'].startswith('bb_estimate')]
#                     res['toolbar']['print'] = _reports
#                 elif type == 'out_invoice':
#                     _reports = [x for x in reports if x['report_name'].startswith('bb_estimate')]
#                     res['toolbar']['print'] = _reports
#                 else:
#                     pass
                
#         return res
    
    @api.multi
    def do_print_picking(self):
        self.write({'printed': True})
        return self.env.ref('bb_estimate.delievery_note').report_action(self)
    
    @api.model
    def create(self,vals):
        if vals['origin']:
            sale_order = self.env['sale.order'].sudo().search([('name','=',vals['origin'])])
            if sale_order.Estimate:
                vals['Project'] = sale_order.Estimate.project.id
        return super(PickingType,self).create(vals)
    
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
    
    @api.model
    def getEstimateData(self):
        for record in self:
            return self.env['bb_estimate.estimate'].sudo().search([('salesOrder','=',record.origin)])
        
    def GetProductData(self):
        packs = {}
        for x in self.move_line_ids_without_package:
            if not (x.product_id.productType == 'Package'):
                if x.qty_done > 0:
                    if "%d,%d"%(x.product_id.id,x.qty_done) in packs.keys():
                        packs["%d,%d"%(x.product_id.id,x.qty_done)] += 1
                    else:
                        packs["%d,%d"%(x.product_id.id,x.qty_done)] = 1
        
        result = ["%d box(es) of %s per box"%(packs[x],x.split(',')[1]) for x in packs.keys()]
        return result
    
    def TotalBoxes(self):
        lines = self.GetProductData()
        return sum([int(x.split()[0]) for x in lines])
    
    def calculatePrice(self):
        sale = self.env['sale.order'].sudo().search([('name','=',self.origin)])
        estimate = sale.Estimate
        price = ((estimate['total_price_%s'%(estimate.selectedQuantity)] - estimate['total_price_extra_%s'%(estimate.selectedQuantity)]) * estimate.SelectedQtyRatio) + ((estimate.total_price_run_on - estimate.total_price_extra_run_on) * estimate.selectedRatio)
        return str(price)
    
    