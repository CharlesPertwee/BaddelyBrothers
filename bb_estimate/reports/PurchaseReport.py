# -*- coding: utf-8 -*-
from odoo import tools
from odoo import models, fields, api
import datetime

class PurchaseDayReport(models.Model):
    _name = 'bb_estimate.purchase_day_report'
    _desc = 'Purchase Report'
    _auto = False
    _order = 'id desc'
    
    order_date = fields.Char('Order Date', readonly=True)
    supplier = fields.Char('Supplier', readonly=True)
    name = fields.Char('Order No', readonly=True)
    qty = fields.Float('Quantity', readonly=True, digits=(16,0))
    description = fields.Char('Description', readonly=True)
    job_no = fields.Char('Job No', readonly=True)
    value = fields.Char('Value', readonly=True)
    inv_ref = fields.Char('Inv Ref', readonly=True)
    price = fields.Char('Price', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        return """
            SELECT
                l.id, 
                to_char(date_order,'MM/dd/yyyy') order_date,
                p.name supplier,
                o.name,
                product_qty qty,
                l.name description,
                o.origin job_no,
                l.price_total "value",
                '' inv_ref,
                l.price_unit price 
            FROM purchase_order_line l
            inner join purchase_order o on l.order_id = o.id
            join res_partner p on p.id = o.partner_id


        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))