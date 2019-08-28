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
    _rec_name = 'title'
    
    
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
    estimateConditions = fields.Many2many('bb_estimate.conditions', string="Estimate Conditions")
    isEnvelope = fields.Boolean('Is Envelope',related="product_type.isEnvelope")
    showMo = fields.Boolean('Show Mo Button',related="state.isOrder")
    EnquiryComments = fields.Text('Enquiry Comments')
    SpecialInstuction = fields.Text('Special Instructions')
    #PackingInstruction = fields.Text('Packing Instructions')
    isLocked = fields.Boolean('Locked',copy=False)
    hasDelivery = fields.Boolean('Delivery Added?',copy=False)
    priceHistory = fields.One2many('bb_estimate.price_history','Estimate','Price Adjustments',copy=False)
    
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
    
    lead = fields.Many2one('crm.lead','Enquiry',copy=False)
    reSyncCount = fields.Integer('Re Sync Count',compute='_compute_reSync')
    
    materialInfo = fields.Text('Changed Material Quantities')
    
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
        default = dict(default or {})
        default.update({'duplicateProcess': True})
        return super(Estimate, self).copy(default)

    
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
                record['total_cost_'+qty] = sum([x['total_cost_'+qty] for x in record.estimate_line])
                record['total_price_extra_'+qty] = sum([x['total_price_'+qty] for x in record.estimate_line if x.isExtra == True])
                
                if qty != 'run_on':
                    record['unAllocated_'+qty] = record['quantity_'+qty] - sum([x['param_finished_quantity_'+qty] for x in record.estimate_line if x.option_type == 'material'])
                else:
                    record['unAllocated_'+qty] = record[qty] - sum([x['param_finished_quantity_'+qty] for x in record.estimate_line if x.option_type == 'material'])
                    
            record.hasDelivery = len(record.estimate_line.filtered(lambda x: x.documentCatergory == 'Despatch')) > 0
    
    
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
                'context' : "{'default_estimate_id' : active_id,'default_grammage' : %d}"%(self.grammage),
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
    