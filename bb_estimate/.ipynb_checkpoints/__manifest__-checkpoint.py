# -*- coding: utf-8 -*-
{
    'name': "Estimate Baddely Brothers",

    'summary': """
        This module creates the estimate and job tickets.
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
    'depends': ['base','bb_process','product','mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/EstimateLines.xml',
        'views/Estimate.xml',
        'views/EstimateStages.xml',
        'views/MaterialSize.xml',
        'views/templates.xml',
        'data/Stages.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}