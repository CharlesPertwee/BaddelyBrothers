# -*- coding: utf-8 -*-

from odoo import http, tools, _
from odoo.http import request, Controller, Response
import requests
import codecs
import datetime
import base64
import json
import pytz
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from psycopg2 import IntegrityError
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.exceptions import ValidationError

class WebToLead(WebsiteForm):
    @http.route('/contactus', type='http', auth='public', website='True')
    def contactData(self,**kw):
        countries = request.env['res.country'].sudo().search([])
        envelopeSize = request.env['bb_products.material_size'].sudo().search([('isEnvelopeEstimate','=',True)])
        printSize = request.env['bb_products.material_size'].sudo().search([('isPrintSize','=',True)])
        
        return request.render('bb_estimate.bb_contactus_form',{'countries':countries,'envelopeSize':envelopeSize,'printSize':printSize})
    
    # Extract all data sent by the form and sort its on several properties
    def extract_data(self, model, values):
        #Removal of alternate fields from the values
        if dict(values)['enquiryType'] == 'Envelope Estimate':
            values = {key:value for key,value in values.items() if 'print' not in key.lower()}
            values['enquiryEnvelopeWindow'] = True if values['enquiryEnvelopeWindow'] == 'yes' else False
            if 'enquirySize' in values and values['enquirySize']:
                values['size'] = values['enquirySize']
                values.pop('enquirySize')
        else:
            values = {key:value for key,value in values.items() if 'envelope' not in key.lower()}
            if 'enquiryPrintSize' in values and values['enquiryPrintSize']:
                values['size'] = values['enquiryPrintSize']
                values.pop('enquiryPrintSize')
                
        #Addition of custom fields
        values['contact_name'] = ("%s %s")%(values['enquiryFirstName'] if 'enquiryFirstName' in values.keys() else "",values['enquiryLastName'] if 'enquiryLastName' in values.keys() else "")
        if 'enquiryFirstName' in values.keys():
            values.pop('enquiryFirstName') 
        if 'enquiryLastName' in values.keys():
            values.pop('enquiryLastName')
        values['typeOfLead'] = 'Bespoke'
        
        return super(WebToLead, self).extract_data(model,values)

     