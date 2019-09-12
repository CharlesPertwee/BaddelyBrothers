from collections import defaultdict

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round

class SupplierPO(models.Model):
    _inherit = "product.supplierinfo"
    
    minQuantity = fields.Integer('Minimum Quantity for Estimate')
    multiplier = fields.Integer('Multiple Of',default=1)
    
class Purchase(models.Model):
    _inherit = 'purchase.order'
    
    @api.multi
    def print_quotation(self):
        self.write({'state': "sent"})
        return self.env.ref('bb_estimate.request_for_quotation').report_action(self)
    
    @api.multi
    def write(self,vals):
        if 'origin' in vals.keys():
            pos = vals['origin'].split(',')
            sq = self.env['ir.sequence'].search([('code','=','bb_estimate.jobticket')],limit=1)
            if sq:
                for po in pos:
                    if sq.prefix in po:
                        mrp = self.env['mrp.production'].search([('name','=',po.strip())])
                        if mrp:
                            if self not in mrp.Purchases:
                                mrp.write({'Purchases':[(4, self.id)]})
                            if self not in mrp.Project.Purchase:                                
                                mrp.Project.write({'Purchase':[(4, self.id)]})
                            
        return super(Purchase,self).write(vals)
    
    @api.model
    def create(self,vals):
        record = super(Purchase,self).create(vals)
        if vals['origin']:
            pos = vals['origin'].split(',')
            for po in pos:
                sq = self.env['ir.sequence'].search([('code','=','bb_estimate.jobticket')],limit=1)
                if sq:
                    if sq.prefix in po:
                        mrp = self.env['mrp.production'].search([('name','=',po.strip())])
                        if mrp:
                            if self not in mrp.Purchases:
                                mrp.write({'Purchases':[(4, record.id)]})
                            if self not in mrp.Project.Purchase:
                                mrp.Project.write({'Purchase':[(4, record.id)]})
                            
        return record