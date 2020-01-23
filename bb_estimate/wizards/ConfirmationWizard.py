# -*- coding: utf-8 -*-
import odoo
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError

class ConfirmationBox(models.TransientModel):
    _name = 'bb_estimate.confirmation_box'
    _desc = 'Confimation Box'
    
    data = fields.Text('Message')
    
