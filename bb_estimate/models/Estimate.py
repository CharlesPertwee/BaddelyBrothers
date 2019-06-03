# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from datetime import datetime

DIE_SIZES = [
    ('standard','No Die (No Charge)'),
    ('small','Crest Die'),
    ('medium','Heading Die'),
    ('large','Invitation Die')
]

ENVELOPE_TYPES = [
    ('none', ''),
    ('diamond', 'Diamond'),
    ('highcutdiamond','High Cut Diamond'),
    ('tuck', 'Tuck'),
    ('pocket', 'Pocket'),
    ('walletpocket','Walletstyle Pocket'),
    ('wallet', 'Wallet'),
    ('banker', 'Banker'),
    ('tissuelined', 'Tissue Lined, Embossed & Windowed'),
]

FLAP_GLUE_TYPES = [
    ('none', ''),
    ('gummed', 'Gummed'),
    ('doublegummed','Double Gummed'),
    ('peel', 'Peel & Stick'),
    ('ungummed', 'Un-gummed'),
    ('topless', 'Topless'),
    ('stringwasher', 'String & Washer'),
]

TISSUE_LINING_OPTIONS = [
    ('full', 'Yes - Fully'),
    ('half', 'Yes - Half'),
    ('unlined', 'Unlined'),
]

class Estimate(models.Model):
    _name = 'bb_estimate.estimate'
    _rec_name = 'title'
    
    @api.model
    def _read_group_state(self, stages, domain, order):
        stages = self.env['bb_estimate.stage'].sudo().search([])
        return stages
    
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
    state = fields.Many2one('bb_estimate.stage','State'
                            , ondelete='restrict'
                            , track_visibility='onchange'
                            , index=True
                            , group_expand='_read_group_state'
                            , default=lambda self: self.env['bb_estimate.stage'].search([])[0])
    estimate_line = fields.One2many('bb_estimate.estimate_line','estimate_id',string='Estimate Line',compute="_get_estimate_line")
    estimate_extra_line = fields.One2many('bb_estimate.estimate_line','estimate_id',string='Estimate Extra Line')
    
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
    finished_size = fields.Many2one('bb_estimate.material_size','Finished Size')
    finished_width = fields.Integer('Finished Width')
    finished_height = fields.Integer('Finished Height')
    working_size = fields.Many2one('bb_estimate.material_size','Working Size')
    working_width = fields.Integer('Working Width')
    working_height = fields.Integer('Working Height')
    knife_number = fields.Char('Knife Number')
    
    envelope_type = fields.Selection(ENVELOPE_TYPES,string="Envelope Type")
    flap_glue_type = fields.Selection(FLAP_GLUE_TYPES,string="Flap Glue Type")
    tissue_lined = fields.Selection(TISSUE_LINING_OPTIONS,'Tissue Lined')
    knife_number = fields.Char('Knife Number')
    embossed = fields.Boolean('Embossed')
    windowed = fields.Boolean('Windowed')
    standardWindowSize = fields.Boolean('Standard Window Size')
    windowHeight = fields.Float('Window Size: Height(mm)')
    windowWidth = fields.Float('Window Size:Widht(mm)')
    windowFlhs = fields.Float('Window Pos: FLHS')
    windowUp = fields.Float('Window Pos: Up')
    
    routings = fields.Many2one('mrp.routing','Generated Routing')
    bom = fields.Many2one('mrp.bom', 'Generated Bom')
    manufacturingOrder = fields.Many2one('mrp.production','Job Ticket')
    
    hasExtra = fields.Boolean('Has Extra',compute="getExtras")
    
    @api.depends('hasExtra')
    def getExtras(self):
        for record in self:
            for line in estimate_extra_line:
                if line.isExtra:
                    record.hasExtra = True
    
    
    @api.depends('estimate_line','estimate_extra_line')
    def _get_estimate_line(self):
        for record in self:
            record_not_extra = self.env['bb_estimate.estimate_line'].sudo().search([('estimate_id','=',record.id),('isExtra','=',False)])
            record.estimate_line = record_not_extra
    
    @api.onchange('finished_size')
    def finished_size_change(self):
        for record in self:
            record.finished_width = record.finished_size.width
            record.finished_height = record.finished_size.height
            if record.finished_size.isEnvelopeEstimate:
                record.working_size = record.finished_size.id
                record.working_width = record.finished_size.flatWidth
                record.working_height = record.finished_size.flatHeight
                record.knife_number = record.finished_size.knifeNumber
                
    @api.onchange('working_size')
    def working_size_change(self):
        for record in self:
            if record.working_size.isEnvelopeEstimate:
                record.working_width = record.working_size.flatWidth
                record.working_height = record.working_size.flatHeight
                record.knife_number = record.working_size.knifeNumber
            else:
                record.working_width = record.working_size.width
                record.working_height = record.working_size.height
    
    
    @api.onchange('partner_id')
    def PartnerUpdate(self):
        for record in self:
            record.invoice_account = record.partner_id
            customer_account_addresses = self.env['res.partner'].sudo().search(['&',('parent_id','=',record.partner_id.id),('type','=','invoice')])
            if(len(customer_account_addresses)>0):
                for address in customer_account_addresses:
                    record.invoice_address = address
                    break
            customer_contacts = self.env['res.partner'].sudo().search(['&','&',('parent_id','=',record.partner_id.id),('type','=','contact'),('employeeStatus','=','current')])
            if (len(customer_contacts)):
                for contacts in customer_contacts:
                    record.contact = contacts
                    record.invoice_contact = contacts
                    break
    
    @api.onchange('invoice_account')
    def InvoiceAccount(self):
        for records in self:
            customer_account_addresses = self.env['res.partner'].sudo().search(['&',('parent_id','=',records.partner_id.id),('type','=','invoice')])
            if(len(customer_account_addresses)>0):
                for address in customer_account_addresses:
                    records.invoice_address = address
                    break

            customer_contacts = self.env['res.partner'].sudo().search(['&','&',('parent_id','=',records.partner_id.id),('type','=','contact'),('employeeStatus','=','current')])
            if (len(customer_contacts)):
                for contacts in customer_contacts:
                    records.contact = contacts
                    records.invoice_contact = contacts
                    break
    
    def CreateManufacturingOrder(self):
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'name': 'Convert',
                'res_model' : 'bb_estimate.wizard_order_convert',
                'type' : 'ir.actions.act_window',
                'context' : "{'default_EstimateId' : active_id}",
                'target' : 'new'
            }
        
    def AddLineItem(self):
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'name': 'Add New Line',
                'res_model' : 'bb_estimate.estimate_line',
                'type' : 'ir.actions.act_window',
                'context' : "{'default_estimate_id' : active_id}",
                'target' : 'new'
            }