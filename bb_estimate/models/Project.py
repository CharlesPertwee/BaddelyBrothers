from collections import defaultdict

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round

class Project(models.Model):
    _inherit = 'project.project'
    
    Estimates = fields.One2many('bb_estimate.estimate','project','Estimates')
    Leads = fields.One2many('crm.lead','Project','Leads/Opportunity')
    SalesOrder = fields.One2many('sale.order','Project','Sales Orders')
    Productions = fields.One2many('mrp.production','Project','Job Tickets')
    Invoices = fields.One2many('account.invoice','Project','Invoices')
    Deliveries = fields.One2many('stock.picking','Project','Deliveries')
    Purchase = fields.Many2many('purchase.order',string='Purchase')
    
    allow_timesheets = fields.Boolean("Allow timesheets", default=False)
