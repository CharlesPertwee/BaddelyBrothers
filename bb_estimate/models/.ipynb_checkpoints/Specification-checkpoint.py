# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SpecList(models.Model):
    _name="bb_estimate.specification"
    
    name = fields.Char('Option',store=True,required=True)
    value = fields.Char('Value',store=True,required=True)