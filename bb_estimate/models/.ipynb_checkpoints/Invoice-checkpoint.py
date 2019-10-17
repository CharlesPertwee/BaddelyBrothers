# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountInvoiceBB(models.Model):
    _inherit = "account.invoice"
    
    Project = fields.Many2one('project.project','Project')
    invoiceDescription = fields.Html('Invoice Details')
    
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         res = super(AccountInvoiceBB, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
#         if self._context.get('type'):
#             if res.get('toolbar', False) and res.get('toolbar').get('print', False):
#                 reports = res.get('toolbar').get('print')
#                 type = self._context.get('type')
#                 if type == 'in_invoice':
#                     _reports = [x for x in reports if not x['report_name'].startswith('bb_estimate')]
#                     res['toolbar']['print'] = _reports
#                 elif type == 'out_invoice':
#                     _reports = [x for x in reports if x['report_name'].startswith('bb_estimate')]
#                     res['toolbar']['print'] = _reports
#         return res
                    
          
    @api.model
    def create(self,vals):
        if 'origin' in vals.keys():
            if vals['origin']:
                sale_order = self.env['sale.order'].sudo().search([('name','=',vals['origin'])])
                if sale_order.Estimate:
                    vals['Project'] = sale_order.Estimate.project.id
                    vals['invoiceDescription'] = sale_order.ProFormaLines 
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
    