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
        
        packingMaterial = sale.Estimate.estimate_line.search([('estimate_id','=',sale.Estimate.id),('documentCatergory','=','Packing'),('option_type','=','material')])
        
        if packingMaterial and len(packingMaterial) > 1:
            raise UserError(_('Multiple Packing added.'))
        elif packingMaterial:
            quantity = sale.Estimate['quantity_'+sale.Estimate.selectedQuantity]
            runOnQuantity = sale.Estimate.selectedRunOn
            packages = {
                'quantity': (int(math.ceil(packingMaterial['quantity_required_'+sale.Estimate.selectedQuantity])),quantity),
                'run_on': (int(math.ceil(packingMaterial.quantity_required_run_on * sale.Estimate.selectedRatio)),runOnQuantity)
            }
            
            #sheets = packingMaterial.param_sheets_per_box
            
            #SheetsPerBox = math.ceil(quantity / sheets) 
            
            for pick in self.filtered(lambda p: p.state not in ('done', 'cancel')):
                qty_done = sum([x.qty_done for x in pick.move_line_ids.filtered(lambda o: o.qty_done > 0 and not o.result_package_id)])
                if qty_done >= quantity:
                    ml = pick.move_line_ids.filtered(lambda o: o.qty_done > 0 and not o.result_package_id)[0] #move_line_ids
                    move_lines_to_pack = self.env['stock.move.line']
                    packaging_id = self.env['product.packaging'].search([('name','=',packingMaterial.lineName)])
                    if packaging_id:
                        packaging_id = packaging_id[0]
                    else:
                        packaging_id = self.env['product.packaging'].create({
                            'name': packingMaterial.lineName,
                            'max_weight': packingMaterial.material.weight
                        })
                    hasCommitted = False
                    for x in packages.keys():
                        qty_done = packages[x][1] / packages[x][0]
                        for y in range(packages[x][0]):
                            package = self.env['stock.quant.package'].create({'packaging_id': packaging_id.id})
                            
                            if not hasCommitted and float_compare(qty_done, ml.product_uom_qty, precision_rounding=ml.product_uom_id.rounding) >= 0:
                                move_lines_to_pack = ml
                                hasCommitted = True
                            else:
                                quantity_left_todo = float_round(ml.product_uom_qty - qty_done, precision_rounding=ml.product_uom_id.rounding, rounding_method='UP')
                                done_to_keep = qty_done
                                new_move_line = ml.copy(
                                    default={'product_uom_qty': 0, 'qty_done': qty_done})
                                ml.write({'product_uom_qty': quantity_left_todo, 'qty_done': done_to_keep})
                                new_move_line.write({'product_uom_qty': done_to_keep})
                                move_lines_to_pack = new_move_line
                    
                            package_level = self.env['stock.package_level'].create({
                                'package_id': package.id,
                                'picking_id': pick.id,
                                'location_id': False,
                                'location_dest_id': ml.mapped('location_dest_id').id,
                                'move_line_ids': [(6, 0, move_lines_to_pack.ids)]
                            })
                            move_lines_to_pack.write({
                                'result_package_id': package.id,
                            })
                else:
                    raise UserError(_('You must first complete the Manufacturing and set the quantity you will put in the packs.'))
        else:
            raise UserError(_('No packing process added to estimate.'))
        return package
    
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