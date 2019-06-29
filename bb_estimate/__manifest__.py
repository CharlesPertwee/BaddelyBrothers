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
    'depends': ['base','web','bb_crm','crm','bb_process','bb_products','product','mrp','purchase','project','uom','sale','sale_management','delivery','mrp_account','account','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/Stages.xml',
        'data/Estimate.xml',
        'data/Manufacturing.xml',
        'reports/views/EstimateLetter.xml',
        'reports/views/JobTicket.xml',
        'reports/views/BoxLabel.xml',
        'reports/views/AsBeforeLetter.xml',
        'reports/views/DieLabel.xml',
        'reports/views/InvoiceReport.xml',
        'reports/views/ProForma.xml',
        'reports/views/CreditNote.xml',
        'reports/views/CreditNoteHeaded.xml',
        'reports/views/PurchaseOrder.xml',
        'reports/views/RequestQuote.xml',
        'reports/views/ProFormaHeaded.xml',
        'reports/views/InvoiceHeaded.xml',
        'reports/views/DeliveryNote.xml',
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
        'views/SalesOrder.xml',
        'views/Invoice.xml',
        'views/PurchaseOrder.xml',
        'views/Specification.xml',
        'views/Projects.xml',
        'views/CRM.xml',
        'wizards/views/OrderConvert.xml',
        'wizards/views/MoConfirmation.xml',
        'wizards/views/Packing.xml',
        'wizards/views/PriceAdjustment.xml',
        'wizards/views/SalesAdjustment.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}