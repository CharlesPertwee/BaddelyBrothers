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
        data = res['leads']
        res['lines'] = self.env.ref('bb_estimate.lead_conversion_analysis').render({'data': res['leads']})
        return res
    
    def _get_leads(self, param, relation):
        lead_data = []
        leads_dict = {}
        for lead in self.env['crm.lead'].search([]):
            if param == "year":
                year = str(lead.create_date.strftime("%Y"))
                if (year in leads_dict):
                    leads_dict[year][0]['leads'].extend([lead]) if len(leads_dict[year]) > 0 else leads_dict[year].append({'leads':[lead]})
                    leads_dict[year][0].update({'total_enquiries':len(leads_dict[year][0]['leads'])})
                    leads_dict[year][0].update({'total_enquiries_to_estimate':12})#sum[1 for x in leads_dict[year][0]['leads'] if x.stage_id.name == "Estimate In Progress"]})
                    leads_dict[year][0].update({'total_enquiries_to_order':15})#sum[1 for x in leads_dict[year][0]['leads'] if x.stage_id.name == "Converted to Job"]})
                    leads_dict[year][0].update({'level':0})
                else:
                    leads_dict[year] = []
                    
            elif param == 'month':
                month = str(lead.create_date.strftime("%m"))
                if str(lead.create_date.strftime("%Y")) == str(relation):
                    if (month in leads_dict):
                        leads_dict[month][0]['leads'].extend([lead]) if len(leads_dict[month]) > 0 else leads_dict[month].append({'leads':[lead]})
                        leads_dict[month][0].update({'total_enquiries':len(leads_dict[month][0]['leads'])})
                        leads_dict[month][0].update({'total_enquiries_to_estimate':12})#sum[1 for x in leads_dict[year][0]['leads'] if x.stage_id.name == "Estimate In Progress"]})
                        leads_dict[month][0].update({'total_enquiries_to_order':15})#sum[1 for x in leads_dict[year][0]['leads'] if x.stage_id.name == "Converted to Job"]})
                        leads_dict[month][0].update({'level':1})
                    else:
                        leads_dict[month] = []
                    
            elif param == 'type':
                type = lead.typeOfLead if lead.typeOfLead else 'Undefined'
                month, year = relation.split("/")
                if (str(lead.create_date.strftime("%Y") == str(year)) and (str(lead.create_date.strftime("%m")) == str(month))):
                    if (type in leads_dict):
                        leads_dict[type][0]['leads'].extend([lead]) if len(leads_dict[type]) > 0 else leads_dict[type].append({'leads':[lead]})
                        leads_dict[type][0].update({'total_enquiries':len(leads_dict[type][0]['leads'])})
                        leads_dict[type][0].update({'total_enquiries_to_estimate':12})#sum[1 for x in leads_dict[year][0]['leads'] if x.stage_id.name == "Estimate In Progress"]})
                        leads_dict[type][0].update({'total_enquiries_to_order':15})#sum[1 for x in leads_dict[year][0]['leads'] if x.stage_id.name == "Converted to Job"]})
                        leads_dict[type][0].update({'level':1})
                    else:
                        leads_dict[type] = []
                            
        lead_data.append(leads_dict)
        return lead_data
    
    def get_leads_year(self, year):
        leads_by_months = self._get_leads('month', year)
        return self.env.ref('bb_estimate.report_conversion_analysis_month').render({'data': leads_by_months})
    
    def get_lead_type(self, month):
        leads_by_type = self._get_leads('type', month)
        return self.env.ref('bb_estimate.report_conversion_analysis_type').render({'data':leads_by_type})
    
    def _get_report_data(self):
        lines = self._get_leads('year', None)
        return{
            'leads':lines,
        }