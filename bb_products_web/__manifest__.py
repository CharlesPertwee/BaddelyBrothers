# -*- coding: utf-8 -*-
{
    'name': "ECommerce Baddely Brothers",

    'summary': """
        Product Customization for ECommerce
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "SquadsoftTech",
    'website': "http://www.squadsoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Baddely Brothers',
    'version': '2.0',

    # any module necessary for this one to work correctly
    'depends': ['base','website_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}