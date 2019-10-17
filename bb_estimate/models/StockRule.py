# from dateutil.relativedelta import relativedelta

# from odoo import api, fields, models, _
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
# from odoo.exceptions import UserError

# class StockRuleBB(models.Model):
#     _inherit = "stock.rule"
    
#     @api.multi
#     def _run_buy(self, product_id, product_qty, product_uom, location_id, name, origin, values):
#         raise Exception(product_qty)
#         cache = {}
#         suppliers = product_id.seller_ids\
#             .filtered(lambda r: (not r.company_id or r.company_id == values['company_id']) and (not r.product_id or r.product_id == product_id))
#         if not suppliers:
#             msg = _('There is no vendor associated to the product %s. Please define a vendor for this product.') % (product_id.display_name,)
#             raise UserError(msg)   
#         supplier = self._make_po_select_supplier(values, suppliers, origin = origin,product_id = product_id)
#         partner = supplier.name
#         # we put `supplier_info` in values for extensibility purposes
#         values['supplier'] = supplier

#         domain = self._make_po_get_domain(values, partner)
#         if domain in cache:
#             po = cache[domain]
#         else:
#             po = self.env['purchase.order'].sudo().search([dom for dom in domain])
#             po = po[0] if po else False
#             cache[domain] = po
#         if not po:
#             vals = self._prepare_purchase_order(product_id, product_qty, product_uom, origin, values, partner)
#             company_id = values.get('company_id') and values['company_id'].id or self.env.user.company_id.id
#             po = self.env['purchase.order'].with_context(force_company=company_id).sudo().create(vals)
#             cache[domain] = po
#         elif not po.origin or origin not in po.origin.split(', '):
#             if po.origin:
#                 if origin:
#                     po.write({'origin': po.origin + ', ' + origin})
#                 else:
#                     po.write({'origin': po.origin})
#             else:
#                 po.write({'origin': origin})

#         # Create Line
#         po_line = False
#         for line in po.order_line:
#             if line.product_id == product_id and line.product_uom == product_id.uom_po_id:
#                 if line._merge_in_existing_line(product_id, product_qty, product_uom, location_id, name, origin, values):
#                     vals = self._update_purchase_order_line(product_id, product_qty, product_uom, values, line, partner)
#                     po_line = line.write(vals)
#                     break
#         if not po_line:
#             vals = self._prepare_purchase_order_line(product_id, product_qty, product_uom, values, po, partner)
#             self.env['purchase.order.line'].sudo().create(vals)
    
#     def _make_po_select_supplier(self, values, suppliers, origin,product_id):
#         """ Method intended to be overridden by customized modules to implement any logic in the
#             selection of supplier.
#         """
#         job = self.env['ir.sequence'].search([('code','=','bb_estimate.jobticket')],limit=1)
#         sales = self.env['ir.sequence'].search([('code','=','sale.order')], limit=1)
#         estimate = False
#         if job and (job.prefix in origin):
#             ticket = self.env['mrp.production'].sudo().search([('name','=', origin)],limit=1)
#             if ticket:
#                 estimate = ticket.Estimate
#         if sales and (sales.prefix in origin):
#             sale = self.env['sale.order'].sudo().search([('name','=', origin)],limit=1)
#             if sale:
#                 estimate = sale.Estimate
#         raise Exception(estimate)
#         return suppliers[0]
    