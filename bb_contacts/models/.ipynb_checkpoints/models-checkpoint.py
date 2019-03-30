# -*- coding: utf-8 -*-

from odoo import models, fields, api
from docx import Document
import datetime

class HistoryGroup(models.Model):
    _name = 'bb_contacts.history'
    _rec_name = 'name'
    name = fields.Char('Name',required=True)
    
    contacts = fields.One2many('res.partner','history_id',string='Contacts')
    
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
    jobRole = fields.Selection([('owner','Business Owner'),('department_manager','Departmental Manager'),('finance_excetive','Finance Executive'),('sale_executive','Sales Executive'),('purchase','Purchase'),('account_executive','Account Executive'),('production','Production'),('complaint_dept','Complaints Dept')],default="owner",string="Job Role")
    contactExtention = fields.Char('Contact Extention')
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
    
    def _compute_contact_history(self):
        self.contactHistory = self.history_id.contacts
    
#     def _get_name(self):
#         """ Utility method to allow name_get to be overrided without re-browse the partner """
#         partner = self
#         name = partner.name or ''

#         if partner.company_name or partner.parent_id:
#             if not name and partner.type in ['invoice', 'delivery', 'other']:
#                 name = dict(self.fields_get(['type'])['type']['selection'])[partner.type]
#             if not partner.is_company:
#                 name = "%s, %s" % (partner.commercial_company_name or partner.parent_id.name, name)
#         if self._context.get('show_address_only'):
#             name = partner._display_address(without_company=True)
#         if self._context.get('show_address'):
#             name = name + "\n" + partner._display_address(without_company=True)
#         name = name.replace('\n\n', '\n')
#         name = name.replace('\n\n', '\n')
#         if self._context.get('address_inline'):
#             name = name.replace('\n', ', ')
#         if self._context.get('show_email') and partner.email:
#             name = "%s <%s>" % (name, partner.email)
#         if self._context.get('html_format'):
#             name = name.replace('\n', '<br/>')
#         if self._context.get('show_vat') and partner.vat:
#             name = "%s - %s" % (name, partner.vat)
#         name = partner.street if partner.type != 'contact' else name
#         return name
    
    
    @api.model
    def create(self,values):
        record = super(Partner, self).create(values)
        if record:
            if (record.type == 'contact' and record.company_type == 'person'):
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
        
    
        
