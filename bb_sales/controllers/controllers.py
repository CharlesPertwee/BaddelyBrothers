# -*- coding: utf-8 -*-
from odoo import http

# class BbSales(http.Controller):
#     @http.route('/bb_sales/bb_sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bb_sales/bb_sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bb_sales.listing', {
#             'root': '/bb_sales/bb_sales',
#             'objects': http.request.env['bb_sales.bb_sales'].search([]),
#         })

#     @http.route('/bb_sales/bb_sales/objects/<model("bb_sales.bb_sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bb_sales.object', {
#             'object': obj
#         })