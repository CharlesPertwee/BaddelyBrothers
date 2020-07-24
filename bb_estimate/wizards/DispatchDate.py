# -*- coding: utf-8 -*-
import odoo
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError
from datetime import datetime
from datetime import timedelta

class DispatchDate(models.TransientModel):
	_name = "bb_estimate.dispatch_date"

	target_dispatch_Date = fields.Date('Target Dispatch Date', default=lambda self: (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'))
	Estimate = fields.Many2one('bb_estimate.estimate')

	def confirm(self):
		if self.Estimate:
			self.Estimate.sudo().write({'target_dispatch_date': self.target_dispatch_Date})
			
			self.Estimate.message_post(body="Target Dispatch Date has been updated.")

			if self.Estimate.salesOrder:
				pickings = self.Estimate.salesOrder.picking_ids.sudo().filtered(lambda x: x.state not in ['done', 'cancel'])
				pickings.sudo().write({'scheduled_date': fields.Datetime.to_string( self.target_dispatch_Date) })


