from collections import defaultdict

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round

class Project(models.Model):
    _inherit = 'project.project'
    
    Estimates = fields.One2many('bb_estimate.estimate','project','Estimates')