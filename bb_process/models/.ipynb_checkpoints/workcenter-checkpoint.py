# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class QtyBreakParams(models.Model):
    _name = "bb_process.qty_break_params"
    
    process_id = fields.Many2one('mrp.workcenter','Process')
    
    qty_greater_than = fields.Integer('Quantity Greater Than')
    weight_greater_than = fields.Integer('Weight Greater Than')
    qty_upto = fields.Integer('Quantity Upto')
    make_ready_time = fields.Float('Make Ready Time(Hours)')
    machine_speed = fields.Float('Machine Speed')
    wash_up_time = fields.Float('Wash Up Time(Hours)')
    make_ready_overs = fields.Integer('Make Ready Overs')
    running_overs_percent = fields.Float('Running Overs(%)')
    
    standard_price = fields.Float('Hourly Cost')
    list_price = fields.Float('Hourly Rate')
    
    minimum_price = fields.Float('Minimum Charge', digits=(16,2))
    time_per_pile = fields.Float('Running Time(per pile)',digits=(10,2))
    sheets_per_pile = fields.Integer('Sheets Per Pile')
    margin_percent = fields.Float('Margin(%)')
    process_type = fields.Many2one('bb_process.process',string="Process Type",required=True)
    isDefault = fields.Boolean('Default Breaks')
    
    #_sql_constraints = [('DefaultQtyBreaks', 'unique(process_id, isDefault)', 'Default Quantity Breaks is already set for this process.') ]
    
#     @api.constrains('isDefault')
#     def _check_something(self):
#         for record in self:
#             existingRecord = self.search([('process_id','=',record.process_id.id),('isDefault','=',True)])
#             if record.isDefault and existingRecord:
#                 raise ValidationError("Default Quantity Breaks is already set for this process.")
                
    
class MrpWorkcenter(models.Model):
    _inherit = "mrp.workcenter"
    _name = "mrp.workcenter"
    
    process_type = fields.Many2one('bb_process.process',string="Process Type",required=True)
    qty_break_params = fields.One2many('bb_process.qty_break_params','process_id',string='Quantity Breaks')
    
    standard_description = fields.Text('Description')
    
    standard_price = fields.Float('Hourly Cost', default= 50.00)
    list_price = fields.Float('Hourly Rate', default= 75.00)
    margin_percent = fields.Float('Margin(%)', default= 48.60)
    additional_charge = fields.Float('Misc. Material Charge per 1000', default=10.00)
    misc_charge_per_cm2 = fields.Float('Misc. Material Charge per cm2', default=0.0)
    ink_mix_time = fields.Float('Ink Mix Time (hours)', default=0.28)
    
    associatedBoxId = fields.Many2one('bb_process.boxes',string="Packaging Product")
    sheetsPerBox = fields.Integer('Sheets Per Box')
    timePerBox = fields.Float('Time Per Box')
    paper_type = fields.Selection([('white','White'),('printed','Printed')],string="Paper Type")
    
    
class PackingBoxes(models.Model):
    _name = "bb_process.boxes"
    
    name = fields.Char('Name',required=True)
    customerDescription = fields.Char('Standard Customer Description')
    jobTicketDescription = fields.Char('Standard Job Ticket Description')
    boxWeight = fields.Float('Box Weight(kg)')
    uomId = fields.Many2one('uom.uom',string="Unit of Measure")
    standardCost = fields.Float('Standard Cost')
    standardPrice = fields.Float('Standard Price')
    margin = fields.Float('Margin(%)')