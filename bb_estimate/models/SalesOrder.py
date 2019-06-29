# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sales(models.Model):
    _inherit = "sale.order"
    
    Project = fields.Many2one('project.project','Project',related="Estimate.project")
    Estimate = fields.Many2one('bb_estimate.estimate',string='Originating Estimate')
    JobTicket = fields.Many2one('mrp.production',string="Job Ticket")
    partnerOnHold = fields.Boolean('Account on Hold')
    priceHistory = fields.One2many('bb_estimate.price_history','SalesOrder','Price Adjustments')
    
    @api.onchange('partner_id')
    def check_hold(self):
        for record in self:
            if record.partner_id:
                if record.partner_id.onHold or (record.partner_id.company_type == 'person' and record.partner_id.parent_id.onHold):
                    record.partnerOnHold = True
                else:
                    record.partnerOnHold = False
    
    def AdjustPrice(self):
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'name': 'Adjust Price',
                'res_model' : 'bb_estimate.adjust_price_so',
                'type' : 'ir.actions.act_window',
                'context' : "{'default_SalesOrder' : active_id}",
                'target' : 'new',
            }