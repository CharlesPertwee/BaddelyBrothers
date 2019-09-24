# -*- coding: utf-8 -*-

import json

from odoo import api, models, _
from odoo.tools import float_round

class ReportBomStructure(models.AbstractModel):
    _name = 'report.crm.conversion_analysis'
    _description = 'CRM Lead Conversion Analysis'
    
    @api.model
    def get_html(self, id=False):
        res = self._get_report_data();
        res['leads'].append({'report_type':'html'})
        res['leads'] = self.env.ref('bb_estimate.lead_conversion_analysis').render({'data': res['leads']})
        return res
    
    def get_leads(self, param):
        lead_data = []
        leads_dict = {}
        for lead in self.env['crm.lead'].search([]):
            if param == "year":
                year = str(lead.create_date.strftime("%Y"))
                leads_dict[year].append(lead) if year in leads_dict else leads_dict.update({year:[lead]})
        lead_data.append(leads_dict)
        return lead_data
    
    def _get_report_data(self):
        lines = self.get_leads('year')
        return{
            'leads':lines,
        }