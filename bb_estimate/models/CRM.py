# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
DUPLEX_OPTIONS = [
    ('none', ''),
    ('two', '2 Sheets'),
    ('three', '3 Sheets'),
    ('four', '4 Sheets'),
    ('five', '5 Sheets'),
]

EDGING = [
    ('none', ''),
    ('Silver','Silver'),
    ('Gold','Gold'),
    ('Custom','Custom'),
]

ORIGINATION = [
    ('none', ''),
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
    ('none', ''),
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
    enquiryEdgeColor = fields.Char('Edge Color')
    
    enquiryPrintDuplex = fields.Selection(DUPLEX_OPTIONS,'Duplex')
    enquiryEnvelopeWindow  = fields.Boolean('Windowed')
    
    enquiryMaterial = fields.Char('Material')
    enquiryWeightGsm = fields.Char('Weight(g.s.m)')
    enquiryPrintOrigination = fields.Selection(ORIGINATION,'Print Origination')
    
    size = fields.Many2one('bb_products.material_size','Size')
    enquirySizeHeight = fields.Integer('Size Height')
    enquirySizeWidth = fields.Integer('Size Width')

    #analytic account
    analytic_account = fields.Many2one('account.analytic.account','Analytic Account', required=True)
        
    def _compute_estimates(self):
            for record in self:
                self.Estimate_Count = len(record.Estimates)
                
    @api.onchange('size')
    def calc_size_change_params(self):
        if self.size:
            self.enquirySizeHeight = self.size.height
            self.enquirySizeWidth = self.size.width

    @api.constrains('stage_id')
    def ValidateStage(self):
        for record in self:
            if record.typeOfLead == 'Bespoke' and record.Estimates:
                estimate = record.Estimates[-1]
                if estimate:
                    stage = estimate.state.LeadStage
                    if stage and record.stage_id.sequence > stage.sequence:
                        raise ValidationError('Enquiry cannot move ahead of the estimate.')
                
            elif record.typeOfLead == 'Bespoke' and record.Estimate_Count == 0 and record.stage_id.sequence != 0:
                raise ValidationError('Please provide an estimate first.')