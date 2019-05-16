# -*- coding: utf-8 -*-
from odoo import http

# class BbProducts(http.Controller):
#     @http.route('/bb_products/bb_products/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bb_products/bb_products/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bb_products.listing', {
#             'root': '/bb_products/bb_products',
#             'objects': http.request.env['bb_products.bb_products'].search([]),
#         })

#     @http.route('/bb_products/bb_products/objects/<model("bb_products.bb_products"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bb_products.object', {
#             'object': obj
#         })