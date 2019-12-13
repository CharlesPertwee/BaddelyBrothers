# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError
import datetime
from odoo.addons import decimal_precision as dp
from odoo.tools.safe_eval import safe_eval

DIE_SIZES = [
    ('none', ''),
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
    ('none', ''),
    ('full', 'Yes - Fully'),
    ('half', 'Yes - Half'),
    ('unlined', 'Unlined'),
]

class Estimate(models.Model):
    _name = 'bb_estimate.estimate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Estimate'
    _rec_name = 'estimate_number'
    
    
    @api.model
    def _read_group_state(self, stages, domain, order):
        stages = self.env['bb_estimate.stage'].sudo().search([])
        return stages
    
    #Estimate For Fields
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    contact = fields.Many2one('res.partner', string='Contact')
    project = fields.Many2one('project.project', string='Project',required=True,ondelete='restrict')
    invoice_account = fields.Many2one('res.partner', string='Invoice Account')
    
    #Estimate Summary
    title = fields.Char('Title',required=True)
    product_type = fields.Many2one('product.product', string='Product Type',required=True)
    estimate_date = fields.Date('Estimate Date', default= lambda a: datetime.datetime.now().strftime('%Y-%m-%d'))
    estimator = fields.Many2one('res.users','Estimator', default=lambda self: self.env.uid)
    office_copy = fields.Boolean('Office copy')
    estimate_number = fields.Char('Estimate Number')        
    event_date = fields.Date('Event Date')
    target_dispatch_date = fields.Date('Target Dispatch Date', default=lambda self: (datetime.datetime.now() + datetime.timedelta(days=14)).strftime('%Y-%m-%d'))
    
    #Estimate Detailed Screen
    state = fields.Many2one('bb_estimate.stage','State'
                            , ondelete='restrict'
                            , track_visibility='onchange'
                            , index=True
                            , copy=False
                            , group_expand='_read_group_state'
                            , default=lambda self: self.env['bb_estimate.stage'].search([])[0])
    estimate_line = fields.One2many('bb_estimate.estimate_line','estimate_id',string='Estimate Line', copy = True)
    
    #Delievery Details
    Delivery = fields.Many2one('res.partner',string="Delivery To",required=True)
    #DeliveryContact = fields.Many2one('res.partner',string="Delivery Contact",required=True)
    DeliveryMethod = fields.Many2one('delivery.carrier',string="Delivery Method",required=True) #delivery.carrier
    DeliveryLabel = fields.Boolean('Plain Label')
    
    quantity_1 = fields.Integer('Quantity 1')    
    quantity_2 = fields.Integer('Quantity 2')
    quantity_3 = fields.Integer('Quantity 3')
    quantity_4 = fields.Integer('Quantity 4')
    run_on =  fields.Integer('Run on')
    
    total_price_1 = fields.Float('Total Price 1',digits=(10,2),store=True,copy=True)
    total_price_2 = fields.Float('Total Price 2',digits=(10,2),store=True,copy=True)
    total_price_3 = fields.Float('Total Price 3',digits=(10,2),store=True,copy=True)
    total_price_4 = fields.Float('Total Price 4',digits=(10,2),store=True,copy=True)
    total_price_run_on = fields.Float('Run On',digits=(10,2),store=True,copy=True)
    
    total_price_extra_1 = fields.Float('Total Extra Price 1',digits=(10,2),store=True,compute="_get_estimate_line")
    total_price_extra_2 = fields.Float('Total Extra Price 2',digits=(10,2),store=True,compute="_get_estimate_line")
    total_price_extra_3 = fields.Float('Total Extra Price 3',digits=(10,2),store=True,compute="_get_estimate_line")
    total_price_extra_4 = fields.Float('Total Extra Price 4',digits=(10,2),store=True,compute="_get_estimate_line")
    total_price_extra_run_on = fields.Float('Extra Run On',digits=(10,2),store=True,compute="_get_estimate_line")
    
    total_price_1000_1 = fields.Float('Total Price 1000 1',digits=(10,2),store=True,copy=False)
    total_price_1000_2 = fields.Float('Total Price 1000 2',digits=(10,2),store=True,copy=False)
    total_price_1000_3 = fields.Float('Total Price 1000 3',digits=(10,2),store=True,copy=False)
    total_price_1000_4 = fields.Float('Total Price 1000 4 ',digits=(10,2),store=True,copy=False)
    total_price_1000_run_on = fields.Float('Total Price 1000 Run On',digits=(10,2),store=True,copy=False)
    
    total_cost_1 = fields.Float('Total Cost 1',store=True,compute="_get_estimate_line",digits=(10,2),copy=False)
    total_cost_2 = fields.Float('Total Cost 2',store=True,compute="_get_estimate_line",digits=(10,2),copy=False)
    total_cost_3 = fields.Float('Total Cost 3',store=True,compute="_get_estimate_line",digits=(10,2),copy=False)
    total_cost_4 = fields.Float('Total Cost 4',store=True,compute="_get_estimate_line",digits=(10,2),copy=False)
    total_cost_run_on = fields.Float('Run On',store=True,compute="_get_estimate_line",digits=(10,2),copy=False)
    
    unAllocated_1 = fields.Integer('Un Allocated Quantity 1',store=True,compute="_get_estimate_line")
    unAllocated_2 = fields.Integer('Un Allocated Quantity 1',store=True,compute="_get_estimate_line")
    unAllocated_3 = fields.Integer('Un Allocated Quantity 1',store=True,compute="_get_estimate_line")
    unAllocated_4 = fields.Integer('Un Allocated Quantity 1',store=True,compute="_get_estimate_line")
    unAllocated_run_on = fields.Integer('Un Allocated Quantity 1',store=True,compute="_get_estimate_line")
    
    nett_value_1 = fields.Float('Nett Value',digits=(10,2),copy=False) 
    nett_value_2 = fields.Float('Nett Value 1',digits=(10,2),copy=False)
    nett_value_3 = fields.Float('Nett Value 3',digits=(10,2),copy=False)
    nett_value_4 = fields.Float('Nett Value 4',digits=(10,2),copy=False)

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
    windowHeight = fields.Float('Window Size: Height (mm)',digits=(10,2))
    windowWidth = fields.Float('Window Size:Widht (mm)',digits=(10,2))
    windowFlhs = fields.Float('Window Pos: FLHS',digits=(10,2))
    windowUp = fields.Float('Window Pos: Up',digits=(10,2))
    
    routings = fields.Many2one('mrp.routing','Generated Routing',copy=False)
    bom = fields.Many2one('mrp.bom', 'Generated BOM',copy=False)
    manufacturingOrder = fields.Many2one('mrp.production','Job Ticket',copy=False)
    salesOrder = fields.Many2one('sale.order','Sales Order',copy=False)
    
    hasExtra = fields.Boolean('Has Extra',compute="getExtras")
    estimateConditions = fields.Many2many('bb_estimate.conditions', string="Estimate Conditions", copy=True)
    isEnvelope = fields.Boolean('Is Envelope',related="product_type.isEnvelope")
    showMo = fields.Boolean('Show Mo Button',related="state.isOrder")
    EnquiryComments = fields.Text('Enquiry Comments')
    SpecialInstuction = fields.Text('Special Instructions')
    #PackingInstruction = fields.Text('Packing Instructions')
    isLocked = fields.Boolean('Locked',copy=False)
    hasDelivery = fields.Boolean('Delivery Added?',copy=False)
    priceHistory = fields.One2many('bb_estimate.price_history','Estimate','Price Adjustments',copy=True)
    
    #Fields For BOM and Invoice Computation
    selectedQuantity = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4')],string="Selected Quantity",default="1",copy=False)
    selectedRunOn = fields.Integer('Selected Run On',default=0,copy=False)
    selectedPrice = fields.Float('Total Price Selected',default=0,copy=False)
    selectedRatio = fields.Float('Ratio Selected',default=0,copy=False)
    SelectedQtyRatio = fields.Float('Ratio Selected',default=1,copy=False)
    
    duplicateProcess = fields.Boolean('Process Duplicate',default=False)
    
    Weight_1 = fields.Float('Weight 1',copy=False)
    Weight_2 = fields.Float('Weight 2',copy=False)
    Weight_3 = fields.Float('Weight 3',copy=False)
    Weight_4 = fields.Float('Weight 4',copy=False)
    Weight_run_on = fields.Float('Weight Run On',copy=False)
    
    lead = fields.Many2one('crm.lead','Enquiry',copy=True)
    reSyncCount = fields.Integer('Re Sync Count',compute='_compute_reSync')
    
    ChangeLog = fields.Html("Change Log")
    
    AppendLog = fields.Boolean('Append Log')

    analytic_account = fields.Many2one('account.analytic.account','Analytic Account')
    
    def _compute_reSync(self):
        for record in self:
            record.reSyncCount = len([x for x in record.estimate_line if x.reSync])
            
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
            if estimate.standardWindowSize:
                line += '\nStandard'
            else:
                line += '\n%s mm  x  %s mm' % (estimate.windowHeight, estimate.windowWidth)
                line += '\n%s mm FLHS,  %s mm Up' % (estimate.windowFlhs, estimate.windowUp)
        return line
    
    @api.multi
    def copy(self,default=None):

        record = {
            'partner_id': self.partner_id.id  if self.partner_id else False,
            "contact": self.contact.id  if self.contact else False,
            'project': self.project.id if self.project else False,
            'invoice_account': self.invoice_account.id if self.invoice_account else False,
            'title' : '%s (Copy)'%(self.title),
            'product_type' : self.product_type.id if self.product_type else False,
            'estimate_date' : self.estimate_date,
            'estimator' : self.estimator.id if self.estimator else False,
            'office_copy' : self.office_copy,
            'estimate_number' : self.env['ir.sequence'].next_by_code('bb_estimate.estimate'),
            'event_date' : self.event_date,
            'target_dispatch_date' : self.target_dispatch_date,
            'Delivery' : self.Delivery.id if self.Delivery else False,
            'DeliveryMethod': self.DeliveryMethod.id if self.DeliveryMethod else False,
            'DeliveryLabel' : self.DeliveryLabel,
            'quantity_1' : self.quantity_1,
            'quantity_2': self.quantity_2,
            'quantity_3': self.quantity_3,
            'quantity_4': self.quantity_4,
            'run_on' : self.run_on,
            'total_price_1' : self.total_price_1,
            'total_price_2' : self.total_price_2,
            'total_price_3' : self.total_price_3,
            'total_price_4' : self.total_price_4,
            'total_price_run_on' : self.total_price_run_on,
            'total_price_extra_1' : self.total_price_extra_1,
            'total_price_extra_2' : self.total_price_extra_2,
            'total_price_extra_3' : self.total_price_extra_3,
            'total_price_extra_4' : self.total_price_extra_4,
            'total_price_extra_run_on' : self.total_price_extra_run_on,
            'total_price_1000_1' : self.total_price_1000_1,
            'total_price_1000_2' : self.total_price_1000_2,
            'total_price_1000_3' : self.total_price_1000_3,
            'total_price_1000_4' : self.total_price_1000_4,
            'total_price_1000_run_on' : self.total_price_1000_run_on,
            'total_cost_1' : self.total_cost_1,
            'total_cost_2' : self.total_cost_2,
            'total_cost_3' : self.total_cost_3,
            'total_cost_4' : self.total_cost_4,
            'total_cost_run_on' : self.total_cost_run_on,
            'unAllocated_1' : self.unAllocated_1,
            'unAllocated_2' : self.unAllocated_2,
            'unAllocated_3' : self.unAllocated_3,
            'unAllocated_4' : self.unAllocated_4,
            'unAllocated_run_on' : self.unAllocated_run_on,
            'nett_value_1' : self.nett_value_1,
            'nett_value_2' : self.nett_value_2,
            'nett_value_3' : self.nett_value_3,
            'nett_value_4' : self.nett_value_4,
            'number_up' : self.number_up,
            'grammage' : self.grammage,
            'finished_size' : self.finished_size.id if self.finished_size else False,
            'finished_width' : self.finished_width,
            'finished_height' : self.finished_height,
            'working_size' : self.working_size.id if self.working_size else False,
            'working_width' : self.working_width,
            'working_height' : self.working_height,
            'knife_number' : self.knife_number,
            'envelope_type' : self.envelope_type,
            'flap_glue_type' : self.flap_glue_type,
            'tissue_lined' : self.tissue_lined,
            'knife_number' : self.knife_number,
            'embossed' : self.embossed,
            'windowed' : self.windowed,
            'standardWindowSize': self.standardWindowSize,
            'windowHeight' : self.windowHeight,
            'windowWidth' : self.windowWidth,
            'windowFlhs' : self.windowFlhs,
            'windowUp' : self.windowUp,
            'routings' : False,
            'bom' : False,
            'manufacturingOrder' : False,
            'salesOrder' : False,
            'isEnvelope' : self.isEnvelope,
            'showMo' : False,
            'EnquiryComments' : self.EnquiryComments,
            'SpecialInstuction' : self.SpecialInstuction,
            'isLocked' : False,
            'hasDelivery' : self.hasDelivery,
            'Weight_1' : self.Weight_1,
            'Weight_2' : self.Weight_2,
            'Weight_3' : self.Weight_3,
            'Weight_4' : self.Weight_4,
            'Weight_run_on' : self.Weight_run_on,
            'lead' : self.lead.id if self.lead else False,
            'analytic_account': self.analytic_account.id if self.analytic_account else False,
            'priceHistory': [(0,0,
                              {
                                'CurrentPrice1': x.ChangedPrice1,
                                'CurrentPrice2': x.CurrentPrice2,
                                'CurrentPrice3': x.CurrentPrice3,
                                'CurrentPrice4': x.CurrentPrice4,
                                'CurrentPriceRunOn': x.CurrentPriceRunOn,
                                'ChangedPrice1': x.ChangedPrice1,
                                'ChangedPrice2': x.ChangedPrice2,
                                'ChangedPrice3': x.ChangedPrice3,
                                'ChangedPrice4': x.ChangedPrice4,
                                'ChangedPriceRunOn': x.ChangedPriceRunOn,
                                'SalesOrder': False
                              }) for x in self.priceHistory]
            
        }

        estimate = super(Estimate,self).create(record)
        

        for x in self.estimate_line:
            line = {
                'workcenterId': x.workcenterId.id if x.workcenterId else False,
                'material': x.material.id if x.material else False,
                'estimate_id' : estimate.id,
                'isEnvelope' : x.isEnvelope,
                'isExtra' : x.isExtra,
                'extraDescription' : x.extraDescription,
                'lineName' : x.lineName,
                'customer_description': x.customer_description,
                'documentCatergory' : x.documentCatergory,
                'JobTicketText' : x.JobTicketText,
                'StandardCustomerDescription' : x.StandardCustomerDescription,
                'StandardJobDescription' : x.StandardJobDescription,
                'UseStadandardDescription' : x.UseStadandardDescription,
                'Details' : x.Details,
                'EstimatorNotes' : x.EstimatorNotes,
                'quantity_1' : x.quantity_1,
                'quantity_2' : x.quantity_2,
                'quantity_3' : x.quantity_3,
                'quantity_4' : x.quantity_4,
                'run_on' : x.run_on,
                'param_make_ready_time_1' : x.param_make_ready_time_1,
                'param_make_ready_time_2' : x.param_make_ready_time_2,
                'param_make_ready_time_3' : x.param_make_ready_time_3,
                'param_make_ready_time_4' : x.param_make_ready_time_4,
                'param_make_ready_time_run_on' : x.param_make_ready_time_run_on,
                'req_param_make_ready_time' : x.req_param_make_ready_time,
                'param_machine_speed_1' : x.param_machine_speed_1,
                'param_machine_speed_2' : x.param_machine_speed_2,
                'param_machine_speed_3' : x.param_machine_speed_3,
                'param_machine_speed_4' : x.param_machine_speed_4,
                'param_machine_speed_run_on' : x.param_machine_speed_run_on,
                'req_param_machine_speed' : x.req_param_machine_speed,
                'param_running_time_1' : x.param_running_time_1,
                'param_running_time_2' : x.param_running_time_2,
                'param_running_time_3' : x.param_running_time_3,
                'param_running_time_4' : x.param_running_time_4,
                'param_running_time_run_on' : x.param_running_time_run_on,
                'req_param_running_time' : x.req_param_running_time,
                'param_wash_up_time_1' : x.param_wash_up_time_1,
                'param_wash_up_time_2' : x.param_wash_up_time_2,
                'param_wash_up_time_3' : x.param_wash_up_time_3,
                'param_wash_up_time_4' : x.param_wash_up_time_4,
                'param_wash_up_time_run_on' : x.param_wash_up_time_run_on,
                'req_param_wash_up_time' : x.req_param_wash_up_time,
                'param_make_ready_overs_1' : x.param_make_ready_overs_1,
                'param_make_ready_overs_2' : x.param_make_ready_overs_2,
                'param_make_ready_overs_3' : x.param_make_ready_overs_3,
                'param_make_ready_overs_4' : x.param_make_ready_overs_4,
                'param_make_ready_overs_run_on' : x.param_make_ready_overs_run_on,
                'req_param_make_ready_overs' : x.req_param_make_ready_overs,
                'param_running_overs_percent_1' : x.param_running_overs_percent_1,
                'param_running_overs_percent_2' : x.param_running_overs_percent_2,
                'param_running_overs_percent_3' : x.param_running_overs_percent_3,
                'param_running_overs_percent_4' : x.param_running_overs_percent_4,
                'param_running_overs_percent_run_on' : x.param_running_overs_percent_run_on,
                'req_param_running_overs_percent' : x.req_param_running_overs_percent,
                'unallocated_finished_quantity_1' : x.unallocated_finished_quantity_1,
                'unallocated_finished_quantity_2' : x.unallocated_finished_quantity_2,
                'unallocated_finished_quantity_3' : x.unallocated_finished_quantity_3,
                'unallocated_finished_quantity_4' : x.unallocated_finished_quantity_4,
                'unallocated_finished_quantity_run_on' : x.unallocated_finished_quantity_run_on,
                'req_unallocated_finished_quantity' : x.req_unallocated_finished_quantity,
                'param_finished_quantity_1' : x.param_finished_quantity_1,
                'param_finished_quantity_2' : x.param_finished_quantity_2,
                'param_finished_quantity_3' : x.param_finished_quantity_3,
                'param_finished_quantity_4' : x.param_finished_quantity_4,
                'param_finished_quantity_run_on' : x.param_finished_quantity_run_on,
                'req_param_finished_quantity' : x.req_param_finished_quantity,
                'quantity_required_1' : x.quantity_required_1,
                'quantity_required_2' : x.quantity_required_2,
                'quantity_required_3' : x.quantity_required_3,
                'quantity_required_4' : x.quantity_required_4,
                'quantity_required_run_on' : x.quantity_required_run_on,
                'req_quantity_required' : x.req_quantity_required,
                'cost_per_unit_1' : x.cost_per_unit_1,
                'cost_per_unit_2' : x.cost_per_unit_2,
                'cost_per_unit_3' : x.cost_per_unit_3,
                'cost_per_unit_4' : x.cost_per_unit_4,
                'cost_per_unit_run_on' : x.cost_per_unit_run_on,
                'req_cost_per_unit' : x.req_cost_per_unit,
                'price_per_unit_1' : x.price_per_unit_1,
                'price_per_unit_2' : x.price_per_unit_2,
                'price_per_unit_3' : x.price_per_unit_3,
                'price_per_unit_4' : x.price_per_unit_4,
                'price_per_unit_run_on' : x.price_per_unit_run_on,
                'req_price_per_unit' : x.req_price_per_unit,
                'margin_1' : x.margin_1,
                'margin_2' : x.margin_2,
                'margin_3' : x.margin_3,
                'margin_3' : x.margin_3,
                'margin_4' : x.margin_4,
                'margin_run_on' : x.margin_run_on,
                'req_margin' : x.req_margin,
                'total_cost_1' : x.total_cost_1,
                'total_cost_2' : x.total_cost_2,
                'total_cost_3' : x.total_cost_3,
                'total_cost_4' : x.total_cost_4,
                'total_cost_run_on' : x.total_cost_run_on,
                'req_total_cost' : x.req_total_cost,
                'mat_charge_1' : x.mat_charge_1,
                'mat_charge_2' : x.mat_charge_2,
                'mat_charge_3' : x.mat_charge_3,
                'mat_charge_4' : x.mat_charge_4,
                'mat_charge_run_on' : x.mat_charge_run_on,
                'req_mat_charge' : x.req_mat_charge,
                'total_price_1' : x.total_price_1,
                'total_price_2' : x.total_price_2,
                'total_price_3' : x.total_price_3,
                'total_price_4' : x.total_price_4,
                'total_price_run_on' : x.total_price_run_on,
                'req_total_price' : x.req_total_price,
                'total_price_per_1000_1' : x.total_price_per_1000_1,
                'total_price_per_1000_2' : x.total_price_per_1000_2,
                'total_price_per_1000_3' : x.total_price_per_1000_3,
                'total_price_per_1000_4' : x.total_price_per_1000_4,
                'total_price_per_1000_run_on' : x.total_price_per_1000_run_on,
                'req_total_price_per_1000' : x.req_total_price_per_1000,
                'option_type' : x.option_type,
                'param_finished_size' : x.param_finished_size.id if x.param_finished_size else False,
                'param_finished_width' : x.param_finished_width,
                'param_finished_height' : x.param_finished_height,
                'param_working_size' : x.param_working_size.id if x.param_working_size else False,
                'param_working_width' : x.param_working_width,
                'param_working_height' : x.param_working_height,
                'param_knife_number' : x.param_knife_number,
                'process_working_sheets_quantity_1' : x.process_working_sheets_quantity_1,
                'process_working_sheets_quantity_2' : x.process_working_sheets_quantity_2,
                'process_working_sheets_quantity_3' : x.process_working_sheets_quantity_3,
                'process_working_sheets_quantity_4' : x.process_working_sheets_quantity_4,
                'process_working_sheets_quantity_run_on' : x.process_working_sheets_quantity_run_on,
                'req_process_working_sheets_quantity' : x.req_process_working_sheets_quantity,
                'process_overs_quantity_1' : x.process_overs_quantity_1,
                'process_overs_quantity_2' : x.process_overs_quantity_2,
                'process_overs_quantity_3' : x.process_overs_quantity_3,
                'process_overs_quantity_4' : x.process_overs_quantity_4,
                'process_overs_quantity_run_on' : x.process_overs_quantity_run_on,
                'req_process_overs_quantity' : x.req_process_overs_quantity,
                'MaterialTypes' : x.MaterialTypes,
                'SheetHeight' : x.SheetHeight,
                'SheetWidth' : x.SheetWidth,
                'WhiteCutting' : x.WhiteCutting.id if x.WhiteCutting else False,
                'PrintedCutting' : x.PrintedCutting.id if x.PrintedCutting else False,
                'NoWhiteCuts' : x.NoWhiteCuts,
                'NoPrintedCuts' : x.NoPrintedCuts,
                'NonStockMaterialType' : x.NonStockMaterialType,
                'MaterialName' : x.MaterialName,
                'SheetSize' : x.SheetSize.id if x.SheetHeight else False,
                'PurchaseUnit' : x.PurchaseUnit.id if x.PurchaseUnit else False,
                'Supplier' : x.Supplier.id if x.Supplier else False,
                'MinimumQty' : x.MinimumQty,
                'PackSize' : x.PackSize,
                'CostRate' : x.CostRate,
                'CharegeRate' : x.CharegeRate,
                'Margin' : x.Margin,
                'Sequence' : x.Sequence,
                'hasComputed' : x.hasComputed,
                'reSync' : x.reSync,
                'generatesPO' : x.generatesPO,
                'param_supplier' : x.param_supplier.id if x.param_supplier else False,
                'req_param_supplier' : x.req_param_supplier,
                'param_material_vendor' : x.param_material_vendor.id if x.param_material_vendor else False,
                'req_param_material_vendor' : x.req_param_material_vendor,
                'param_number_up' : x.param_number_up,
                'req_param_number_up' : x.req_param_number_up,
                'param_number_out' : x.param_number_out,
                'req_param_number_out' : x.req_param_number_out,
                'param_number_of_colors' : x.param_number_of_colors,
                'req_param_number_of_colors' : x.req_param_number_of_colors,
                'param_number_of_colors_rev' : x.param_number_of_colors_rev,
                'req_param_number_of_colors_rev' : x.req_param_number_of_colors_rev,
                'work_twist' : x.work_twist,
                'req_work_twist' : x.req_work_twist,
                'grammage' : x.grammage,
                'req_grammage' : x.req_grammage,
                'param_no_of_ink_mixes' : x.param_no_of_ink_mixes,
                'req_param_no_of_ink_mixes' : x.req_param_no_of_ink_mixes,
                'param_additional_charge' : x.param_additional_charge,
                'req_param_additional_charge': x.req_param_additional_charge,
                'param_misc_charge_per_cm2' : x.param_misc_charge_per_cm2,
                'req_param_misc_charge_per_cm2' : x.req_param_misc_charge_per_cm2,
                'param_misc_charge_per_cm2_area' : x.param_misc_charge_per_cm2_area,
                'req_param_misc_charge_per_cm2_area' : x.req_param_misc_charge_per_cm2_area,
                'param_die_size' : x.param_die_size,
                'req_param_die_size' : x.req_param_die_size,
                'param_printed_material' : x.param_printed_material,
                'req_param_printed_material': x.req_param_printed_material,
                'param_duplex_sheets' : x.param_duplex_sheets,
                'req_param_duplex_sheets' : x.req_param_duplex_sheets,
                'param_number_of_sheets' : x.param_number_of_sheets,
                'req_param_number_of_sheets' : x.req_param_number_of_sheets,
                'param_sheets_per_box' : x.param_sheets_per_box,
                'req_param_sheets_per_box' : x.req_param_sheets_per_box,
                'param_time_per_box' : x.param_time_per_box,
                'req_param_time_per_box' : x.req_param_time_per_box,
                'param_number_of_cuts' : x.param_number_of_cuts,
                'req_param_number_of_cuts' : x.req_param_number_of_cuts,
                'param_sheets_per_pile' : x.param_sheets_per_pile,
                'req_param_sheets_per_pile' : x.req_param_sheets_per_pile,
                'param_time_per_pile' : x.param_time_per_pile,
                'req_param_time_per_pile' : x.req_param_time_per_pile,
                'param_env_windowpatching' : x.param_env_windowpatching,
                'req_param_env_windowpatching' : x.req_param_env_windowpatching,
                'param_env_peelandstick' : x.param_env_peelandstick,
                'req_param_env_peelandstick' : x.req_param_env_peelandstick,
                'param_env_inlineemboss' : x.param_env_inlineemboss,
                'req_param_env_inlineemboss' : x.req_param_env_inlineemboss,
                'req_param_env_gumming' : x.req_param_env_gumming,
                'param_material_line_id' : x.param_material_line_id.id if x.param_material_line_id else False,
                'req_param_material_line_id' : x.req_param_material_line_id,
               }
            estimate_line = self.env['bb_estimate.estimate_line'].duplicate(line)
           

            # for y in x.material_ids:
            #     self.env['bb_estimate.material_link'].duplicate({
            #                                                         'estimate' : estimate.id,
            #                                                         'materialLine': estimate_line.id,
            #                                                     })
        oldIndexedLines = [x.id for x in self.estimate_line]
        newIndexedLines = [x.id for x in estimate.estimate_line]

        for line in self.estimate_line:
            for x in line.material_ids:
                self.env['bb_estimate.material_link'].duplicate({
                                                                'estimate' : estimate.id,
                                                                'processLine' : newIndexedLines[oldIndexedLines.index(x.processLine.id)],
                                                                'materialLine': newIndexedLines[oldIndexedLines.index(x.materialLine.id)],
                                                            })
        
        estimate.estimateConditions = self.estimateConditions
        return estimate

    
    @api.model
    def create(self,val):
        val['estimate_number'] = self.env['ir.sequence'].next_by_code('bb_estimate.estimate')
        record = super(Estimate,self).create(val)
        conditions = self.env['bb_estimate.conditions'].sudo().search([('isDefault','=',True)])
        record.estimateConditions = conditions if not record.estimateConditions else record.estimateConditions
        return record
    
    @api.multi
    def write(self,vals):
        old = {x.id:[x['lineName'],x['quantity_required_1'],x['quantity_required_2'],x['quantity_required_3'],x['quantity_required_4'],x['quantity_required_run_on']] for x in self.estimate_line}
        currentRecord = super(Estimate, self).write(vals)
        new = {x.id:[x['lineName'],x['quantity_required_1'],x['quantity_required_2'],x['quantity_required_3'],x['quantity_required_4'],x['quantity_required_run_on']] for x in self.estimate_line}
        
        changedRecords = [[new[x][0],old[x][1],new[x][1],old[x][2],new[x][2],old[x][3],new[x][3],old[x][4],new[x][4],old[x][5],new[x][5]] for x in filter(lambda x: old[x] != new[x], new.keys())]
