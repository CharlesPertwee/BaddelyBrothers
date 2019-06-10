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
    'depends': ['base','bb_process','bb_products','product','mrp','purchase','project','uom','sale','sale_management','delivery','mrp_account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #'reports/views/EstimateLetter.xml',
        'report/views/JobTicket.xml',
        'views/EstimateLines.xml',
        'views/Estimate.xml',
        'views/EstimateStages.xml',
        'views/EstimateMaterialLink.xml',
        'views/EstimateConditions.xml',
        'views/templates.xml',
        'views/Manufacturing.xml',
        'views/WorkOrders.xml',
        'views/Routing.xml',
        'views/Bom.xml',
        #'reports/views/CostStructure.xml',
        'wizards/views/OrderConvert.xml',
        'data/Stages.xml',
        'data/Estimate.xml',
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}