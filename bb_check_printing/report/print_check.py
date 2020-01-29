from odoo import models
from odoo.tools.misc import format_date
from num2words import num2words

class report_print_check(models.Model):
	_inherit = 'account.payment'

	def wordamount(self):
		if self.amount:
			record = [int(x) for x in ('%06d' % (int(self.amount)))]
			data = [num2words(x).capitalize() for x in record ]
			return data
