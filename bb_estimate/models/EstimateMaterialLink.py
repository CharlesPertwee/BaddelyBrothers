# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MaterialLink(models.Model):
    _name = 'bb_estimate.material_link'
    _description = 'Estimate Material Link'
    
    materialLine = fields.Many2one('bb_estimate.estimate_line',string="Material",domain="[('option_type','=','material')]", required=True)
    processLine = fields.Many2one('bb_estimate.estimate_line',string="Process",domain="[('option_type','=','process')]", required=True)
    estimate = fields.Many2one('bb_estimate.estimate')
    
    overs_only = fields.Boolean('Overs Only?')
    working_sheets_quantity_1 = fields.Integer('Working Sheets Required Qty 1', related="processLine.process_working_sheets_quantity_1", readonly=True)
    working_sheets_quantity_2 = fields.Integer('Working Sheets Required Qty 2', related="processLine.process_working_sheets_quantity_2", readonly=True)
    working_sheets_quantity_3 = fields.Integer('Working Sheets Required Qty 3', related="processLine.process_working_sheets_quantity_3", readonly=True)
    working_sheets_quantity_4 = fields.Integer('Working Sheets Required Qty 4', related="processLine.process_working_sheets_quantity_4", readonly=True)
    working_sheets_quantity_run_on = fields.Integer('Working Sheets Required Qty Run On', related="processLine.process_working_sheets_quantity_run_on", readonly=True)
    
    overs_quantity_1 = fields.Integer('Overs Required Qty 1', related="processLine.process_overs_quantity_1", readonly=True)
    overs_quantity_2 = fields.Integer('Overs Required Qty 2', related="processLine.process_overs_quantity_2", readonly=True)
    overs_quantity_3 = fields.Integer('Overs Required Qty 3', related="processLine.process_overs_quantity_3", readonly=True)
    overs_quantity_4 = fields.Integer('Overs Required Qty 4', related="processLine.process_overs_quantity_4", readonly=True)
    overs_quantity_run_on = fields.Integer('Overs Required Qty Run On', related="processLine.process_overs_quantity_run_on", readonly=True)
    
    material = fields.Many2one('product.product',related="materialLine.material", readonly=True)
    workcenter = fields.Many2one('mrp.workcenter',related="processLine.workcenterId", readonly=True)
    
    process_grammage = fields.Integer('Process Grammage(G.S.M)',related="processLine.grammage", readonly=True)
    process_number = fields.Integer('Process Number Up',related="processLine.param_number_up", readonly=True)
    work_twist = fields.Boolean('Work & Twist',related="processLine.work_twist", readonly=True)
    
    
    