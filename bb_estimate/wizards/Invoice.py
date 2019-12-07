# -*- coding: utf-8 -*-
import odoo
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError

class ConfirmationLines(models.TransientModel):
    _name = 'invoice.edit_lines'
    
    @api.onchange('InvoiceId')
    def getEditableLines(self):
        if 'default_InvoiceId' in self._context.keys():
            invoice = self.env['account.invoice'].browse(self._context['default_InvoiceId'])
            if invoice:
                if invoice.invoiceDescription:
                    self.invoiceEditableLines = invoice.invoiceDescription
                    
    @api.onchange('SaleOrder')
    def getSaleOrderEditableLines(self):
        if 'default_SaleOrder' in self._context.keys():
            saleOrder = self.env['sale.order'].sudo().browse(self._context['default_SaleOrder'])
            if saleOrder:
                if saleOrder.ProFormaLines:
                    self.invoiceEditableLines = saleOrder.ProFormaLines
    
    invoiceEditableLines = fields.Html('Editable Line')
    InvoiceId = fields.Many2one('account.invoice','Invoice')  
    SaleOrder = fields.Many2one('sale.order','Sale Order')
    
    def ChangeInvoiceLines(self):
        if self.invoiceEditableLines:
            if self.InvoiceId:
                self.InvoiceId.write({'invoiceDescription':self.invoiceEditableLines})
            if self.SaleOrder:
                self.SaleOrder.write({'ProFormaLines':self.invoiceEditableLines})
                
        elif not self.invoiceEditableLines:
            raise ValidationError("Description can't be left empty.")