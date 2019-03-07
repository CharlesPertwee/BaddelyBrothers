# -*- coding: utf-8 -*-
from odoo import http

# class BbContacts(http.Controller):
#     @http.route('/bb_contacts/bb_contacts/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bb_contacts/bb_contacts/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bb_contacts.listing', {
#             'root': '/bb_contacts/bb_contacts',
#             'objects': http.request.env['bb_contacts.bb_contacts'].search([]),
#         })

#     @http.route('/bb_contacts/bb_contacts/objects/<model("bb_contacts.bb_contacts"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bb_contacts.object', {
#             'object': obj
#         })