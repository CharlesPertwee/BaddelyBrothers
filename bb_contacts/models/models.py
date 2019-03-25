# -*- coding: utf-8 -*-

from odoo import models, fields, api
from docx import Document
import datetime


class ContactJobTitle(models.Model):
    _name = 'bb_contacts.job'
    _rec_name = 'jobTitle'
    
    jobTitle = fields.Char(string="Job Title",required=True)

class ContactLink(models.Model):
    _name = 'bb_contacts.contacts_link'
    _order = "status"
    
    status = fields.Selection([('current','Current'),('past','Past')],required='True',string="State",default="current")
    company = fields.Many2one('res.partner',string="Company",domain="[('is_company','=',True)]",required=True)
    jobTitle = fields.Many2one('bb_contacts.job',string="Job Title")
    jobRole = fields.Selection([('owner','Business Owner'),('department_manager','Departmental Manager'),('finance_excetive','Finance Executive'),('sale_executive','Sales Executive'),('purchase','Purchase'),('account_executive','Account Executive'),('production','Production'),('complaint_dept','Complaints Dept')],string="Job Role")
    relationship = fields.Char(string="Relationship")        
    address = fields.Many2one('res.partner', string="Address",domain="[('type','!=','contact')]")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile Phone")
    extension = fields.Integer(string="Extension")
    email = fields.Char(string='E-mail')
    fax = fields.Char(string='Fax-No')
    joiningDate = fields.Date(string="Joining Date")
    leavingDate = fields.Date(string="Leaving Date")
    main = fields.Boolean(string="Main")
    temperament = fields.Char("Temperament")
    
    contact = fields.Many2one('res.partner',string='Contact',domain="[('is_company','=',False),('type','=','contact')]",required=True)
    
    contactLink_id = fields.Many2one('res.partner')
    companyLink_id = fields.Many2one('res.partner')
    
    #@api.onchange('leavingDate')
    #def leave_employee(self):
    #    for record in self:
    #        if(record.leavingDate):
    #            record.status = 'past'
    
        
    @api.model
    def create(self,values):
        values['contactLink_id'] = values['contact']
        values['companyLink_id'] = values['company']
        values['main'] = self.env['res.partner'].search([('id','=',values['contact'])]).mainContact
        #values['temperament'] = self.env['res.partner'].search([('id','=',values['contact'])]).temperament
        #values['relationship'] = self.env['res.partner'].search([('id','=',values['contact'])]).relationship
        record = super(ContactLink,self).create(values)
        #data = {'contactLinks': [(4,record.id)]}
        #record.company.write(data)
        #record.contact.write(data)
        return record
       
    def generate_address_label_report(self):
        date = str(datetime.datetime.now().date())
        type = "normal"
        return{
            'type':'ir.actions.act_url',
            'url':'/doc/report/%s/%s/%s'%(self.id,type,date),
            'data':self.id,
            'target':'self',
        }            
   
    def headed_letter_report(self):
        date = str(datetime.datetime.now().date())
        type = "letter"
        return{
            'type':'ir.actions.act_url',
            'url':'/doc/report/%s/%s/%s'%(self.id,type,date),
            'data':self.id,
            'target':'self',
        }
    
    def blank_letter_report(self):
        date = str(datetime.datetime.now().date())
        type = "head_letter"
        return{
            'type':'ir.actions.act_url',
            'url':'/doc/report/%s/%s/%s'%(self.id,type,date),
            'data':self.id,
            'target':'self',
        }
    
    
        
class Partner(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    
    reference = fields.Char('Reference No.')
    vatCountryCode = fields.Char('VAT Country Code')
    mailingRestrictions = fields.Boolean('Mailing Restrictions')
    faxNumber = fields.Char('Fax Number')
    employeeCount = fields.Integer('Number of Employee')
    sector = fields.Selection([('Design/Mktg','Design/Mktg'),('Direct','Direct'),('Government','Government'),('Private','Private'),('Student','Student'),('Supplier','Supplier'),('Trade','Trade'),('Trade-Govt','Trade-Govt'),('Trade-Printer','Trade-Printer'),('Trade-Retail','Trade-Retail')],string='Sector')
    source = fields.Selection([('Web','Web'),('Mailing','Mailing'),('E-Mail','E-Mail'),('Phone','Phone'),('Referral','Referral'),('Ad','Ad')],string='Source')
    jobRole = fields.Selection([('owner','Business Owner'),('department_manager','Departmental Manager'),('finance_excetive','Finance Executive'),('sale_executive','Sales Executive'),('purchase','Purchase'),('account_executive','Account Executive'),('production','Production'),('complaint_dept','Complaints Dept')],default="owner",string="Job Role")
    contactExtention = fields.Char('Contact Extention')
    mainContact = fields.Boolean('Main Contact')
    capability = fields.Char('Capability')
    personalPhone = fields.Char('Personal Phone')
    personalMobile = fields.Char('Personal Mobile')
    personalEmail = fields.Char('Personal Email')
    employeeStatus = fields.Selection([('current','Current'),('past','Past')],required='True',string="State",default="current")
    joiningDate = fields.Date(string="Joining Date")
    leavingDate = fields.Date(string="Leaving Date")
    companyLinks = fields.One2many('bb_contacts.contacts_link','companyLink_id',string='Company History')
    contactLinks = fields.One2many('bb_contacts.contacts_link','contactLink_id',string='Contact History')
    
    #toa = fields.Char('Turnover FY 2016-17')
    #tob = fields.Char('Turnover FY 2017-18')
    #toc = fields.Char('Turnover FY 2018-19')
    
    def _get_name(self):
        """ Utility method to allow name_get to be overrided without re-browse the partner """
        partner = self
        name = partner.name or ''

        if partner.company_name or partner.parent_id:
            if not name and partner.type in ['invoice', 'delivery', 'other']:
                name = dict(self.fields_get(['type'])['type']['selection'])[partner.type]
            if not partner.is_company:
                name = "%s, %s" % (partner.commercial_company_name or partner.parent_id.name, name)
        if self._context.get('show_address_only'):
            name = partner._display_address(without_company=True)
        if self._context.get('show_address'):
            name = name + "\n" + partner._display_address(without_company=True)
        name = name.replace('\n\n', '\n')
        name = name.replace('\n\n', '\n')
        if self._context.get('address_inline'):
            name = name.replace('\n', ', ')
        if self._context.get('show_email') and partner.email:
            name = "%s <%s>" % (name, partner.email)
        if self._context.get('html_format'):
            name = name.replace('\n', '<br/>')
        if self._context.get('show_vat') and partner.vat:
            name = "%s - %s" % (name, partner.vat)
        name = partner.street if partner.type != 'contact' else name
        return name
    
    
    @api.model
    def create(self,values):
        record = super(Partner, self).create(values)
        if record:
            if record.type == 'contact' and record.company_type == 'person':
                data = {
                    'status': 'current',
                    'company': record.parent_id.id, 
                    'address': record.parent_id.id,
                    'phone': record.phone,
                    'mobile': record.mobile,
                    'email': record.email,
                    'contact' : record.id
                }
                self.env['bb_contacts.contacts_link'].sudo().create(data)
        return record
        
