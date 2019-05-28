# -*- coding: utf-8 -*-
from odoo import http

# class BbEstimate(http.Controller):
#     @http.route('/bb_estimate/bb_estimate/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bb_estimate/bb_estimate/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bb_estimate.listing', {
#             'root': '/bb_estimate/bb_estimate',
#             'objects': http.request.env['bb_estimate.bb_estimate'].search([]),
#         })

#     @http.route('/bb_estimate/bb_estimate/objects/<model("bb_estimate.bb_estimate"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bb_estimate.object', {
#             'object': obj
#         })