from odoo import api, models


class MrpCostStructure(models.AbstractModel):
    _inherit = 'report.mrp_account.mrp_cost_structure'
    
    def get_lines_standard(self, productions):
        ProductProduct = self.env['product.product']
        StockMove = self.env['stock.move']
        res = []
        for product in productions.mapped('product_id'):
            mos = productions.filtered(lambda m: m.product_id == product)
            total_cost = 0.0

            #get the cost of operations
            operations = []
            Workorders = self.env['mrp.workorder'].search([('production_id', 'in', mos.ids)])
            if Workorders:
                query_str = """SELECT w.operation_id, op.name, partner.name, sum(t.duration), wc.costs_hour
                                FROM mrp_workcenter_productivity t
                                LEFT JOIN mrp_workorder w ON (w.id = t.workorder_id)
                                LEFT JOIN mrp_workcenter wc ON (wc.id = t.workcenter_id )
                                LEFT JOIN res_users u ON (t.user_id = u.id)
                                LEFT JOIN res_partner partner ON (u.partner_id = partner.id)
                                LEFT JOIN mrp_routing_workcenter op ON (w.operation_id = op.id)
                                WHERE t.workorder_id IS NOT NULL AND t.workorder_id IN %s
                                GROUP BY w.operation_id, op.name, partner.name, t.user_id, wc.costs_hour
                                ORDER BY op.name, partner.name
                            """
                self.env.cr.execute(query_str, (tuple(Workorders.ids), ))
                for op_id, op_name, user, duration, cost_hour in self.env.cr.fetchall():
                    operations.append([user, op_id, op_name, duration / 60.0, cost_hour])

            #get the cost of raw material effectively used
            raw_material_moves = []
            query_str = """SELECT product_id, bom_line_id, SUM(product_qty), abs(SUM(price_unit * product_qty))
                            FROM stock_move WHERE raw_material_production_id in %s AND state != 'cancel'
                            GROUP BY bom_line_id, product_id"""
            self.env.cr.execute(query_str, (tuple(mos.ids), ))
            for product_id, bom_line_id, qty, cost in self.env.cr.fetchall():
                raw_material_moves.append({
                    'qty': qty,
                    'cost': cost,
                    'product_id': ProductProduct.browse(product_id),
                    'bom_line_id': bom_line_id
                })
                total_cost += cost

            #get the cost of scrapped materials
            scraps = StockMove.search([('production_id', 'in', mos.ids), ('scrapped', '=', True), ('state', '=', 'done')])
            uom = mos and mos[0].product_uom_id
            mo_qty = 0
            if not all(m.product_uom_id.id == uom.id for m in mos):
                uom = product.uom_id
                for m in mos:
                    qty = sum(m.mapped('move_finished_ids.product_qty'))
                    if m.product_uom_id.id == uom.id:
                        mo_qty += qty
                    else:
                        mo_qty += m.product_uom_id._compute_quantity(qty, uom)
            else:
                mo_qty = sum(mos.mapped('move_finished_ids.product_qty'))
            res.append({
                'product': product,
                'mo_qty': mo_qty,
                'mo_uom': uom,
                'operations': operations,
                'currency': self.env.user.company_id.currency_id,
                'raw_material_moves': raw_material_moves,
                'total_cost': total_cost,
                'scraps': scraps,
                'mocount': len(mos),
                'sub_product_moves': []
            })
        return res
    
    def get_lines_computed(self, production):
        ProductProduct = self.env['product.product']
        StockMove = self.env['stock.move']
        
        estimate = False
        #operations
        operations = []
        for workorder in production.workorder_ids:
            if workorder.operation_id.EstimateLineId.estimate_id:
                if not estimate:
                    estimate = workorder.operation_id.EstimateLineId.estimate_id
                
                estimate_line = workorder.operation_id.EstimateLineId
                
                unitPrice = (estimate_line['total_price_'+estimate.selectedQuantity] + (estimate_line.total_price_run_on * estimate.selectedRatio)) / (estimate_line['quantity_required_'+estimate.selectedQuantity] + (estimate_line.quantity_required_run_on * estimate.selectedRatio))
                working_time = sum([x.duration for x in workorder.time_ids])

                if working_time < workorder.ActualTime:
                    working_time = workorder.ActualTime

                operations.append(['', workorder.operation_id, workorder.operation_id.name,round(working_time,2), round(unitPrice ,2)])
        
        #products
        raw_material_moves = []
        materialComputed = []
        total_cost = 0
        for product in production.move_raw_ids:
            if product.product_uom_qty > 0:
                estimate_line = estimate.estimate_line.search([('quantity_required_'+estimate.selectedQuantity,'>',0),('estimate_id','=',estimate.id),('option_type','=','material'),('material','=',product.product_id.id),('id','not in',materialComputed)])
                if estimate_line:
                    estimate_line = estimate_line[0]
                materialComputed.append(estimate_line.id)   

                m_qty = 0
                for x in production.workorder_ids:
                    m_qty += sum([y.MaterialUsed for y in x.EstimateMaterials if y.EstimateLineId.id == estimate_line.id])

                unitPrice = (estimate_line['total_price_'+estimate.selectedQuantity] + (estimate_line.total_price_run_on * estimate.selectedRatio)) / (estimate_line['quantity_required_'+estimate.selectedQuantity] + (estimate_line.quantity_required_run_on *estimate.selectedRatio))
                total_cost += (m_qty * unitPrice)
                bom_line_id = production.bom_id.search([('id','=',production.bom_id.id),('product_id','=',product.product_id.id)])
                raw_material_moves.append({
                        'qty': m_qty,
                        'cost': m_qty * unitPrice,
                        'product_id': product.product_id,
                        'bom_line_id': bom_line_id
                    })
        
        if estimate:
            product = production.mapped('product_id')
            uom = product.uom_id
            qty = sum(production.mapped('move_finished_ids.product_qty'))
            mo_qty = production.product_uom_id._compute_quantity(qty, uom)
        #get the cost of scrapped materials
        scraps = StockMove.search([('production_id', '=', production.id), ('scrapped', '=', True), ('state', '=', 'done')])
        res = {
                'product': product,
                'mo_qty': mo_qty,
                'mo_uom': uom,
                'operations': operations,
                'currency': self.env.user.company_id.currency_id,
                'raw_material_moves': raw_material_moves,
                'total_cost': total_cost,
                'scraps': scraps,
                'mocount': 1,
                'sub_product_moves': []
            }
        
        return res
    
    @api.multi
    def get_lines(self, productions):
        non_estimates = productions.filtered(lambda r: r.origin != 'Estimate Workflow')
        estimates = productions.filtered(lambda r: r.origin == 'Estimate Workflow')
        res = []
        for estimate in estimates:
            res.append(self.get_lines_computed(estimate))
        res.extend(self.get_lines_standard(non_estimates))
        return res