#         changedRecords = ['%s - Qty1 %0.2f to %0.2f Qty2 %0.2f to %0.2f Qty3 %0.2f to %0.2f Qty4 %0.2f to %0.2f Qty Run On %0.2f to %0.2f'
#                             %(new[x][0],old[x][1],new[x][1],old[x][2],new[x][2],old[x][3],new[x][3],old[x][4],new[x][4],old[x][5],new[x][5]) 
#                             for x in filter(lambda x: old[x] != new[x], new.keys())]
        #raise Exception(old,new,changedRecords)
        
        update_vals = {}
        if 'estimate_line' in vals.keys():
            values = {
                'lines': changedRecords
                }
            body = self.env.ref('bb_estimate.change_log').render(values=values)
            update_vals = { 'ChangeLog': body }
        else:
            update_vals = { 'ChangeLog': '' }
            
        if 'total_price_1' in vals.keys():
            self.lead.write({'planned_revenue':vals['total_price_1']})
            
        
        currentRecord = super(Estimate, self).write(update_vals)
        #raise Exception(old,new)
        return currentRecord
        
    
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
                record['total_cost_'+qty] = sum([x['total_cost_'+qty] for x in record.estimate_line])
                record['total_price_extra_'+qty] = sum([x['total_price_'+qty] for x in record.estimate_line if x.isExtra == True])
                
                if qty != 'run_on':
                    record['unAllocated_'+qty] = record['quantity_'+qty] - sum([x['param_finished_quantity_'+qty] for x in record.estimate_line if x.option_type == 'material'])
                else:
                    record['unAllocated_'+qty] = record[qty] - sum([x['param_finished_quantity_'+qty] for x in record.estimate_line if x.option_type == 'material'])
                    
            record.hasDelivery = len(record.estimate_line.filtered(lambda x: x.documentCatergory == 'Despatch')) > 0
    
    @api.onchange('materialInfo')
    def ShowChangedLines(self):
        pass
    
    @api.onchange('finished_size')
    def finished_size_change(self):
        for record in self:
            if record.finished_size.width:
                record.finished_width = record.finished_size.width
            if record.finished_size.height:
                record.finished_height = record.finished_size.height
            if record.finished_size.isEnvelopeEstimate:
                record.knife_number = record.finished_size.knifeNumber
                
    @api.onchange('working_size')
    def working_size_change(self):
        for record in self:
            if record.working_size.isEnvelopeEstimate:
                if record.working_size.flatWidth:
                    record.working_width = record.working_size.flatWidth
                if record.working_size.flatHeight:
                    record.working_height = record.working_size.flatHeight
                record.knife_number = record.working_size.knifeNumber
            else:
                if record.working_size.width:
                    record.working_width = record.working_size.width
                if record.working_size.height:
                    record.working_height = record.working_size.height
    
    
    @api.onchange('partner_id')
    def PartnerUpdate(self):
        """
        Update the following fields when the partner is changed:
        - Invoice address
        - Delivery address
        """
        if not self.partner_id:
            self.update({
                'contact': False,
                'invoice_account': False,
                'Delivery': False
            })
            return

        addr = self.partner_id.address_get(['delivery', 'invoice','contact'])
        values = {
            'contact': addr['contact'],
            'invoice_account': addr['invoice'],
            'Delivery': addr['delivery'],
        }
        self.update(values)
    
    @api.onchange('state')            
    def _computeLeadState(self):
        if self.state:
            if self.state.LeadStage and self.lead:
                self.lead.write({'stage_id':self.state.LeadStage.id})
    
