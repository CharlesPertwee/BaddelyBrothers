# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountInvoiceBB(models.Model):
    _inherit = "account.invoice"
    
    Project = fields.Many2one('project.project','Project')
    invoiceDescription = fields.Html('Invoice Details')
          
    @api.model
    def create(self,vals):
        if vals['origin']:
            sale_order = self.env['sale.order'].sudo().search([('name','=',vals['origin'])])
            if sale_order.Estimate:
                vals['Project'] = sale_order.Estimate.project.id
        return super(AccountInvoiceBB,self).create(vals)
    
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
        
    def create(self,val):
        invoice = super(AccountInvoiceBB,self).create(val)
        Estimate = invoice.getEstimateData()
        Description = ""
        if Estimate:
            Description = "<br/>".join([x.customer_description for x in Estimate.estimate_line if isinstance(x.customer_description,str)])
        invoice.write({'invoiceDescription':Description})
        return invoice
                    
    def EditInvoiceLine(self):
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'name': 'Edit',
                'res_model' : 'invoice.edit_lines',
                'type' : 'ir.actions.act_window',
                'context' : "{'default_InvoiceId' : active_id}",
                'target' : 'new',
            }