# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContactJobTitle(models.Model):
    _name = 'bb_contacts.job'
    _rec_name = 'jobTitle'
    
    jobTitle = fields.Char(string="Job Title",required=True)

class ContactLink(models.Model):
    _name = 'bb_contacts.contacts_link'
    
    status = fields.Selection([('current','Current'),('past','Past')],required='True',string="State",default="current")
    company = fields.Many2one('res.partner',string="Company",domain="[('is_company','=',True)]",required=True)
    jobTitle = fields.Many2one('bb_contacts.job',string="Job Title")
    jobRole = fields.Selection([('owner','Bussiness Owner'),('department_manager','Departmental Manager'),('finance_excetive','Finance Executive'),('sale_executive','Sales Executive'),('purchase','Purchase'),('account_executive','Account Executive'),('production','Production'),('complaint_dept','Complaints Dept')],string="Job Role")
    relationship = fields.Char(string="Relationship")        
    address = fields.Char(string="Address")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile Phone")
    extension = fields.Integer(string="Extension")
    email = fields.Char(string='E-mail')
    fax = fields.Char(string='Fax-No')
    joiningDate = fields.Date(string="Joining Date")
    leavingDate = fields.Date(string="Leaving Date")
    
    contact = fields.Many2one('res.partner',string='Contact',domain="[('is_company','=',False)]",required=True)
    
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
        record = super(ContactLink,self).create(values)
        #data = {'contactLinks': [(4,record.id)]}
        #record.company.write(data)
        #record.contact.write(data)
        return record
        
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
    jobRole = fields.Char('Job Role')
    contactExtention = fields.Char('Contact Extention')
    mainContact = fields.Boolean('Main Contact')
    
    companyLinks = fields.One2many('bb_contacts.contacts_link','companyLink_id',string='Comapanies')
    contactLinks = fields.One2many('bb_contacts.contacts_link','contactLink_id',string='Contacts')
    
  