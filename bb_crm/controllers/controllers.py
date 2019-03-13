# -*- coding: utf-8 -*-
from odoo import http

# class BbCrm(http.Controller):
#     @http.route('/bb_crm/bb_crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bb_crm/bb_crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bb_crm.listing', {
#             'root': '/bb_crm/bb_crm',
#             'objects': http.request.env['bb_crm.bb_crm'].search([]),
#         })

#     @http.route('/bb_crm/bb_crm/objects/<model("bb_crm.bb_crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bb_crm.object', {
#             'object': obj
#         })