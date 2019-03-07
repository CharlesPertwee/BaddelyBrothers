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
    relationship = fields.Text(string="Relationship")        
    address = fields.Char(string="Address")
    phone = fields.Integer(string="Phone")
    mobile = fields.Integer(string="Mobile Phone")
    extension = fields.Text(string="Extension")
    email = fields.Char(string='E-mail')
    fax = fields.Integer(string='Fax-No')
    joiningDate = fields.Date(string="Joining Date")
    leavingDate = fields.Date(string="Leaving Date")
    
    contact = fields.Many2one('res.partner','Contact')
    
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
    
    contactLinks = fields.One2many('bb_contacts.contacts_link','contact','Contacts')
    


    
# class CompanyLink(models.Model):
#     _name = 'bb_contacts.company_link'
    
#     status = fields.Selection([('current','Current'),('past','Past')],required='True',string="State",default="current")
#     company = fields.Many2one('res.partner',string="Company",domain="[('is_company','=',False)]",required=True)
#     jobTitle = fields.Many2one('bb_contacts.job',string="Job Title")
#     jobRole = fields.Selection([('owner','Bussiness Owner'),('department_manager','Departmental Manager'),('finance_excetive','Finance Executive'),('sale_executive','Sales Executive'),('purchase','Purchase'),('account_executive','Account Executive'),('production','Production'),('complaint_dept','Complaints Dept')],string="Job Role")
#     relationship = fields.Text(string="Relationship")        
#     address = fields.Char(string="Address")
#     phone = fields.Integer(string="Phone")
#     mobile = field.Integer(string="Mobile Phone")
#     extension = fields.Text(string="Extension")
#     email = fields.Char(string='E-mail')
#     fax = fields.Integer(string='Fax-No')
#     #fields for map_view
#     joiningDate = fields.Date(string="Joining Date")
#     leavingDate = fields.Date(string="Leaving Date")
#     