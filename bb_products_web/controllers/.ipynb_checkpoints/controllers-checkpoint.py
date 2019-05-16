# -*- coding: utf-8 -*-
from odoo import http
import math
import json
import logging
from werkzeug.exceptions import Forbidden, NotFound

from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.website.controllers.main import QueryURL
from odoo.exceptions import ValidationError
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.osv import expression

_logger = logging.getLogger(__name__)

PPG = 20  # Products Per Page
PPR = 4   # Products Per Row
class WebsiteSalesBB(WebsiteSale):
    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        
        
        order = request.website.sale_get_order(force_create=1)
        if order.state != 'draft':
            request.website.sale_reset()
            return {}
        
        line_product = order.order_line.search([('id','=',product_id)])
        roundOff = line_product.product_id.roundOff if line_product.product_id.roundOff > 0 else 100
        set_qty = math.ceil(set_qty/roundOff) * roundOff
        
        value = order._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty)
        
        if not order.cart_quantity:
            request.website.sale_reset()
            return value

        order = request.website.sale_get_order()
        value['cart_quantity'] = order.cart_quantity
        from_currency = order.company_id.currency_id
        to_currency = order.pricelist_id.currency_id

        if not display:
            return value

        value['website_sale.cart_lines'] = request.env['ir.ui.view'].render_template("website_sale.cart_lines", {
            'website_sale_order': order,
            # compute_currency deprecated (not used in view)
            'compute_currency': lambda price: from_currency._convert(
                price, to_currency, order.company_id, fields.Date.today()),
            'date': fields.Date.today(),
            'suggested_products': order._cart_accessories()
        })
        value['website_sale.short_cart_summary'] = request.env['ir.ui.view'].render_template("website_sale.short_cart_summary", {
            'website_sale_order': order,
            'compute_currency': lambda price: from_currency._convert(
                price, to_currency, order.company_id, fields.Date.today()),
        })
        return value
    
    @http.route(['/product_configurator/get_combination_info'], type='json', auth="user", methods=['POST'])
    def get_combination_info(self, product_template_id, product_id, combination, add_qty, pricelist_id, **kw):
        combination = request.env['product.template.attribute.value'].browse(combination)
        pricelist = self._get_pricelist(pricelist_id)
        ProductTemplate = request.env['product.template']
        if 'context' in kw:
            ProductTemplate = ProductTemplate.with_context(**kw.get('context'))
        product = ProductTemplate.browse(int(product_template_id))  
        roundOff = product.roundOff if product.roundOff > 0 else 100
        add_qty = math.ceil(add_qty/roundOff) * roundOff
        
        data = product._get_combination_info(combination, int(product_id or 0), int(add_qty or 1), pricelist)
        data["quantity"] = add_qty
        data["roundOff"] = roundOff
        return data
    
    @http.route(['/product_configurator/get_combination_info_website'], type='json', auth="public", methods=['POST'], website=True)
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, **kw):
        """Special route to use website logic in get_combination_info override.
        This route is called in JS by appending _website to the base route.
        """
        kw.pop('pricelist_id')
        res = self.get_combination_info(product_template_id, product_id, combination, add_qty, request.website.get_current_pricelist(), **kw)
        product = request.env['product.template'].sudo().search([('id', '=', product_template_id)])
        roundOff = product.roundOff if product.roundOff > 0 else 100
        add_qty = math.ceil(add_qty/roundOff) * roundOff
        if request.env.ref('website_sale.shop_product_carousel', raise_if_not_found=False):  # IF for compatibility 12.0
            res.update(carousel=request.env['ir.ui.view'].render_template('website_sale.shop_product_carousel', 
            values={
                'product': request.env['product.template'].browse(res['product_template_id']),
                'product_variant': request.env['product.product'].browse(res['product_id']),
                'quantity': add_qty,
                'roundOff': roundOff
            }))
        return res

