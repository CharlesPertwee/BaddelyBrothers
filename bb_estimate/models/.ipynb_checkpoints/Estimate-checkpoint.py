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
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Estimate'
    _rec_name = 'title'
    
    
    @api.model
    def _read_group_state(self, stages, domain, order):
        stages = self.env['bb_estimate.stage'].sudo().search([])
        return stages
    
    #Estimate For Fields
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    contact = fields.Many2one('res.partner', string='Contact')
    project = fields.Many2one('project.project', string='Project',required=True)
    invoice_account = fields.Many2one('res.partner', string='Invoice Account')
    invoice_address = fields.Many2one('res.partner', string='Invoice Address')
    invoice_contact = fields.Many2one('res.partner', string='Invoice Contact')
    
    #Estimate Summary
    title = fields.Char('Title',required=True)
    product_type = fields.Many2one('product.product', string='Product Type',required=True)
    estimate_date = fields.Date('Estimate Date')
    estimator = fields.Many2one('res.users','Estimator', default=lambda self: self.env.uid)
    office_copy = fields.Boolean('Office copy')
    estimate_number = fields.Char('Estimate Number')        
    event_date = fields.Date('Event Date')
    target_dispatch_date = fields.Date('Target Dispatch Date')
    
    #Estimate Detailed Screen
    state = fields.Many2one('bb_estimate.stage','State'
                            , ondelete='restrict'
                            , track_visibility='onchange'
                            , index=True
                            , group_expand='_read_group_state'
                            , default=lambda self: self.env['bb_estimate.stage'].search([])[0])
    estimate_line = fields.One2many('bb_estimate.estimate_line','estimate_id',string='Estimate Line')
    
    #Delievery Details
    Delivery = fields.Many2one('res.partner',string="Delivery To",domain="[('type','=','delivery')]",required=True)
    DeliveryContact = fields.Many2one('res.partner',string="Delivery Contact",required=True)
    DeliveryMethod = fields.Many2one('product.product',string="Delivery Method",required=True) #delivery.carrier
    DeliveryLabel = fields.Boolean('Plain Label')
    
    quantity_1 = fields.Integer('Quantity 1')    
    quantity_2 = fields.Integer('Quantity 2')
    quantity_3 = fields.Integer('Quantity 3')
    quantity_4 = fields.Integer('Quantity 4')
    run_on =  fields.Integer('Run on')
    
    total_price_1 = fields.Float('Total Price 1',store=True,compute="_get_estimate_line")
    total_price_2 = fields.Float('Total Price 2',store=True,compute="_get_estimate_line")
    total_price_3 = fields.Float('Total Price 3',store=True,compute="_get_estimate_line")
    total_price_4 = fields.Float('Total Price 4',store=True,compute="_get_estimate_line")
    total_price_run_on = fields.Float('Run On',store=True,compute="_get_estimate_line")
    
    total_price_extra_1 = fields.Float('Total Price 1',store=True,compute="_get_estimate_line")
    total_price_extra_2 = fields.Float('Total Price 2',store=True,compute="_get_estimate_line")
    total_price_extra_3 = fields.Float('Total Price 3',store=True,compute="_get_estimate_line")
    total_price_extra_4 = fields.Float('Total Price 4',store=True,compute="_get_estimate_line")
    total_price_extra_run_on = fields.Float('Run On',store=True,compute="_get_estimate_line")
    
    total_cost_1 = fields.Float('Total Cost 1',store=True,compute="_get_estimate_line")
    total_cost_2 = fields.Float('Total Cost 2',store=True,compute="_get_estimate_line")
    total_cost_3 = fields.Float('Total Cost 3',store=True,compute="_get_estimate_line")
    total_cost_4 = fields.Float('Total Cost 4',store=True,compute="_get_estimate_line")
    total_cost_run_on = fields.Float('Run On',store=True,compute="_get_estimate_line")
    
    unAllocated_1 = fields.Integer('Un Allocated Quantity 1',store=True,compute="_get_estimate_line")
    unAllocated_2 = fields.Integer('Un Allocated Quantity 1',store=True,compute="_get_estimate_line")
    unAllocated_3 = fields.Integer('Un Allocated Quantity 1',store=True,compute="_get_estimate_line")
    unAllocated_4 = fields.Integer('Un Allocated Quantity 1',store=True,compute="_get_estimate_line")
    unAllocated_run_on = fields.Integer('Un Allocated Quantity 1',store=True,compute="_get_estimate_line")
    
    nett_value_1 = fields.Float('Nett Value') 
    nett_value_2 = fields.Float('Nett Value 1')
    nett_value_3 = fields.Float('Nett Value 3')
    nett_value_4 = fields.Float('Nett Value 4')

    number_up = fields.Integer('Number up', default=1 ,required=True )
    grammage = fields.Integer('Grammage (G.S.M)', required=True)
    finished_size = fields.Many2one('bb_products.material_size','Finished Size', required=True)
    finished_width = fields.Integer('Finished Width', required=True)
    finished_height = fields.Integer('Finished Height', required=True)
    working_size = fields.Many2one('bb_products.material_size','Working Size', required=True)
    working_width = fields.Integer('Working Width', required=True)
    working_height = fields.Integer('Working Height', required=True)
    knife_number = fields.Char('Knife Number')
    
    envelope_type = fields.Selection(ENVELOPE_TYPES,string="Envelope Type")
    flap_glue_type = fields.Selection(FLAP_GLUE_TYPES,string="Flap Glue Type")
    tissue_lined = fields.Selection(TISSUE_LINING_OPTIONS,'Tissue Lined')
    knife_number = fields.Char('Knife Number')
    embossed = fields.Boolean('Embossed')
    windowed = fields.Boolean('Windowed')
    standardWindowSize = fields.Boolean('Standard Window Size')
    windowHeight = fields.Float('Window Size: Height (mm)')
    windowWidth = fields.Float('Window Size:Widht (mm)')
    windowFlhs = fields.Float('Window Pos: FLHS')
    windowUp = fields.Float('Window Pos: Up')
    
    routings = fields.Many2one('mrp.routing','Generated Routing')
    bom = fields.Many2one('mrp.bom', 'Generated Bom')
    manufacturingOrder = fields.Many2one('mrp.production','Job Ticket')
    salesOrder = fields.Many2one('sale.order','Sales Order')
    
    hasExtra = fields.Boolean('Has Extra',compute="getExtras")
    estimateConditions = fields.Many2many('bb_estimate.conditions', string="Estimate Conditions")
    isEnvelope = fields.Boolean('Is Envelope',related="product_type.isEnvelope")
    showMo = fields.Boolean('Show Mo Button',related="state.isOrder")
    EnquiryComments = fields.Text('Enquiry Comments')
    SpecialInstuction = fields.Text('Special Instructions')
    PackingInstruction = fields.Text('Packing Instructions')
    isLocked = fields.Boolean('Locked')
    
    #Fields For BOM and Invoice Computation
    selectedQuantity = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4')],string="Selected Quantity",default="1")
    selectedRunOn = fields.Integer('Selected Run On',default=0)
    selectedPrice = fields.Float('Total Price Selected',default=0)
    selectedRatio = fields.Float('Ratio Selected',default=0)
    
    def GenerateEnvelopeDetails(self,estimate):
        line = ''
        if estimate.envelope_type:
            line += '%s' % dict(ENVELOPE_TYPES)[estimate.envelope_type]
        if estimate.flap_glue_type:
            line += '\n%s' % dict(FLAP_GLUE_TYPES)[estimate.flap_glue_type]
        if estimate.tissue_lined:
            line += '\n%s' % dict(TISSUE_LINING_OPTIONS)[estimate.tissue_lined]
        if estimate.embossed:
            line += '\nBlind Embossed'
        if estimate.windowed:
            if estimate.standard_window_size:
                line += '\nStandard'
            else:
                line += '\n%s mm  x  %s mm' % (estimate.windowHeight, estimate.windowWidth)
                line += '\n%s mm FLHS,  %s mm Up' % (estimate.windowFlhs, estimate.windowUp)
        return line
    
    @api.model
    def create(self,val):
        val['estimate_number'] = self.env['ir.sequence'].next_by_code('bb_estimate.estimate')
        record = super(Estimate,self).create(val)
        conditions = self.env['bb_estimate.conditions'].sudo().search([('isDefault','=',True)])
        record.estimateConditions = conditions
        return record
    
    @api.depends('hasExtra')
    def getExtras(self):
        for record in self:
            for line in record.estimate_line:
                if line.isExtra:
                    record.hasExtra = True
    
    
    @api.depends('estimate_line')
    def _get_estimate_line(self):
        for record in self:
            #totals
            for qty in ['1','2','3','4','run_on']:
                record['total_price_'+qty] = sum([x['total_price_'+qty] for x in record.estimate_line])
                record['total_cost_'+qty] = sum([x['total_cost_'+qty] for x in record.estimate_line])
                record['total_price_extra_'+qty] = sum([x['total_price_'+qty] for x in record.estimate_line if x.isExtra == True])
                if qty != 'run_on':
                    record['unAllocated_'+qty] = record['quantity_'+qty] - sum([x['param_finished_quantity_'+qty] for x in record.estimate_line if x.option_type == 'material'])
                else:
                    record['unAllocated_'+qty] = record[qty] - sum([x['param_finished_quantity_'+qty] for x in record.estimate_line if x.option_type == 'material'])
                    
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
            customerDeliveryContact = self.env['res.partner'].sudo().search(['&',('parent_id','=',record.partner_id.id),('type','=','contact')])
            if customerDeliveryContact:
                record.DeliveryContact = customerDeliveryContact[0]
            else:
                record.DeliveryContact = record.partner_id
            
            customerDeliveryAddress = self.env['res.partner'].sudo().search(['&',('parent_id','=',record.partner_id.id),('type','=','delivery')])
            if customerDeliveryAddress:
                record.Delivery = customerDeliveryAddress[0]
            
            customer_account_addresses = self.env['res.partner'].sudo().search(['&',('parent_id','=',record.partner_id.id),('type','=','invoice')])
            if customer_account_addresses and not record.invoice_address:
                record.invoice_address = customer_account_addresses[0]
           
            customer_contacts = self.env['res.partner'].sudo().search(['&','&',('parent_id','=',record.partner_id.id),('type','=','contact'),('employeeStatus','=','current')])
            if customer_contacts and not (record.invoice_contact or record.invoice_contact):
                record.invoice_contact = customer_contacts[0]
                
                
    
    @api.onchange('invoice_account')
    def InvoiceAccount(self):
        for records in self:
            customer_account_addresses = self.env['res.partner'].sudo().search(['&',('parent_id','=',records.invoice_account.id),('type','=','invoice')])
            if customer_account_addresses:
                records.invoice_address = customer_account_addresses[0]
            
            customer_contacts = self.env['res.partner'].sudo().search(['&','&',('parent_id','=',records.invoice_account.id),('type','=','contact'),('employeeStatus','=','current')])
            if customer_contacts:
                records.invoice_contact = customer_contacts[0]
                
            
    def CreateManufacturingOrder(self):
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'name': 'Convert',
                'res_model' : 'bb_estimate.wizard_order_convert',
                'type' : 'ir.actions.act_window',
                'context' : "{'default_EstimateId' : active_id}",
                'target' : 'new',
            }

    def AddLineItem(self):
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'name': 'Add New Line',
                'res_model' : 'bb_estimate.estimate_line',
                'type' : 'ir.actions.act_window',
                'context' : "{'default_estimate_id' : active_id,'default_grammage' : %d}"%(self.grammage),
                'target' : 'new',
            }