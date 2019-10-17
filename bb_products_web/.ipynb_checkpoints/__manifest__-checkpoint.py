# -*- coding: utf-8 -*-
{
    'name': "ECommerce Baddeley Brothers",

    'summary': """
        Product Customization for ECommerce
        """,

    'description': """
     
     """,

    'author': "SquadsoftTech",
    'website': "http://www.squadsoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Baddely Brothers',
    'version': '4.0',

    # any module necessary for this one to work correctly
    'depends': ['base','website','website_sale','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/Product.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}