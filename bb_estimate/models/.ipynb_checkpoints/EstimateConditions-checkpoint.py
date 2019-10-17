# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from datetime import datetime


class EstimateConditions(models.Model):
    _name = 'bb_estimate.conditions'
    _description = 'Estimate Conditions'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Short Name')
    description = fields.Text('Condition Text')
    isDefault = fields.Boolean('Is Default')
    