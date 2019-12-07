# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api, SUPERUSER_ID, _
from datetime import datetime
from odoo.tools import float_round
#from odoo.addons.mrp.report.mrp_report_bom_structure import ReportBomStructure as Report

class BomStructure(models.AbstractModel):
    _inherit='report.mrp.report_bom_structure'
    
    
    def _get_bom_standard(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        bom = self.env['mrp.bom'].browse(bom_id)
        bom_quantity = line_qty
        if line_id:
            current_line = self.env['mrp.bom.line'].browse(int(line_id))
            bom_quantity = current_line.product_uom_id._compute_quantity(line_qty, bom.product_uom_id)
        # Display bom components for current selected product variant
        if product_id:
            product = self.env['product.product'].browse(int(product_id))
        else:
            product = bom.product_id or bom.product_tmpl_id.product_variant_id
        if product:
            attachments = self.env['mrp.document'].search(['|', '&', ('res_model', '=', 'product.product'),
            ('res_id', '=', product.id), '&', ('res_model', '=', 'product.template'), ('res_id', '=', product.product_tmpl_id.id)])
        else:
            product = bom.product_tmpl_id
            attachments = self.env['mrp.document'].search([('res_model', '=', 'product.template'), ('res_id', '=', product.id)])
        operations = self._get_operation_line(bom.routing_id, (bom_quantity / bom.product_qty), 0)
        lines = {
            'bom': bom,
            'bom_qty': bom_quantity,
            'bom_prod_name': product.display_name,
            'currency': self.env.user.company_id.currency_id,
            'product': product,
            'code': bom and self._get_bom_reference(bom) or '',
            'price': product.uom_id._compute_price(product.standard_price, bom.product_uom_id) * bom_quantity,
            'total': sum([op['total'] for op in operations]),
            'level': level or 0,
            'operations': operations,
            'operations_cost': sum([op['total'] for op in operations]),
            'attachments': attachments,
            'operations_time': sum([op['duration_expected'] for op in operations])
        }
        components, total = self._get_bom_lines(bom, bom_quantity, product, line_id, level)
        lines['components'] = components
        lines['total'] += total
        return lines
    
    def _get_bom_lines_computed(self, bom, bom_quantity, product, line_id, level,estimate):
        components = []
        total = 0
        for line in bom.bom_line_ids:
            if line.EstimateLineId:
                line_quantity = (line.EstimateLineId['quantity_required_'+line.EstimateLineId.estimate_id.selectedQuantity] * line.EstimateLineId.estimate_id.SelectedQtyRatio) + (line.EstimateLineId.quantity_required_run_on * line.EstimateLineId.estimate_id.selectedRatio)
                if line._skip_bom_line(product):
                    continue
                price = (line.EstimateLineId['total_price_'+line.EstimateLineId.estimate_id.selectedQuantity] * line.EstimateLineId.estimate_id.SelectedQtyRatio) + (line.EstimateLineId.total_price_run_on * line.EstimateLineId.estimate_id.selectedRatio)

                if line.child_bom_id:
                    factor = line.product_uom_id._compute_quantity(line_quantity, line.child_bom_id.product_uom_id) * line.child_bom_id.product_qty
                    sub_total = self._get_price(line.child_bom_id, factor)
                else:
                    sub_total = price

                components.append({
                    'prod_id': line.product_id.id,
                    'prod_name': line.product_id.display_name,
                    'code': line.child_bom_id and self._get_bom_reference(line.child_bom_id) or '',
                    'prod_qty': line_quantity,
                    'prod_uom': line.product_uom_id.name,
                    'prod_cost': price,
                    'parent_id': bom.id,
                    'line_id': line.id,
                    'level': level or 0,
                    'total': sub_total,
                    'child_bom': line.child_bom_id.id,
                    'phantom_bom': line.child_bom_id and line.child_bom_id.type == 'phantom' or False,
                    'attachments': self.env['mrp.document'].search(['|', '&',
                        ('res_model', '=', 'product.product'), ('res_id', '=', line.product_id.id), '&', ('res_model', '=', 'product.template'), ('res_id', '=', line.product_id.product_tmpl_id.id)]),

                })
                total += sub_total
        return components, total

    def _get_bom_computed(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False,MO=False):
        bom = self.env['mrp.bom'].browse(bom_id)
        estimate = self.env['bb_estimate.estimate'].sudo().search([('estimate_number','=',bom.code)])
        if estimate:
            estimate = estimate[0]
        
        bom_quantity = estimate.selectedRunOn + (estimate['quantity_'+estimate.selectedQuantity] * estimate.SelectedQtyRatio)
        price = sum([x['total_price_'+estimate.selectedQuantity] for x in estimate.estimate_line.search([('estimate_id','=',estimate.id),('option_type','=','material'),('isExtra','=',False)])]) * estimate.SelectedQtyRatio
        # Display bom components for current selected product variant
        if product_id:
            product = self.env['product.product'].browse(int(product_id))
        else:
            product = bom.product_id or bom.product_tmpl_id.product_variant_id
        
        if product:
            attachments = self.env['mrp.document'].search(['|', '&', ('res_model', '=', 'product.product'),
            ('res_id', '=', product.id), '&', ('res_model', '=', 'product.template'), ('res_id', '=', product.product_tmpl_id.id)])
        else:
            product = bom.product_tmpl_id
            attachments = self.env['mrp.document'].search([('res_model', '=', 'product.template'), ('res_id', '=', product.id)])
        
        operations = self._get_operation_line_computed(bom.routing_id, (bom_quantity / bom.product_qty), 0, bom,MO,estimate)
        lines = {
            'bom': bom,
            'bom_qty': bom_quantity,
            'bom_prod_name': product.display_name,
            'currency': self.env.user.company_id.currency_id,
            'product': product,
            'code': bom and self._get_bom_reference(bom) or '',
            'price': price,
            'total': sum([op['total'] for op in operations]),
            'level': level or 0,
            'operations': operations,
            'operations_cost': sum([op['total'] for op in operations]),
            'attachments': attachments,
            'operations_time': sum([op['duration_expected'] for op in operations])
        }
        components, total = self._get_bom_lines_computed(bom, bom_quantity, product, line_id, level, estimate)
        lines['components'] = components
        lines['total'] += total
        return lines
    
    def _get_operation_line_computed(self, routing, qty, level, Bom=False, MO=False,estimate=False):
        operations = []
        total = 0.0
        for operation in routing.operation_ids:
            if operation.EstimateLineId:
                duration_expected = (operation.EstimateLineId['quantity_required_'+operation.EstimateLineId.estimate_id.selectedQuantity] * operation.EstimateLineId.estimate_id.SelectedQtyRatio) + (operation.EstimateLineId['quantity_required_run_on'] * operation.EstimateLineId.estimate_id.selectedRatio)
                total = (operation.EstimateLineId['total_price_'+operation.EstimateLineId.estimate_id.selectedQuantity] * operation.EstimateLineId.estimate_id.SelectedQtyRatio) + (operation.EstimateLineId['total_price_run_on'] * operation.EstimateLineId.estimate_id.selectedRatio)

                operations.append({
                    'level': level or 0,
                    'operation': operation,
                    'name': operation.name + ' - ' + operation.workcenter_id.name,
                    'duration_expected': duration_expected,
                    'total': float_round(total, precision_rounding=self.env.user.company_id.currency_id.rounding),
                })
        return operations

    def _get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        bom = self.env['mrp.bom'].sudo().search([('id','=',bom_id)])
        if bom:
            mo = self.env['bb_estimate.estimate'].sudo().search([('estimate_number','=',bom[0].code)])
            if mo:
                return self._get_bom_computed(bom_id,product_id,line_qty,line_id,level)
            else:
                return self._get_bom_standard(bom_id,product_id,line_qty,line_id,level)
    
    @api.model
    def get_operations(self, bom_id=False, qty=0, level=0):
        bom = self.env['mrp.bom'].browse(bom_id)
        estimate = self.env['bb_estimate.estimate'].sudo().search([('estimate_number','=',bom.code)])
        if estimate:
            lines = self._get_operation_line_computed(bom.routing_id, qty, level, bom,estimate=estimate)
            values = {
                'bom_id': bom_id,
                'currency': self.env.user.company_id.currency_id,
                'operations': lines,
            }
        else:
            lines = self._get_operation_line(bom.routing_id, qty, level)
            values = {
                'bom_id': bom_id,
                'currency': self.env.user.company_id.currency_id,
                'operations': lines,
            }
        return self.env.ref('mrp.report_mrp_operation_line').render({'data': values})
    
    def _get_pdf_line(self, bom_id, product_id=False, qty=1, child_bom_ids=[], unfolded=False):
        
        data = self._get_bom(bom_id=bom_id, product_id=product_id, line_qty=qty)
        
        def get_sub_lines(bom, product_id, line_qty, line_id, level):
            data = self._get_bom(bom_id=bom.id, product_id=product_id, line_qty=line_qty, line_id=line_id, level=level)
            bom_lines = data['components']
            lines = []
            for bom_line in bom_lines:
                lines.append({
                    'name': bom_line['prod_name'],
                    'type': 'bom',
                    'quantity': bom_line['prod_qty'],
                    'uom': bom_line['prod_uom'],
                    'prod_cost': bom_line['prod_cost'],
                    'bom_cost': bom_line['total'],
                    'level': bom_line['level'],
                    'code': bom_line['code']
                })
                if bom_line['child_bom'] and (unfolded or bom_line['child_bom'] in child_bom_ids):
                    line = self.env['mrp.bom.line'].browse(bom_line['line_id'])
                    lines += (get_sub_lines(line.child_bom_id, line.product_id, line.product_qty * data['bom_qty'], line, level + 1))
            if data['operations']:
                lines.append({
                    'name': _('Operations'),
                    'type': 'operation',
                    'quantity': data['operations_time'],
                    'uom': _('minutes'),
                    'bom_cost': data['operations_cost'],
                    'level': level,
                })
                for operation in data['operations']:
                    if unfolded or 'operation-' + str(bom.id) in child_bom_ids:
                        lines.append({
                            'name': operation['name'],
                            'type': 'operation',
                            'quantity': operation['duration_expected'],
                            'uom': _('minutes'),
                            'bom_cost': operation['total'],
                            'level': level + 1,
                        })
            return lines

        bom = self.env['mrp.bom'].browse(bom_id)
        product = product_id or bom.product_id or bom.product_tmpl_id.product_variant_id
        pdf_lines = get_sub_lines(bom, product, qty, False, 1)
        data['components'] = []
        data['lines'] = pdf_lines
        return data