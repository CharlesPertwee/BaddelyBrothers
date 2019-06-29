# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Leads(models.Model):
    _inherit = 'crm.lead'
    
    Estimates = fields.One2many('bb_estimate.estimate','lead','Estimates')
    Estimate_Count = fields.Integer('Processes',compute='_compute_estimates')
    Project = fields.Many2one('project.project')
    
    def _compute_estimates(self):
            for record in self:
                self.Estimate_Count = len(record.Estimates)