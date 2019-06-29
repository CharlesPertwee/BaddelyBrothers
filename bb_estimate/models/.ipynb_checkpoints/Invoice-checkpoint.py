# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    Project = fields.Many2one('project.project','Project')
    
    def create(self,vals):
        if vals['origin']:
            sale_order = self.env['sale.order'].sudo().search([('name','=',record.origin)])
            if sale_order.Estimate:
                vals['Project'] = Estimate.project.id
        return super(AccountInvoice,self).create(vals)
    @api.model
    def getEstimateData(self):
        for record in self:
            if record.origin:
                sale_order = self.env['sale.order'].sudo().search([('name','=',record.origin)])
                return sale_order.Estimate
            
    @api.model
    def getMo(self):
        for record in self:
            sale_order_estimate = self.getEstimateData()
            mo = self.env['mrp.production'].sudo().search([('Estimate.id','=',sale_order_estimate.id)])
            return mo