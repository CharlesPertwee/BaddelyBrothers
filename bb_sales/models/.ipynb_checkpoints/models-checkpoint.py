# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sales(models.Model):
    _inherit = "sale.order"
   
    partnerOnHold = fields.Boolean('Account on Hold')
    
    @api.onchange('partner_id')
    def check_hold(self):
        for record in self:
            if record.partner_id:
                if record.partner_id.onHold or (record.partner_id.company_type == 'person' and record.partner_id.parent_id.onHold):
                    record.partnerOnHold = True
                else:
                    record.partnerOnHold = False
                
    