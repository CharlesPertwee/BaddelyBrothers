# -*- coding: utf-8 -*-
import odoo
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError
from datetime import datetime
from datetime import timedelta

class DispatchDate(models.TransientModel):
	_name = "bb_estimate.dispatch_date"

	target_dispatch_Date = fields.Date('Target Dispatch Date', default=lambda self: (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'))
	Estimate = fields.Many2one('bb_estimate.estmate')

	def confirm(self):
		if self.Estimate:
			self.Estimate.write({'target_dispatch_Date': self.target_dispatch_Date})

			if self.Estimate.salesOrder:
				pickings = self.Estimate.salesOrder.picking_ids.filterred(lambda x: x.state not in ['done', 'cancel'])
				pickings.write({'scheduled_date': self.target_dispatch_Date})


