# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _

class AuditLog(models.Model):
    _name = "bb_estimate.audit_log"
    _order = 'id desc'
    
    estimate = fields.Many2one('bb_estimate.estimate',string="Estimate")
    estimateLine = fields.Char(string="Line Name")
    
    quantity_1 = fields.Integer('Quantity 1')
    quantity_2 = fields.Integer('Quantity 2')
    quantity_3 = fields.Integer('Quantity 3')
    quantity_4 = fields.Integer('Quantity 4')
    quantity_run_on = fields.Integer('Run On')
    
    changed_quantity_1 = fields.Integer('New Quantity 1')
    changed_quantity_2 = fields.Integer('New Quantity 2')
    changed_quantity_3 = fields.Integer('New Quantity 3')
    changed_quantity_4 = fields.Integer('New Quantity 4')
    changed_quantity_run_on = fields.Integer('New Quantity Run On')
    Action = fields.Selection([('Modify','Modify'),('Delete','Delete')], string="Action")