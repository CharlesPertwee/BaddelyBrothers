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
    
    invoiceEditableLines = fields.Html('Invoice Line')
    InvoiceId = fields.Many2one('account.invoice','Invoice')          
    
    def ChangeInvoiceLines(self):
        if self.invoiceEditableLines:
            self.InvoiceId.write({'invoiceDescription':self.invoiceEditableLines})
        elif not self.invoiceEditableLines:
            raise ValidationError("Invoice description can't be left empty.")