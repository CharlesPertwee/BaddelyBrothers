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

# class Package(models.TransientModel):
#     _name = 'bb_estimate.picking_line'
    
#     PickId = fields.Many2one('bb_estimate.picking','Picking')
#     NoOfBoxes = fields.Integer('No Of Boxes')
#     QuantityPerBox = fields.Integer('Quantity Per Box')

class Packing(models.TransientModel):
    _name = 'bb_estimate.picking'
    
    Pick = fields.Many2one('stock.picking','Pick')
    Quantity = fields.Float('Quantity Done')#,related="Pick.quantity_done")
    QuantityPerBox = fields.Integer('Quantity Per Box')
    #Packages = fields.One2many('bb_estimate.picking_line','PickId')
    
    NoOfBox1 = fields.Integer('Quantity')
    CapacityBox1 = fields.Integer('Quantity Per Box')
    
    NoOfBox2 = fields.Integer('Quantity')
    CapacityBox2 = fields.Integer('Quantity Per Box')
    
    @api.onchange('Quantity','QuantityPerBox')
    def _changeQuantityPerBox(self):
        for record in self:
            if record.Quantity and record.QuantityPerBox:
                if record.Quantity < record.QuantityPerBox:
                    record.NoOfBox1 = 1
                    record.CapacityBox1 = record.Quantity
                else:
                    record.NoOfBox1 = math.floor(float(record.Quantity) / float(record.QuantityPerBox))
                    record.CapacityBox1 = record.QuantityPerBox

                    QtyRemaining = float(record.Quantity) % float(record.QuantityPerBox)

                    if QtyRemaining > 0.0:
                        record.NoOfBox2 = 1
                        record.CapacityBox2 = QtyRemaining

    @api.onchange('Pick')
    def _computePickup(self):
        for record in self:
            if record.Pick.move_ids_without_package:
                qty_done = sum([x.qty_done for x in record.Pick.move_line_ids.filtered(lambda o: o.qty_done > 0 and o.result_package_id)])
                record.Quantity = record.Pick.move_ids_without_package[0].quantity_done - qty_done
                
            
    def Confirm(self):
        move_line_ids = self.Pick.move_line_ids.filtered(lambda o: o.qty_done > 0 and not o.result_package_id)
        pick = self.Pick
        if move_line_ids:
            ml = move_line_ids[0]
            move_lines_to_pack = self.env['stock.move.line']
            
            rec = [(self.NoOfBox1,self.CapacityBox1),(self.NoOfBox2,self.CapacityBox2)]
            for line in rec:
                for pack in range(line[0]):
                    package = self.env['stock.quant.package'].create({})
                    
                    if float_compare(ml.qty_done, ml.product_uom_qty, precision_rounding=ml.product_uom_id.rounding) >= 0:
                        move_lines_to_pack = ml
                    else:
                        quantity_left_todo = float_round(ml.product_uom_qty - line[1], precision_rounding=ml.product_uom_id.rounding, rounding_method='UP')
                        done_to_keep = line[1]
                        new_move_line = ml.copy(default={'product_uom_qty': 0, 'qty_done': line[1]})
                        ml.write({'product_uom_qty': quantity_left_todo, 'qty_done': 0.0})
                        new_move_line.write({'product_uom_qty': done_to_keep})
                        move_lines_to_pack = new_move_line
                    
                    package_level = self.env['stock.package_level'].create({
                        'package_id': package.id,
                        'picking_id': pick.id,
                        'location_id': False,
                        'location_dest_id': move_line_ids.mapped('location_dest_id').id,
                        'move_line_ids': [(6, 0, move_lines_to_pack.ids)]
                    })
                    move_lines_to_pack.write({
                        'result_package_id': package.id,
                    })
        else:
            raise UserError(_('You must first set the quantity you will put in the pack.'))
            