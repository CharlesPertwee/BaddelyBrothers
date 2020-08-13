# -*- coding: utf-8 -*-

from odoo import http, tools, _
from odoo.http import request, Controller, Response
import requests
import codecs
import datetime
import base64
import json
import pytz
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from psycopg2 import IntegrityError
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import ValidationError

class WebsiteSale(WebsiteSale):
	
	def _checkout_form_save(self, mode, checkout, all_values):
		Partner = request.env['res.partner']
		if mode[0] == 'new':
			checkout.update({'accountStatus':"Open",'onHold':False})
			partner_id = Partner.sudo().create(checkout).id
		elif mode[0] == 'edit':
			partner_id = int(all_values.get('partner_id', 0))
			if partner_id:
				# double check
				order = request.website.sale_get_order()
				shippings = Partner.sudo().search([("id", "child_of", order.partner_id.commercial_partner_id.ids)])
				if partner_id not in shippings.mapped('id') and partner_id != order.partner_id.id:
					return Forbidden()
				Partner.browse(partner_id).sudo().write(checkout)
		return partner_id
