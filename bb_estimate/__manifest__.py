# -*- coding: utf-8 -*-
{
    'name': "Estimate Baddeley Brothers",

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
    'version': '1.2',

    # any module necessary for this one to work correctly
    'depends': ['base','web','hr_timesheet','website_crm','bb_crm','crm','bb_process','bb_products','product','mrp','purchase','project','uom','sale','sale_management','delivery','mrp_account','account','stock','sale_crm','purchase_stock','account'],

    # always loaded
    'data': [
        'data/Groups.xml',
        'security/ir.model.access.csv',
        'data/Stages.xml',
        'data/Estimate.xml',
        'data/Manufacturing.xml',
        'data/WebToLead.xml',
        'data/StockPicking.xml',
        'reports/views/EstimateLetter.xml',
        'reports/views/JobTicket.xml',
        'reports/views/BoxLabel.xml',
        'reports/views/AsBeforeLetter.xml',
        'reports/views/DieLabel.xml',
        'reports/views/InvoiceReport.xml',
        'reports/views/SaleQuote.xml',
        'reports/views/ProForma.xml',
        'reports/views/CreditNote.xml',
        'reports/views/CreditNoteHeaded.xml',
        'reports/views/PurchaseOrder.xml',
        'reports/views/RequestQuote.xml',
        'reports/views/ProFormaHeaded.xml',
        'reports/views/InvoiceHeaded.xml',
        'reports/views/DeliveryNote.xml',
        'reports/views/CustomDeliveryNoteWithoutLine.xml',
        'reports/views/CustomDeliveryNoteWithLines.xml',
        'reports/views/EnquiryConversionReport.xml',
        'reports/views/EnquiryMonthlyRates.xml',
        'reports/views/EnquiryTimesReport.xml',
        'reports/views/DeliverySlip.xml',
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
        'data/sale_order_mail_template.xml',
        'views/Invoice.xml',
        'data/invoice_mail_template.xml',
        'views/PurchaseOrder.xml',
        'data/purchase_mail_template.xml',
        'views/Specification.xml',
        'views/StockPicking.xml',
        'views/Projects.xml',
        'views/CRM.xml',
        'views/Accounting.xml',
        'wizards/views/OrderConvert.xml',
        'wizards/views/MoConfirmation.xml',
        'wizards/views/Packing.xml',
        'wizards/views/Invoice.xml',
        'wizards/views/PriceAdjustment.xml',
        'wizards/views/SalesAdjustment.xml',
        'wizards/views/AmmendQty.xml',
        'wizards/views/DeliveryNote.xml',
        'reports/views/EstimateConversionReport.xml',
        'reports/views/EstimateMonthlyRates.xml',
        'reports/views/EstimateTimesReport.xml',
        'reports/views/TicketTimesReport.xml',
        'reports/views/PurchaseDayReport.xml',
        'reports/views/OnTimeDelivery.xml',
        'reports/views/DeliveryPerformance.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
