# -*- coding: utf-8 -*-

from odoo import models, api

class account_payment(models.Model):
	_inherit = "account.payment"

	@api.multi
	def do_print_checks(self):
		if self:
			check_layout = self[0].company_id.account_check_printing_layout
			if check_layout != 'disabled' and self[0].journal_id.company_id.country_id.code == "GB":
				self.write({'state' : 'sent'})
				return self.env.ref('bb_check_printing.%s' % check_layout).report_action(self)
		return super(account_payment, self).do_print_checks()
