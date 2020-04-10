# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from docx import Document
import datetime


ACCOUNT_STATUS = [
    ('Open','Open'),
    ('New Customer - Awaiting Credit Approval','New Customer - Awaiting Credit Approval'),
    ('New Account','New Account'),
    ('Cash/chq on delievery only','Cash/chq on delievery only'),
    ('Settle a/c prior to ordering','Settle a/c prior to ordering'),
    ('On stop - see DP or CP','On stop - see DP or CP'),
    ('In court - on stop','In court - on stop'),
    ('In liquidation on stop','In liquidation on stop'),
    ('Closed','Closed'),
    ('Delete Account','Delete Account')
  ]

class HistoryGroup(models.Model):
    _name = 'bb_contacts.history'
    _rec_name = 'name'
    name = fields.Char('Name',required=True)
    
    contacts = fields.One2many('res.partner','history_id',string='Contacts',context={'active_test': False})
    
class Partner(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    
    reference = fields.Char('Reference No.')
    vatCountryCode = fields.Char('VAT Country Code')
    mailingRestrictions = fields.Boolean('Mailing Restriction')
    faxNumber = fields.Char('Fax Number')
    employeeCount = fields.Integer('Number of Employees')
    sector = fields.Selection([('Design / Mktg','Design / Mktg'),('Direct','Direct'),('Government','Government'),('Private','Private'),('Student','Student'),('Supplier','Supplier'),('Trade','Trade'),('Trade - Govt','Trade - Govt'),('Trade - Printer','Trade - Printer'),('Trade - Retail','Trade - Retail')],string='Sector')
    source = fields.Selection([('Web','Web'),('Mailing','Mailing'),('E-Mail','E-Mail'),('Phone','Phone'),('Referral','Referral'),('Ad','Ad')],string='Source')
    jobRole = fields.Selection([('Business Owner','Business Owner'),('Departmental Manager','Departmental Manager'),('Finance Executive','Finance Executive'),('Sales Executive','Sales Executive'),('Purchasing','Purchasing'),('Accounts Executive','Accounts Executive'),('Production','Production'),('Complaints Dept','Complaints Dept')],default="Business Owner",string="Job Role")
    contactExtention = fields.Char('Phone Extention')
    mainContact = fields.Boolean('Main Contact')
    capability = fields.Char('Capability')
    personalPhone = fields.Char('Personal Phone')
    personalMobile = fields.Char('Personal Mobile')
    personalEmail = fields.Char('Personal Email')
    employeeStatus = fields.Selection([('current','Current'),('past','Past')],required='True',string="Contact Status",default="current")
    joiningDate = fields.Date(string="Joining Date")
    leavingDate = fields.Date(string="Leaving Date")
    
    
    toa = fields.Char('Turnover FY 2016-17')
    tob = fields.Char('Turnover FY 2017-18')
    toc = fields.Char('Turnover FY 2018-19')
    
    history_id = fields.Many2one('bb_contacts.history',string='Group')
    
    customerType = fields.Selection([('Price Driven','Price Driven'),('Product Driven','Product Driven'),('Customer Driven','Customer Driven')],string="Customer Type")
    
    #Compute Fields only, doesn't store any data.
    contact_id = fields.Many2one('res.partner',store=False)
    contactHistory = fields.One2many('res.partner','history_id',string='Contact Links', compute="_compute_contact_history",store=False)
    
    accountStatus = fields.Selection(ACCOUNT_STATUS, string="Account Status", default="New Customer - Awaiting Credit Approval")
    onHold = fields.Boolean('Account on Hold', default=True)

    readOnlyGroup = fields.Boolean('Read Only Group', compute="_compute_group_access")
    
    specialReport = fields.Boolean('Custom Delivery Note')

    AdminContact = fields.Boolean("Restricted")
    payeeName = fields.Many2one("res.partner",'Payee')
    isPayee = fields.Boolean('Is a Payee?')

    @api.constrains('onHold','accountStatus')
    def on_hold_constraint(self):
        for record in self:
            if not record.accountStatus in ['Open','New Account'] and not record.onHold:
                raise ValidationError("For Account Status: %s, Account on hold must be true"%(str(record.accountStatus)))
            elif record.accountStatus in ['Open','New Account'] and record.onHold:
                raise ValidationError("For Account Status: %s, Account on hold must be false"%(str(record.accountStatus)))


    def _compute_group_access(self):
        self.readOnlyGroup = not self.env.user.has_group('bb_contacts.group_contacts_user')
    
    def _compute_contact_history(self):
        self.contactHistory = self.history_id.contacts
    
    @api.model
    def create(self,values):
        record = super(Partner, self).create(values)
        if record:
            if (record.name and record.company_type == 'person'):
                if not record.history_id:
                    data = {
                        'name': record.name
                    }
                    rec = self.env['bb_contacts.history'].sudo().create(data)
                    record.write({'history_id':rec.id})
                else:
                    records = self.env['bb_contacts.history'].sudo().search([('id','=',record.history_id.id)])
                    for rec in records.contacts:
                        if rec.id != record.id:
                            rec.write({'employeeStatus':'past'})
        return record            
    
    def move_company(self):
        data = self.copy()
        view_id = self.env.ref('bb_contacts.view_partner_form_bb').id
        
        #set field values
        data.parent_id = None
        data.joiningDate = None
        data.leavingDate = None
        
        #Archive Contact
        self.write({'active':False})

        return {
            "name": "Contact Form",
            "view_type": "form",
            "view_mode": "form",
            'views' : [(view_id,'form')],
            "res_model": "res.partner",
            'view_id': view_id,
            "type": "ir.actions.act_window",
            "res_id": data.id,
            "target": "new",
            
        }