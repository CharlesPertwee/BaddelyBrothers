# -*- coding: utf-8 -*-
{
    'name': "Products Baddeley Brothers",

    'summary': """
        Product Customizations for Baddely Brothers

        """,

    'description': """
    
    """,

    'author': "SquadsoftTech",
    'website': "http://www.squadsoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Baddely Brothers',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','stock','uom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/MaterialSize.xml',
        'views/views.xml',
        'wizards/views/ProductDeletion.xml',
        'views/templates.xml',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