#     @api.onchange('invoice_account')
#     def InvoiceAccount(self):
#         for record in self:
#             if record.invoice_account:
#                 customer_account_addresses = self.env['res.partner'].sudo().search(['&',('parent_id','=',record.invoice_account.id),('type','=','invoice')])
#                 if customer_account_addresses:
#                     record.invoice_address = customer_account_addresses[0]

#                 customer_contacts = self.env['res.partner'].sudo().search(['&','&',('parent_id','=',record.invoice_account.id),('type','=','contact'),('employeeStatus','=','current')])
#                 if customer_contacts:
#                     record.invoice_contact = customer_contacts[0]

            
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
    def AmmendQty(self):
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'name': 'Ammend Qty',
                'res_model' : 'bb_estimate.wizard_amend_qty',
                'type' : 'ir.actions.act_window',
                'context' : "{'default_EstimateId' : active_id}",
                'target' : 'new',
            }
    def AddLineItem(self):
        self.duplicateProcess = False
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'name': 'Add New Line',
                'res_model' : 'bb_estimate.estimate_line',
                'type' : 'ir.actions.act_window',
                'context' : "{'default_estimate_id' : active_id,'default_grammage' : %d,'default_param_number_up' : %d}"%(self.grammage,self.number_up),
                'target' : 'new',
            }
    
    def AdjustPrice(self):
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'name': 'Adjust Price',
                'res_model' : 'bb_estimate.adjust_price',
                'type' : 'ir.actions.act_window',
                'context' : "{'default_Estimate' : active_id}",
                'target' : 'new',
            }
  
    def _match_address(self,carrier, partner):
        self.ensure_one()
        if carrier.country_ids and partner.country_id not in carrier.country_ids:
            return False
        if carrier.state_ids and partner.state_id not in carrier.state_ids:
            return False
        if carrier.zip_from and (partner.zip or '').upper() < carrier.zip_from.upper():
            return False
        if carrier.zip_to and (partner.zip or '').upper() > carrier.zip_to.upper():
            return False
        return True
    
    def _get_price_from_picking(self,carrier, total, weight, volume, quantity):
        price = 0.0
        criteria_found = False
        price_dict = {'price': total, 'volume': volume, 'weight': weight, 'wv': volume * weight, 'quantity': quantity}
        for line in carrier.price_rule_ids:
            test = safe_eval(line.variable + line.operator + str(line.max_value), price_dict)
            if test:
                price = line.list_base_price + line.list_price * price_dict[line.variable_factor]
                criteria_found = True
                break
        if not criteria_found:
            raise UserError(_("No price rule matching this order; delivery cost cannot be computed."))

        return price
    
    def _get_price_available(self,carrier,qty):
        self.ensure_one()
        total = weight = volume = quantity = 0
        total_delivery = 0.0
        for line in self.estimate_line:
            total_delivery += line['total_price_'+qty]
            lineQuantity = line['quantity_required_'+qty]
            weight += self.LineWeight(line,qty)
            volume += (line.material.volume or 0.0) * lineQuantity
            quantity += lineQuantity
        total = total_delivery

        return self._get_price_from_picking(carrier,total, weight, volume, quantity)
    
    def GetWeight(self,qty):
        self.ensure_one()
        weight = 0
        for line in self.estimate_line:
            weight += self.LineWeight(line,qty)
        return weight
    
    def AddDelivery(self):
        prices = {}
        for qty in ['1','2','3','4','run_on']:
            quantity = 0
            if qty == 'run_on':
                quantity = self.run_on
            else:
                quantity = self['quantity_'+qty]
            if quantity > 0:
                carrier = self._match_address(self.DeliveryMethod,self.Delivery)
                if carrier:
                    price_unit = self._get_price_available(self.DeliveryMethod,qty)
                    prices['qty_'+qty] = price_unit
                else:
                    prices['qty_'+qty] = 0.0
                    raise UserError(_('Shipping address not valid for selected delivery method.'))
            else:
                prices['qty_'+qty] = 0.0
        newLine = self.env['bb_estimate.estimate_line'].create(
            {
                'material': self.DeliveryMethod.product_id.id,
                'estimate_id': self.id,
                'lineName': self.DeliveryMethod.product_id.name,
                'option_type':'material',
                'MaterialTypes':'Stock',
                'customer_description': self.DeliveryMethod.product_id.customerDescription,
                'documentCatergory': 'Despatch',
                'JobTicketText': self.DeliveryMethod.product_id.jobTicketDescription,
                'StandardCustomerDescription': self.DeliveryMethod.product_id.customerDescription,
                'StandardJobDescription': self.DeliveryMethod.product_id.jobTicketDescription,
                'quantity_required_1': 1 if self.quantity_1 > 0 else 0,
                'quantity_required_2': 1 if self.quantity_2 > 0 else 0,
                'quantity_required_3': 1 if self.quantity_3 > 0 else 0,
                'quantity_required_4': 1 if self.quantity_4 > 0 else 0,
                'quantity_required_run_on': 1 if self.run_on > 0 else 0,
                'cost_per_unit_1': prices['qty_1'],
                'cost_per_unit_2': prices['qty_2'],
                'cost_per_unit_3': prices['qty_3'],
                'cost_per_unit_4': prices['qty_4'],
                'cost_per_unit_run_on': prices['qty_run_on'],
                'price_per_unit_1': prices['qty_1'] * (1.0 + (float(self.DeliveryMethod.margin) / 100.0)),
                'price_per_unit_2': prices['qty_2'] * (1.0 + (float(self.DeliveryMethod.margin) / 100.0)),
                'price_per_unit_3': prices['qty_3'] * (1.0 + (float(self.DeliveryMethod.margin) / 100.0)),
                'price_per_unit_4': prices['qty_4'] * (1.0 + (float(self.DeliveryMethod.margin) / 100.0)),
                'price_per_unit_run_on': prices['qty_run_on'],
                'margin_1': self.DeliveryMethod.margin,
                'margin_2': self.DeliveryMethod.margin,
                'margin_3': self.DeliveryMethod.margin,
                'margin_4': self.DeliveryMethod.margin,
                'margin_run_on': self.DeliveryMethod.margin,
                'total_cost_1': prices['qty_1'],
                'total_cost_2': prices['qty_2'],
                'total_cost_3': prices['qty_3'],
                'total_cost_4': prices['qty_4'],
                'total_cost_run_on': prices['qty_run_on'],
                'total_price_1': prices['qty_1'] * (1.0 + (float(self.DeliveryMethod.margin) / 100.0)),
                'total_price_2': prices['qty_2'] * (1.0 + (float(self.DeliveryMethod.margin) / 100.0)),
                'total_price_3': prices['qty_3'] * (1.0 + (float(self.DeliveryMethod.margin) / 100.0)),
                'total_price_4': prices['qty_4'] * (1.0 + (float(self.DeliveryMethod.margin) / 100.0)),
                'total_price_run_on': prices['qty_run_on'],
                'hasDelivery': True
                
            })
        self.write(
                {
                    'Weight_1': self.GetWeight('1'),
                    'Weight_2': self.GetWeight('2'),
                    'Weight_3': self.GetWeight('3'),
                    'Weight_4': self.GetWeight('4'),
                    'Weight_run_on': self.GetWeight('run_on')
                })
        self.message_post(body="Delivery Added %s"%(self.DeliveryMethod.name))

    def LineWeight(self,line, qty):
        # return the weight of the specified estimate line for the specified quantity
        if line.material.productType in ['Stock','Trade Counter']:
            if line['quantity_required_'+qty] and line.material.sheet_width and line.material.sheetSize and line.material.grammage:
                kg_per_sheet =  (float(line.material.sheet_width) / 1000.0) * (float(line.material.sheet_height) / 1000.0) * (float(line.material.grammage) / 1000.0)
                total_weight = float(line['quantity_required_'+qty]) * kg_per_sheet
                return total_weight
            else:
                return 0.0
        elif line.material.productType in ['Package']:
            return line.material.weight or 0.0
        else:
            return 0.0
        
    def EstimateLetter(self):
        return { 
                'type': 'ir.actions.act_url',
                'url': '/bb_estimate/bb_estimate/estimateLetter/%s' % self.id,
                'target': 'new',
                'res_id': self.id,
               }       
    
