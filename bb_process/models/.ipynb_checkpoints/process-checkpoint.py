# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.safe_eval import safe_eval, test_python_expr
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError
import math

class EstimateLogic():
    def __init__(self,workcenter_Id,qty_params,cost_params,process_type,fieldUpdated,qty):
        self.workcenter_Id = workcenter_Id
        self.qty_params = qty_params
        self.cost_params = cost_params
        self.process_type = process_type
        self.fieldUpdated = fieldUpdated
        self.qty = qty
        
    def update(self,qty_params,cost_params,qty):
        #self.workcenter_Id = workcenter_Id
        self.qty_params = qty_params
        self.cost_params = cost_params
        #self.process_type = process_type
        #self.fieldUpdated = state_params
        self.qty = qty

class ProcessFields(models.Model):
    _name = 'bb_process.process_name'
    
    name = fields.Char('Name',required=True)
    process_type = fields.Many2one('bb_process.process','Process')
    
class ProcessTypes(models.Model):
    _name="bb_process.process"
    
    DEFAULT_PYTHON_CODE = """# Available variables:
#  - env: Odoo Environment on which the action is triggered
#  - model: Odoo Model of the record on which the action is triggered; is a void recordset
#  - workcenter: current workcenter
#  - estimate: estimate object which contains all the required parameters.
#  - time, datetime, dateutil, timezone: useful Python libraries
# To return an action, assign: action = {...}\n\n\n\n"""
    
    name = fields.Char('Name', required=True)
    processes = fields.One2many('mrp.workcenter','process_type',string="Processes")
    process_count = fields.Integer('Processes',compute='_compute_process')
    requiredFields = fields.One2many('bb_process.process_name','process_type',string="Required Fields")
    
    estimate = fields.Text(string='Estimate Logic', 
                           groups='base.group_system', 
                           default=DEFAULT_PYTHON_CODE,
                           help="Write Python code that the action will execute. Some variables are "
                           "available for use; help about python expression is given in the help tab.")
    
    def _compute_process(self):
        for record in self:
            self.process_count = len(record.processes)
    
    @api.constrains('estimate')
    def _check_python_code(self):
        for action in self:
            msg = test_python_expr(expr=action.estimate.strip(), mode="exec")
            if msg:
                raise ValidationError(msg)
    
    def get_default_field_values(self):
        param_defaults = {
            'param_number_up' : 1,
            'param_additional_charge' : 0.00,
            'param_number_of_colors' : 1,
            'param_misc_charge_per_cm2' : 0.0,
            'param_misc_charge_per_cm2_area' : 0.0,
            'param_number_out' : 1,
            'param_printed_material' : False,
        }    
        return param_defaults
    
    def UpdateEstimate(self,workcenter_Id, qty_params, cost_params, process_type, fieldUpdated, qty):
        estimate = EstimateLogic(workcenter_Id, qty_params, cost_params, process_type, fieldUpdated, qty)
        eval_context = {
                'env' : self.env,
                'model' : self.env['bb_process.process'].sudo(),
                'workcenter' : workcenter_Id,
                'estimate' : estimate,
                'math': math
        }
        safe_eval(self.sudo().estimate.strip(), eval_context, mode="exec", nocopy=True)
        qty_params.update(estimate.qty_params)
        cost_params.update(estimate.cost_params)
        
        #raise Exception(estimate.qty_params)
        
        


    
