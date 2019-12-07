# -*- coding: utf-8 -*-
import odoo
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError

class LeadConversion(models.TransientModel):
	_name = 'bb_estimate.LeadConversion'
    _desc = 'Lead Conversion Report'

    FinancialYear = fields.Integer('Financial Year')
    Year = fields.Integer('Year')
    Month = fields.Tnteger('Month')
    EnquiryType = fields.Selection([],string='Enquiry Type')
    TotalEnquiry = fields.Integer('Total Enquiries')
    ConvertedEnquriy = fields.Integer('Converted To Estimate')
    ConvertedOrder = fields.Integer('Converted To Order')

    

