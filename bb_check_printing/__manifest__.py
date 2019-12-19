# -*- coding: utf-8 -*-
{
    'name': 'BB Checks Layout',
    'version': '1.0',
    'author': 'Odoo SA, OERP Canada',
    'category': 'Accounting',
    'summary': 'Print BB Checks',
    'description': """
This module allows to print your payments on pre-printed checks.
You can configure the output (layout, stubs, paper format, etc.) in company settings, and manage the
checks numbering (if you use pre-printed checks without numbers) in journal settings.

Supported formats
-----------------
- Check on top : Quicken / QuickBooks standard
- Check on middle: Peachtree standard
- Check on bottom: ADP standard
    """,
    'website': 'https://www.odoo.com/page/accounting',
    'depends': ['account_check_printing', 'l10n_uk'],
    'data': [
        'data/bb_uk_check_printing.xml',
        'report/views/print_check.xml',
        'report/views/print_check_top.xml',
        'report/views/print_check_middle.xml',
        'report/views/print_check_bottom.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
