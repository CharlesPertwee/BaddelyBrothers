# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Leads(models.Model):
    _inherit = 'crm.lead'
    _name = 'crm.lead'
    
    typeOfLead = fields.Selection([('Trade Counter','Trade Counter'),('Bespoke','Bespoke')],string="Type Of Opportunity",default="Trade Counter")
    
class Stages(models.Model):
    _inherit = 'crm.stage'
    _name = 'crm.stage'
    
    typeOfLead = fields.Selection([('Trade Counter','Trade Counter'),('Bespoke','Bespoke')],string="Opportunity Type",default="Trade Counter")
    isCommon = fields.Boolean(string="Is Common")
