# -*- coding: utf-8 -*-

from odoo import models, fields, api


ACCOUNT_STATUS = [
    ('Open','Open'),
    ('New Customer - Awaiting Credit Approval','New Customer - Awaiting Credit Approval'),
    ('New Account','New Account'),
    ('Cash/chq on delievery only','Cash/chq on delievery only'),
    ('Settle a/c prior to ordering','Settle a/c prior to ordering'),
    ('On stop - see DP or CP','On stop - see DP or CP'),
    ('In court - on stop','In court - on stop'),
    ('In liquidation on stop','In liquidation on stop'),
    ('Closed','Closed'),
    ('Delete Account','Delete Account')
]

class Sales(models.Model):
    _inherit = "sale.order"
    
    Project = fields.Many2one('project.project','Project')
    Estimate = fields.Many2one('bb_estimate.estimate',string='Originating Estimate',ondelete='restrict')
    EstimateTitle = fields.Char("Job Title", related="Estimate.title")
    JobTicket = fields.Many2one('mrp.production',string="Job Ticket")
    partnerOnHold = fields.Boolean('Account on Hold',compute="compute_hold")
    partnerStatus = fields.Selection(ACCOUNT_STATUS,compute="compute_hold")
    priceHistory = fields.One2many('bb_estimate.price_history','SalesOrder','Price Adjustments')
    ProFormaLines = fields.Html('Pro-Forma Line')
    orderStatus = fields.Selection([('To Deliver', 'To Deliver'),('Delivered', 'Delivered'), ('To Invoice', 'To Invoice'),('Fully Invoiced', 'Fully Invoiced')],string='Order Status',default='To Deliver')
    orderDelivered = fields.Boolean("Order Delivered",compute="DeliverOrder")

    @api.depends("order_line")
    def DeliverOrder(self):
        for record in self:
            if record.order_line:
                record.orderDelivered = all([x for x in map(lambda x: bool(x.qty_delivered>=x.product_uom_qty),record.order_line)])
                if record.orderDelivered and record.orderStatus == "To Deliver":
                    record.write({"orderStatus":'Delivered'})

    @api.onchange('partner_id')
    def compute_hold(self):
        for record in self:
            if record.partner_id:
                if record.partner_id.onHold or (record.partner_id.company_type == 'person' and record.partner_id.parent_id.onHold):
                    record.partnerOnHold = True
                    record.partnerStatus = record.partner_id.partner_id.accountStatus if record.partner_id.company_type == 'person' else record.partner_id.accountStatus
                else:
                    record.partnerOnHold = False

    
    def AdjustPrice(self):
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'name': 'Adjust Price',
                'res_model' : 'bb_estimate.adjust_price_so',
                'type' : 'ir.actions.act_window',
                'context' : "{'default_SalesOrder' : active_id}",
                'target' : 'new',
            }
    
    @api.model
    def create(self,vals):
        if 'Estimate' in vals.keys():
            Estimate = self.env['bb_estimate.estimate'].browse(vals['Estimate'])
            vals['ProFormaLines'] = "<br/>".join([x.customer_description for x in Estimate.estimate_line if isinstance(x.customer_description,str) and (not x.isExtra)])

        order = super(Sales,self).create(vals)
        order.compute_hold()
        return order
    
    def EditProFormaLine(self):
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'name': 'Edit',
                'res_model' : 'invoice.edit_lines',
                'type' : 'ir.actions.act_window',
                'context' : "{'default_SaleOrder' : active_id}",
                'target' : 'new',
            }
    
    @api.multi
    def action_quotation_send(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('sale', 'email_template_edi_sale')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'report_template':'account_pro_forma_headed',
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    
    