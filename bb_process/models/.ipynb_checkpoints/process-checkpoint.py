# -*- coding: utf-8 -*-

from odoo import models, fields, api

class QtyBreakParams(models.Model):
    _name="bb_process.process"
    
    name = fields.Char('Name', required=True)