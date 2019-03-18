# -*- coding: utf-8 -*-
from odoo import http

# class BbProductsWeb(http.Controller):
#     @http.route('/bb_products_web/bb_products_web/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bb_products_web/bb_products_web/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bb_products_web.listing', {
#             'root': '/bb_products_web/bb_products_web',
#             'objects': http.request.env['bb_products_web.bb_products_web'].search([]),
#         })

#     @http.route('/bb_products_web/bb_products_web/objects/<model("bb_products_web.bb_products_web"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bb_products_web.object', {
#             'object': obj
#         })