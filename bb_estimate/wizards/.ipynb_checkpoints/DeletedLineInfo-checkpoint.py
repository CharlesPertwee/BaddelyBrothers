# -*- coding: utf-8 -*-
import odoo
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError

class DeletedLineInfo(models.TransientModel):
    _name="estimate.delete_line_info"
    
    info = fields.Text(string="Information")