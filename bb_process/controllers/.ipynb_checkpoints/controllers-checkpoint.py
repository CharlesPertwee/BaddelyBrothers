# -*- coding: utf-8 -*-
from odoo import http

# class BbProcess(http.Controller):
#     @http.route('/bb_process/bb_process/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bb_process/bb_process/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bb_process.listing', {
#             'root': '/bb_process/bb_process',
#             'objects': http.request.env['bb_process.bb_process'].search([]),
#         })

#     @http.route('/bb_process/bb_process/objects/<model("bb_process.bb_process"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bb_process.object', {
#             'object': obj
#         })