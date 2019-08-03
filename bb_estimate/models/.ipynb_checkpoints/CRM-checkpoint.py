# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
DUPLEX_OPTIONS = [
    ('two', '2 Sheets'),
    ('three', '3 Sheets'),
    ('four', '4 Sheets'),
    ('five', '5 Sheets'),
]

EDGING = [
    ('Silver','Silver'),
    ('Gold','Gold'),
    ('Custom','Custom'),
]

ORIGINATION = [
    ('Print Ready PDF','Print Ready PDF'),
    ('You to prepare file from copy supplied','You to prepare file from copy supplied'),
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

class Leads(models.Model):
    _inherit = 'crm.lead'
    
    Estimates = fields.One2many('bb_estimate.estimate','lead','Estimates')
    Estimate_Count = fields.Integer('Processes', compute='_compute_estimates')
    Project = fields.Many2one('project.project', ondelete='restrict')
    
    #Web Form fields
    enquiryType = fields.Selection([('Envelope Estimate','Envelope Estimate'),('Print Estimate','Print Estimate')],string="Enquiry Type") 
    
    #Web form Envelope Field
    Quantity1 = fields.Integer('Quantity 1')
    Quantity2 = fields.Integer('Quantity 2')
    Quantity3 = fields.Integer('Quantity 3')
    Quantity4 = fields.Integer('Quantity 4')
    runOn = fields.Integer('Run on')
    enquiryEnvelopeType = fields.Selection(ENVELOPE_TYPES,'Envelope Types')
    enquiryEnvelopeFlaptype = fields.Selection(FLAP_GLUE_TYPES,'Flap Type')
    enquiryEnvelopeTissuelIne = fields.Selection(TISSUE_LINING_OPTIONS,'Tissue Line')
    
    #Web Form Print Field
    enquiryPrintEdging = fields.Selection(EDGING,'Edging')
    enquiryPrintDuplex = fields.Selection(DUPLEX_OPTIONS,'Duplex')
    enquiryEnvelopeWindow  = fields.Boolean('Windowed')
    
    enquiryMaterial = fields.Char('Material')
    enquiryWeightGsm = fields.Char('Weight(g.s.m)')
    enquiryPrintOrigination = fields.Selection(ORIGINATION,'Print Origination')
    
    size = fields.Many2one('bb_products.material_size','Size')
    
    def _compute_estimates(self):
            for record in self:
                self.Estimate_Count = len(record.Estimates)