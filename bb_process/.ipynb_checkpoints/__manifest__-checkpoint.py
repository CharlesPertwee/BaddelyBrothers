# -*- coding: utf-8 -*-
{
    'name': "Processes Baddeley Brothers",

    'summary': """
        This module adds the process type to work centers.
        """,

    'description': """
     
     """,

    'author': "Squadsoft Tech",
    'website': "http://www.squadsoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Baddely Brothers',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/process.xml',
        'views/QuantityBreaks.xml',
        'views/workcenter.xml',
        'views/templates.xml',
        'data/process.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}