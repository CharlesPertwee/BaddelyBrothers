# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

DIE_SIZES = [
    ('standard','No Die (No Charge)'),
    ('small','Crest Die'),
    ('medium','Heading Die'),
    ('large','Invitation Die')
]

class Estimate(models.Model):
    _name = 'bb_estimate.estimate'
    
    #Estimate For Fields
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    contact = fields.Many2one('res.partner', string='Contact')
    project = fields.Many2one('project.project', string='Project')
    invoice_account = fields.Many2one('res.partner', string='Invoice Account')
    invoice_address = fields.Many2one('res.partner', string='Invoice Address')
    invoice_contact = fields.Many2one('res.partner', string='Invoice Contact')
    
    #Estimate Summary
    title = fields.Char('Title',required=True)
    product_type = fields.Many2one('product.product', string='Product Type')
    estimate_date = fields.Date('Estimate Date')
    estimator = fields.Many2one('res.users','Estimator')
    office_copy = fields.Boolean('Office copy')
    estimate_number = fields.Char('Estimate Number')#, compute='generate_estimate_number')        
    event_date = fields.Date('Event Date')
    target_dispatch_date = fields.Date('Target Dispatch Date')
    
    #Estimate Detailed Screen
    state = fields.Many2one('bb_estimate.stage','State',default=lambda self: self.env['bb_estimate.stage'].search([])[0])
    estimate_line = fields.One2many('bb_estimate.estimate_line','estimate_id',string='Estimate Line')

    quantity_1 = fields.Integer('Quantity 1')    
    quantity_2 = fields.Integer('Quantity 2')
    quantity_3 = fields.Integer('Quantity 3')
    quantity_4 = fields.Integer('Quantity 4')
    run_on =  fields.Integer('Run on')
    nett_value_1 = fields.Float('Nett Value') 
    nett_value_2 = fields.Float('Nett Value 1')
    nett_value_3 = fields.Float('Nett Value 3')
    nett_value_4 = fields.Float('Nett Value 4')

    number_up = fields.Integer('Number up')

    grammage = fields.Integer('Grammage(g.s.m)')
    