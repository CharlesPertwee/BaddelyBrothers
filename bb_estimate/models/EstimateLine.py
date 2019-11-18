# -*- coding: utf-8 -*-

from odoo import models, fields, api
import math
from datetime import datetime
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError

DIE_SIZES = [
    ('none', ''),
    ('standard','No Die (No Charge)'),
    ('small','Crest Die'),
    ('medium','Heading Die'),
    ('large','Invitation Die')
]

DUPLEX_OPTIONS = [
    ('none', ''),
    ('two', '2 Sheets'),
    ('three', '3 Sheets'),
    ('four', '4 Sheets'),
    ('five', '5 Sheets'),
]

LINE_DOCUMENT_CATEGORIES = [
    ('none', ''),
    ('Origination', 'Origination'),
    ('Material', 'Material'),
    ('Process','Process'),
    ('Finishing','Finishing'),
    ('Packing','Packing'),
    ('Despatch','Despatch'),
]

class EstimateLine(models.Model):
    _name = 'bb_estimate.estimate_line'
    _rec_name = 'lineName'
    _description = 'Estimate Lines'
    _order = "Sequence, id"
    
    workcenterId = fields.Many2one('mrp.workcenter', string="Process")
    material = fields.Many2one('product.product', string="Materials")
    estimate_id = fields.Many2one('bb_estimate.estimate','Estimate')
    isEnvelope = fields.Boolean('Is Envelope',related="estimate_id.product_type.isEnvelope")
    
    isExtra = fields.Boolean('Extra')
    extraDescription = fields.Char('Extra Description')
    
    lineName = fields.Char(string='Process/Material',compute="_computeName")
    customer_description = fields.Char(string="Customer Description")
    documentCatergory = fields.Selection(LINE_DOCUMENT_CATEGORIES,'Letter Category')
    JobTicketText = fields.Char('Job Ticket Text')
    StandardCustomerDescription = fields.Char('Standard Customer Description')
    StandardJobDescription = fields.Char('Standard Job Ticket Text')
    UseStadandardDescription = fields.Boolean('Use Standard Descriptions?')
    Details = fields.Text('Details and Notes')
    EstimatorNotes = fields.Text('Notes for Estimator')
    
    quantity_1 = fields.Integer('Quantity 1', related="estimate_id.quantity_1")#store=True, compute="getEstimateParams")
    quantity_2 = fields.Integer('Quantity 2', related="estimate_id.quantity_2")#store=True, compute="getEstimateParams")
    quantity_3 = fields.Integer('Quantity 3', related="estimate_id.quantity_3")#store=True, compute="getEstimateParams")
    quantity_4 = fields.Integer('Quantity 4', related="estimate_id.quantity_4")#store=True, compute="getEstimateParams")
    run_on = fields.Integer('Run On', related="estimate_id.run_on")#store=True, compute="getEstimateParams")
    
    # Parameters for calculation
    param_make_ready_time_1 = fields.Float('Make Ready Time (hours) Qty 1', digits=(10,2))
    param_make_ready_time_2 = fields.Float('Make Ready Time (hours) Qty 2', digits=(10,2))
    param_make_ready_time_3 = fields.Float('Make Ready Time (hours) Qty 3', digits=(10,2))
    param_make_ready_time_4 = fields.Float('Make Ready Time (hours) Qty 4', digits=(10,2))
    param_make_ready_time_run_on = fields.Float('Make Ready Time (hours) Run On', digits=(10,2))
    req_param_make_ready_time = fields.Boolean('Req Make Ready Time (hours)')
    
    param_machine_speed_1 = fields.Float('Machine Speed Qty 1', digits=(10,2))
    param_machine_speed_2 = fields.Float('Machine Speed Qty 2', digits=(10,2))
    param_machine_speed_3 = fields.Float('Machine Speed Qty 3', digits=(10,2))
    param_machine_speed_4 = fields.Float('Machine Speed Qty 4', digits=(10,2))
    param_machine_speed_run_on = fields.Float('Machine Speed Run On', digits=(10,2))
    req_param_machine_speed = fields.Boolean('Req Machine Speed')
    
    param_running_time_1 = fields.Float('Running Time Qty 1', digits=(10,2))
    param_running_time_2 = fields.Float('Running Time Qty 2', digits=(10,2))
    param_running_time_3 = fields.Float('Running Time Qty 3', digits=(10,2))
    param_running_time_4 = fields.Float('Running Time Qty 4', digits=(10,2))
    param_running_time_run_on = fields.Float('Running Time Run On', digits=(10,2))
    req_param_running_time = fields.Boolean('Req Machine Speed')
    
    param_wash_up_time_1 = fields.Float('Wash Up Time (hours) Qty 1', digits=(10,2))
    param_wash_up_time_2 = fields.Float('Wash Up Time (hours) Qty 2', digits=(10,2))
    param_wash_up_time_3 = fields.Float('Wash Up Time (hours) Qty 3', digits=(10,2))
    param_wash_up_time_4 = fields.Float('Wash Up Time (hours) Qty 4', digits=(10,2))
    param_wash_up_time_run_on = fields.Float('Wash Up Time (hours) Run On', digits=(10,2))
    req_param_wash_up_time = fields.Boolean('Req Wash Up Time (hours)')
    
    param_make_ready_overs_1 = fields.Integer('Make Ready Overs Qty 1')
    param_make_ready_overs_2 = fields.Integer('Make Ready Overs Qty 2')
    param_make_ready_overs_3 = fields.Integer('Make Ready Overs Qty 3')
    param_make_ready_overs_4 = fields.Integer('Make Ready Overs Qty 4')
    param_make_ready_overs_run_on = fields.Integer('Make Ready Overs Run On')
    req_param_make_ready_overs = fields.Boolean('Req Make Ready Overs')
    
    param_running_overs_percent_1 = fields.Float('Running Overs (%) Qty 1', digits=(10,2))
    param_running_overs_percent_2 = fields.Float('Running Overs (%) Qty 2', digits=(10,2))
    param_running_overs_percent_3 = fields.Float('Running Overs (%) Qty 3', digits=(10,2))
    param_running_overs_percent_4 = fields.Float('Running Overs (%) Qty 4', digits=(10,2))
    param_running_overs_percent_run_on = fields.Float('Running Overs (%) Run On', digits=(10,2))
    req_param_running_overs_percent = fields.Boolean('Req Running Overs')
    
    unallocated_finished_quantity_1 = fields.Integer('Unallocated Finished Quantity Qty 1')
    unallocated_finished_quantity_2 = fields.Integer('Unallocated Finished Quantity Qty 2')
    unallocated_finished_quantity_3 = fields.Integer('Unallocated Finished Quantity Qty 3')
    unallocated_finished_quantity_4 = fields.Integer('Unallocated Finished Quantity Qty 4')
    unallocated_finished_quantity_run_on = fields.Integer('Unallocated Finished Quantity Run On')
    req_unallocated_finished_quantity = fields.Boolean('Req Unallocated Finished Quantity')
    
    param_finished_quantity_1 = fields.Integer('Material Finished Quantity Qty 1')
    param_finished_quantity_2 = fields.Integer('Material Finished Quantity Qty 2')
    param_finished_quantity_3 = fields.Integer('Material Finished Quantity Qty 3')
    param_finished_quantity_4 = fields.Integer('Material Finished Quantity Qty 4')
    param_finished_quantity_run_on = fields.Integer('Material Finished Quantity Run On')
    req_param_finished_quantity = fields.Boolean('Req Material Finished Quantity')
    
    quantity_required_1 = fields.Float('Quantity/Hours Qty 1', digits=(10,2))
    quantity_required_2 = fields.Float('Quantity/Hours Qty 2', digits=(10,2))
    quantity_required_3 = fields.Float('Quantity/Hours Qty 3', digits=(10,2))
    quantity_required_4 = fields.Float('Quantity/Hours Qty 4', digits=(10,2))
    quantity_required_run_on = fields.Float('Quantity/Hours Run On', digits=(10,2))
    req_quantity_required = fields.Boolean('Req Quantity/Hours')
    
    cost_per_unit_1 = fields.Float('Cost Rate (GBP) Qty 1', digits=(16,6))
    cost_per_unit_2 = fields.Float('Cost Rate (GBP) Qty 2', digits=(16,6))
    cost_per_unit_3 = fields.Float('Cost Rate (GBP) Qty 3', digits=(16,6))
    cost_per_unit_4 = fields.Float('Cost Rate (GBP) Qty 4', digits=(16,6))
    cost_per_unit_run_on = fields.Float('Cost Rate (GBP) Run On', digits=(16,6))
    req_cost_per_unit = fields.Boolean('Req Cost Rate (GBP)')
    
    price_per_unit_1 = fields.Float('Charge Rate (GBP) Qty 1', digits=(16,6))       
    price_per_unit_2 = fields.Float('Charge Rate (GBP) Qty 2', digits=(16,6))      
    price_per_unit_3 = fields.Float('Charge Rate (GBP) Qty 3', digits=(16,6))
    price_per_unit_4 = fields.Float('Charge Rate (GBP) Qty 4', digits=(16,6))
    price_per_unit_run_on = fields.Float('Charge Rate (GBP) Run On', digits=(16,6))
    req_price_per_unit = fields.Boolean('Req Charge Rate (GBP) ')
    
    margin_1 = fields.Float('Margin (%) Qty 1', digits=(10,2))
    margin_2 = fields.Float('Margin (%) Qty 2', digits=(10,2))
    margin_3 = fields.Float('Margin (%) Qty 3', digits=(10,2))
    margin_4 = fields.Float('Margin (%) Qty 4', digits=(10,2))
    margin_run_on = fields.Float('Margin (%) Run On', digits=(10,2))
    req_margin = fields.Boolean('Req Margin')
    
    total_cost_1 = fields.Float('Cost Qty 1', digits=(16,2))
    total_cost_2 = fields.Float('Cost Qty 2', digits=(16,2))
    total_cost_3 = fields.Float('Cost Qty 3', digits=(16,2))
    total_cost_4 = fields.Float('Cost Qty 4', digits=(16,2))
    total_cost_run_on = fields.Float('Cost Run On', digits=(16,2))
    req_total_cost = fields.Boolean('Req Cost')
    
    mat_charge_1 = fields.Float('Material Charge Qty 1', digits=(16,2))
    mat_charge_2 = fields.Float('Material Charge Qty 2', digits=(16,2))
    mat_charge_3 = fields.Float('Material Charge Qty 3', digits=(16,2))
    mat_charge_4 = fields.Float('Material Charge Qty 4', digits=(16,2))
    mat_charge_run_on = fields.Float('Material Charge Run On', digits=(16,2))
    req_mat_charge = fields.Boolean('Req Material Charge')
    
    total_price_1 = fields.Float('Price 1', digits=(16,2))
    total_price_2 = fields.Float('Price 2', digits=(16,2))
    total_price_3 = fields.Float('Price 3', digits=(16,2))
    total_price_4 = fields.Float('Price 4', digits=(16,2))
    total_price_run_on = fields.Float('Price Run On', digits=(16,2))
    req_total_price = fields.Boolean('Req Price')
    
    total_price_per_1000_1 = fields.Float('Price Per 1000 Qty 1', digits=(16,2))       
    total_price_per_1000_2 = fields.Float('Price Per 1000 Qty 2', digits=(16,2))
    total_price_per_1000_3 = fields.Float('Price Per 1000 Qty 3', digits=(16,2))
    total_price_per_1000_4 = fields.Float('Price Per 1000 Qty 4', digits=(16,2))
    total_price_per_1000_run_on = fields.Float('Price Per 1000 Run On', digits=(16,2))
    req_total_price_per_1000 = fields.Boolean('Req Price Per 1000')
    
    option_type = fields.Selection([('process','Process'),('material','Material')],string="Select option",default="process")
    
    param_finished_size = fields.Many2one('bb_products.material_size','Finished Size',related="estimate_id.finished_size")#,compute="compute_sizes")
    param_finished_width = fields.Integer('Finished Width',related="estimate_id.finished_width")#compute="compute_sizes")
    param_finished_height = fields.Integer('Finished Height',related="estimate_id.finished_height")#compute="compute_sizes")
    param_working_size = fields.Many2one('bb_products.material_size','Working Size',related="estimate_id.working_size")#compute="compute_sizes")
    param_working_width = fields.Integer('Working Width',related="estimate_id.working_width")#compute="compute_sizes")
    param_working_height = fields.Integer('Working Height',related="estimate_id.working_height")#compute="compute_sizes")
    param_knife_number = fields.Char('Knife Number',related="estimate_id.knife_number")#compute="compute_sizes")
    
    process_working_sheets_quantity_1 = fields.Integer('Process Working Sheets Required Qty 1')
    process_working_sheets_quantity_2 = fields.Integer('Process Working Sheets Required Qty 2')
    process_working_sheets_quantity_3 = fields.Integer('Process Working Sheets Required Qty 3')
    process_working_sheets_quantity_4 = fields.Integer('Process Working Sheets Required Qty 4')
    process_working_sheets_quantity_run_on = fields.Integer('Process Working Sheets Required Run On')
    req_process_working_sheets_quantity = fields.Boolean('Process Required')
    
    process_overs_quantity_1 = fields.Integer('Process Overs 1')
    process_overs_quantity_2 = fields.Integer('Process Overs 2')
    process_overs_quantity_3 = fields.Integer('Process Overs 3')
    process_overs_quantity_4 = fields.Integer('Process Overs 4')
    process_overs_quantity_run_on = fields.Integer('Process Overs Run On')
    req_process_overs_quantity = fields.Boolean('Overs Quantity')
    
    process_ids = fields.One2many('bb_estimate.material_link','processLine','Processes')
    material_ids = fields.One2many('bb_estimate.material_link','materialLine','Material')
    
    #Material Fields
    MaterialTypes = fields.Selection([('Stock','Stock'),('Trade Counter','Trade Counter'),('Non-Stockable','Non-Stockable')],string="Material Type")
    SheetHeight = fields.Float('Sheet Height (mm)')
    SheetWidth = fields.Float('Sheet Width (mm)')
    WhiteCutting = fields.Many2one('mrp.workcenter',string="White Cutting", domain="[('paper_type','=','white')]")
    PrintedCutting = fields.Many2one('mrp.workcenter',string="Printed Cutting", domain="[('paper_type','=','printed')]")
    NoWhiteCuts = fields.Integer('Number of White Cuts')
    NoPrintedCuts = fields.Integer('Number of Printed Cuts')
    NonStockMaterialType = fields.Selection([('Bespoke Material','Bespoke Material'),('Customer Supplied Material','Customer Supplied Material')],string="Non-Stock Material Type")
    MaterialName = fields.Char('Material')
    SheetSize = fields.Many2one('bb_products.material_size',string="Sheet Size")
    PurchaseUnit = fields.Many2one('uom.uom',string="Purchase Unit")
    Supplier = fields.Many2one('res.partner',string="Supplier",domain="[('supplier','=',True)]")
    MinimumQty = fields.Integer('Min. Quantity')
    PackSize = fields.Integer('Multiple Of')
    CostRate = fields.Float('Cost Rate')
    CharegeRate = fields.Float('Charge Rate')
    Margin = fields.Float('Margin')
    isLocked = fields.Boolean('Is Locked',related="estimate_id.isLocked")
    Sequence = fields.Integer('Sequence', default=1, help='Gives the sequence order when displaying a product list')
    staticPrice = fields.Boolean('Static Price', related="estimate_id.product_type.staticPrice")
    hasComputed = fields.Boolean('Has Computed in Total')
    reSync = fields.Boolean('ReSync')
    generatesPO = fields.Boolean('Generates PO',default=False)
    
    #General Parameters
    param_supplier = fields.Many2one('res.partner','Supplier',domain="[('supplier','=',True)]")
    req_param_supplier = fields.Boolean('Req Supplier')
    
    param_material_vendor = fields.Many2one('product.supplierinfo',string='Vendor',domain="[('product_id','=',True)]")
    req_param_material_vendor = fields.Boolean('Req Vendor')
    
    param_number_up = fields.Integer('Number Up')
    req_param_number_up = fields.Boolean('Req Number Up')
    
    param_number_out = fields.Integer('Number out')
    req_param_number_out = fields.Boolean('Number out')
    
    param_number_of_colors = fields.Integer('Number of Colors')
    req_param_number_of_colors = fields.Boolean('Number of Colors')
    
    param_number_of_colors_rev = fields.Integer('Number of Colors (Reverse)')
    req_param_number_of_colors_rev = fields.Boolean('Number of Colors (Reverse)')
    
    work_twist = fields.Boolean('Work and Twist')
    req_work_twist = fields.Boolean('Work and Twist')
    
    grammage = fields.Integer('Grammage(g.s.m)')
    req_grammage = fields.Boolean('Grammage(g.s.m)')
    
    param_no_of_ink_mixes = fields.Integer('No of Ink mixes')
    req_param_no_of_ink_mixes = fields.Boolean('No of Ink mixes')
    
    param_additional_charge = fields.Float('Misc. Material Charge (per 1000)',digits=(10,2))
    req_param_additional_charge = fields.Boolean('Misc. Material Charge (per 1000)')
    
    param_misc_charge_per_cm2 = fields.Float('Misc. Material Charge (Per cm2)',digits=(10,6))
    req_param_misc_charge_per_cm2 = fields.Boolean('Misc. Material Charge (Per cm2)')
    
    param_misc_charge_per_cm2_area = fields.Float('Misc. Mat. Charge Area (cm2)',digits=(10,6))
    req_param_misc_charge_per_cm2_area = fields.Boolean('Misc. Material Charge Area (Per cm2)')
    
    param_die_size = fields.Selection(DIE_SIZES,string="Size of Die")
    req_param_die_size = fields.Boolean('Size of Die')
    
    param_printed_material = fields.Boolean('Printed Material?')
    req_param_printed_material = fields.Boolean('Printed Material?')
    
    param_duplex_sheets = fields.Selection(DUPLEX_OPTIONS,string="Duplex Sheets")
    req_param_duplex_sheets = fields.Boolean('Duplex Sheets')
    
    param_number_of_sheets = fields.Integer('Number of Sections', default=1)
    req_param_number_of_sheets = fields.Boolean('Number of Sections')
    
    param_sheets_per_box = fields.Integer('Sheets per Box')
    req_param_sheets_per_box = fields.Boolean('Req. Sheets per Box')
    
    param_time_per_box = fields.Float('Time per Box(Hours)')
    req_param_time_per_box =fields.Boolean('Req. Time per Box (Hours)')
    
    param_number_of_cuts = fields.Integer('Number of cuts')
    req_param_number_of_cuts = fields.Boolean('Number of cuts')
    
    param_sheets_per_pile = fields.Integer('Sheets per pile')
    req_param_sheets_per_pile = fields.Boolean('Sheets per pile')
    
    param_time_per_pile = fields.Float('Time per pile')
    req_param_time_per_pile = fields.Boolean('Time per pile')
    
    param_env_windowpatching = fields.Boolean('Window Patching')
    req_param_env_windowpatching = fields.Boolean('Window Patching')
    
    param_env_peelandstick = fields.Boolean('Peel & Stick')
    req_param_env_peelandstick = fields.Boolean('Peel & Stick')
    
    param_env_inlineemboss = fields.Boolean('In-line Emboss')
    req_param_env_inlineemboss = fields.Boolean('Window Patching')
    
    param_env_gumming = fields.Boolean('Gumming')
    req_param_env_gumming = fields.Boolean('Gumming')
    
    param_material_line_id = fields.Many2one('bb_estimate.estimate_line',string="Material")
    req_param_material_line_id = fields.Boolean('Material')
    
    def GenerateMaterialDetails(self,line):
        name = False
        Grammage = False
        if line.customer_description:
            name = line.customer_description
        else:
            name = line.material.name
        
        if line.option_type == 'material':
            Grammage = line.material.grammage
        if Grammage:
            name =  '%s %s gsm' % (name, Grammage)
        return name
    
    @api.onchange('CostRate')
    def computePricesNonStockCost(self):
        for record in self:
            if record.CharegeRate:
                record.Margin = ((record.CharegeRate / record.CostRate) - 1) * 100
            elif record.Margin:
                record.CharegeRate = ((record.Margin / 100) + 1) * record.CostRate
                
    
    @api.onchange('Margin')
    def computePricesNonStockMargin(self):
        for record in self:
            record.CharegeRate = ((record.Margin / 100) + 1) * record.CostRate
            
    
    @api.onchange('CharegeRate')
    def computePricesNonStockPrice(self):
        for record in self:
            if record.CharegeRate:
                record.Margin = ((record.CharegeRate / record.CostRate) - 1) * 100
            elif record.Margin:
                record.CostRate = record.CharegeRate / ((record.Margin / 100) + 1)
            
    
    @api.depends('workcenterId','material')
    def _computeName(self):
        for record in self:
            if record.option_type == 'process':
                record.lineName = record.workcenterId.name
            elif record.option_type == 'material':
                record.lineName = record.material.name
    
                
    def calc_material_fields(self):
        for record in self:
            if record.estimate_id.unAllocated_1 != 0:
                record.param_finished_quantity_1 = record.estimate_id.unAllocated_1
                record.estimate_id.unAllocated_1 -= record.param_finished_quantity_1
                record.unallocated_finished_quantity_1 -= record.param_finished_quantity_1
            
            if record.estimate_id.unAllocated_2 != 0:
                record.param_finished_quantity_2 = record.estimate_id.unAllocated_2
                record.estimate_id.unAllocated_2 -= record.param_finished_quantity_2
                record.unallocated_finished_quantity_2 -= record.param_finished_quantity_2
            
            if record.estimate_id.unAllocated_3 != 0:
                record.param_finished_quantity_3 = record.estimate_id.unAllocated_3
                record.estimate_id.unAllocated_3 -= record.param_finished_quantity_3
                record.unallocated_finished_quantity_3 -= record.param_finished_quantity_3
            
            if record.estimate_id.unAllocated_4 != 0:
                record.param_finished_quantity_4 = record.estimate_id.unAllocated_4
                record.estimate_id.unAllocated_4 -= record.param_finished_quantity_4
                record.unallocated_finished_quantity_4 -= record.param_finished_quantity_4
            
            if record.estimate_id.unAllocated_run_on != 0:
                record.param_finished_quantity_run_on = record.estimate_id.unAllocated_run_on
                record.estimate_id.unAllocated_run_on -= record.param_finished_quantity_run_on
                record.unallocated_finished_quantity_run_on -= record.param_finished_quantity_run_on
            
            if record.material:
                proc = self.env['stock.location.route'].sudo().search(['|',('name','=','Buy'),('name','=','Make To Order')])
                if set(proc).issubset(record.material.route_ids) and record.material.route_ids:
                    if record.material.seller_ids:
                        record.param_material_vendor = record.material.seller_ids[0]
                        record.req_param_material_vendor = False
                        record.generatesPO = True
                        if len(record.material.seller_ids) > 1:
                            record.req_param_material_vendor = True
                    else:
                        raise ValidationError("There is no vendor associated to the product %s. Please define a vendor for this product."%(record.material.name))
                    
                record.documentCatergory = 'Material'
                if record.material.productType in ['Package','Delivery']:
                    record.documentCatergory = record.material.productType
                    if record.documentCategory == 'Delivery':
                        record.documentCategory = 'Despatch'

                record.customer_description = record.material.customerDescription
                record.JobTicketText = record.material.jobTicketDescription
                record.StandardCustomerDescription = record.material.customerDescription
                record.StandardJobDescription = record.material.jobTicketDescription

                record.grammage = record.material.grammage
                record.SheetHeight = record.material.sheet_height
                record.SheetWidth = record.material.sheet_width
                record.SheetSize = record.material.sheetSize
                
                if record.MaterialTypes == "Non-Stockable":
                    record.MaterialName = record.material.name
                
                if record.WhiteCutting:
                    record.NoWhiteCuts = self.WhiteCutting.process_type.get_white_cuts_for_number_out(record.param_number_out)
                if record.PrintedCutting:
                    record.NoPrintedCuts = self.PrintedCutting.process_type.get_printed_cuts_for_number_up(record.param_number_up)
                    
    @api.onchange('MaterialName')
    def _computeDescription(self):
        for record in self:
            record.customer_description = record.MaterialName
            record.JobTicketText = record.MaterialName
    
    @api.onchange('param_finished_quantity_1')
    def _onChangeQuantities1(self):
        de = (self.estimate_id.unAllocated_1 + self.param_finished_quantity_1)
        ratio = 0 if de == 0 else (float(self.param_finished_quantity_1) / de)
        if ratio != 0:
            self.unallocated_finished_quantity_1 = self.estimate_id.unAllocated_1
            self.param_finished_quantity_2 = (self.param_finished_quantity_2 + self.estimate_id.unAllocated_2) * ratio
            self.unallocated_finished_quantity_2 = (self.param_finished_quantity_2 / ratio) - self.param_finished_quantity_2
            self.estimate_id.unAllocated_2 = self.unallocated_finished_quantity_2
            
            self.param_finished_quantity_3 = (self.param_finished_quantity_3 + self.estimate_id.unAllocated_3) * ratio
            self.unallocated_finished_quantity_3 = (self.param_finished_quantity_3 / ratio) - self.param_finished_quantity_3
            self.estimate_id.unAllocated_3 = self.unallocated_finished_quantity_3
            
            self.param_finished_quantity_4 = (self.param_finished_quantity_4 + self.estimate_id.unAllocated_4) * ratio
            self.unallocated_finished_quantity_4 = (self.param_finished_quantity_4 / ratio) - self.param_finished_quantity_4
            self.estimate_id.unAllocated_4 = self.unallocated_finished_quantity_4
            
            self.param_finished_quantity_run_on = (self.param_finished_quantity_run_on + self.estimate_id.unAllocated_run_on) * ratio
            self.unallocated_finished_quantity_run_on = (self.param_finished_quantity_run_on / ratio) - self.param_finished_quantity_run_on
            self.estimate_id.unAllocated_run_on = self.unallocated_finished_quantity_run_on
            
    @api.onchange('param_finished_quantity_2')
    def _onChangeQuantities2(self):
        self.unallocated_finished_quantity_2 = self.estimate_id.unAllocated_2
        
    @api.onchange('param_finished_quantity_3')
    def _onChangeQuantities3(self):
        self.unallocated_finished_quantity_3 = self.estimate_id.unAllocated_3
    
    @api.onchange('param_finished_quantity_4')
    def _onChangeQuantities4(self):
        self.unallocated_finished_quantity_4 = self.estimate_id.unAllocated_4
    
    @api.onchange('param_finished_quantity_run_on')
    def _onChangeQuantitiesRunOn(self):
        self.unallocated_finished_quantity_run_on = self.estimate_id.unAllocated_run_on
    
    @api.onchange('param_number_out')
    def _onChangeNumberOut(self):
        if self.option_type == 'process':
            self.onChangeEventTrigger('param_number_out')
        else:
            if self.WhiteCutting:
                self.NoWhiteCuts = self.WhiteCutting.process_type.get_white_cuts_for_number_out(self.param_number_out)
            if self.PrintedCutting:
                self.NoPrintedCuts = self.PrintedCutting.process_type.get_printed_cuts_for_number_up(self.param_number_up)
    
    @api.onchange('SheetSize')
    def _onChangeSheetSize(self):
        if self.SheetSize:
            self.SheetHeight = self.SheetSize.height
            self.SheetWidth = self.SheetSize.width
    
    @api.onchange('param_additional_charge')
    def calc_param_additional_charge(self):
        self.onChangeEventTrigger('param_additional_charge')
        
    @api.onchange('param_misc_charge_per_cm2')
    def calc_param_misc_charge_per_cm2(self):
        self.onChangeEventTrigger('param_misc_charge_per_cm2')
        
    @api.onchange('param_misc_charge_per_cm2_area')
    def calc_param_misc_charge_per_cm2_area(self):
        self.onChangeEventTrigger('param_misc_charge_per_cm2_area')
        
    @api.onchange('param_sheets_per_box')
    def calc_param_sheets_per_box(self):
        self.onChangeEventTrigger('param_sheets_per_box')
        
    @api.onchange('param_time_per_box')
    def calc_param_time_per_box(self):
        self.onChangeEventTrigger('param_time_per_box')
        
    @api.onchange('param_env_windowpatching')
    def calc_param_env_windowpatching(self):
        self.onChangeEventTrigger('param_env_windowpatching')
        
    @api.onchange('param_env_peelandstick')
    def calc_param_env_peelandstick(self):
        self.onChangeEventTrigger('param_env_peelandstick')
        
    @api.onchange('param_env_inlineemboss')
    def calc_param_env_inlineemboss(self):
        self.onChangeEventTrigger('param_env_inlineemboss')
        
    @api.onchange('param_env_gumming')
    def calc_param_env_gumming(self):
        self.onChangeEventTrigger('param_env_gumming')
        
    @api.onchange('grammage')
    def calc_grammage(self):
        self.onChangeEventTrigger('param_grammage')
        
    @api.onchange('param_number_of_cuts')
    def calc_param_number_of_cuts(self):
        self.onChangeEventTrigger('param_number_of_cuts')
        
    @api.onchange('param_sheets_per_pile')
    def calc_param_sheets_per_pile(self):
        self.onChangeEventTrigger('param_sheets_per_pile')
        
    @api.onchange('param_time_per_pile')
    def calc_param_time_per_pile(self):
        self.onChangeEventTrigger('param_time_per_pile')
        
    @api.onchange('param_material_line_id')
    def calc_param_material_line_id_charge(self):
        self.onChangeEventTrigger('param_material_line_id')
        
    @api.onchange('param_number_of_sheets')
    def calc_param_number_of_sheets_change(self):  
        self.onChangeEventTrigger('param_number_of_sheets')
    
    @api.onchange('param_duplex_sheets')
    def calc_param_duplex_sheets_change(self):  
        self.onChangeEventTrigger('param_duplex_sheets')
        
    @api.onchange('workcenterId')  
    def calc_workcenterId_change(self):
        self.UpdateRequiredFields()
        self.onChangeEventTrigger('workcenterId')
        
    @api.onchange('material')  
    def calc_material_change(self):
        self.calc_material_fields()        
        self.onChangeEventTrigger('material')
                
    @api.onchange('param_printed_material')
    def calc_gen_printed_mat_change(self):
        self.onChangeEventTrigger('param_printed_material')
    
    @api.onchange('param_die_size')  
    def calc_gen_param_change(self):
        self.onChangeEventTrigger('param_die_size')
        
    @api.onchange('param_number_up')
    def calc_param_number_up_change(self):
        self.onChangeEventTrigger('param_number_up')
        
    #--------#
    @api.onchange('param_make_ready_time_1','param_make_ready_time_2','param_make_ready_time_3','param_make_ready_time_4')
    def calc_param_make_ready_time_1(self):
        self.onChangeEventTrigger('param_make_ready_time')  
    
    @api.onchange('quantity_required_1','quantity_required_2','quantity_required_3','quantity_required_4','quantity_required_run_on')
    def calc_quantity_required_1_change(self):
        self.onChangeEventTrigger('quantity_required')
    
    @api.onchange('margin_1','margin_2','margin_3','margin_4','margin_run_on')
    def calc_margin_1_change(self):
        self.onChangeEventTrigger('margin')
        
    @api.onchange('param_machine_speed_1','param_machine_speed_2','param_machine_speed_3','param_machine_speed_4','param_machine_speed_run_on')
    def calc_param_machine_speed(self):
        self.onChangeEventTrigger('param_machine_speed') 
        
    @api.onchange('param_wash_up_time_1','param_wash_up_time_2','param_wash_up_time_3','param_wash_up_time_4','param_wash_up_time_run_on')
    def calc_param_wash_up_time(self):
        self.onChangeEventTrigger('param_wash_up_time')        
    
    @api.onchange('param_make_ready_overs_1','param_make_ready_overs_2','param_make_ready_overs_3','param_make_ready_overs_4','param_make_ready_overs_run_on')
    def calc_param_make_ready_overs(self):
        self.onChangeEventTrigger('param_make_ready_overs')
        
    @api.onchange('param_running_overs_percent_1','param_running_overs_percent_2','param_running_overs_percent_3','param_running_overs_percent_4','param_running_overs_percent_run_on')
    def calc_param_running_overs_percent(self):
        self.onChangeEventTrigger('param_running_overs_percent')
        
    @api.onchange('cost_per_unit_1','cost_per_unit_2','cost_per_unit_3','cost_per_unit_4','cost_per_unit_run_on')
    def calc_cost_per_unit(self):
        self.onChangeEventTrigger('cost_per_unit')
        
    @api.onchange('price_per_unit_1','price_per_unit_2','price_per_unit_3','price_per_unit_4','price_per_unit_run_on')
    def calc_price_per_unit(self):
        self.onChangeEventTrigger('price_per_unit')
        
    @api.onchange('param_number_of_colors')
    def calc_param_number_of_colors_changes(self):
        self.onChangeEventTrigger('param_number_of_colors')
        
    @api.onchange('param_number_of_colors_rev')
    def calc_param_number_of_colors_rev_changes(self):
        self.onChangeEventTrigger('param_number_of_colors_rev')
        
    @api.onchange('param_no_of_ink_mixes')
    def calc_param_no_of_ink_mixes_changes(self):
        self.onChangeEventTrigger('param_no_of_ink_mixes')

        
#     @api.onchange('total_price_per_1000_1','total_price_per_1000_2','total_price_per_1000_3','total_price_per_1000_4','total_price_per_1000_run_on')
#     def calc_total_price_per_1000(self):
#         self.onChangeEventTrigger('total_price_per_1000')
    
    #--------#
        
    #Material Methods
    def get_default_field_values(self,material):
        qty_params = {
            'param_number_out':1
        }
        return qty_params
    
    def calculateNumberOutSheet(self, mat_width, mat_height, wrk_width, wrk_height):
        first_number_out = math.floor( mat_width / float(wrk_width) ) * math.floor( mat_height / float(wrk_height) )
        second_number_out = math.floor( mat_width / float(wrk_height) ) * math.floor( mat_height / float(wrk_width) )
        return max(first_number_out, second_number_out)
    
    def get_number_out(self,material,qty_param):
        if material.sheet_width and material.sheet_height and qty_param.get('working_width') and qty_param.get('working_height'):
            return self.calculateNumberOutSheet(material.sheet_width,material.sheet_height,qty_param.get('working_width'),qty_param.get('working_height'))
        else:
            return 1
    
    def update_field_values(self,material,qty_param,cost_param,fieldUpdated,qty):
        if fieldUpdated == 'material':
            qty_param['param_number_out'] = self.get_number_out(material,qty_param)
            cost_param['margin'] = material.margin
            if material.uom_id.factor:
                cost_param['cost_per_unit'] = material.standard_price * material.uom_id.factor
                cost_param['price_per_unit'] = material.list_price * material.uom_id.factor
            else:
                cost_param['cost_per_unit'] = material.standard_price * material.uom_id.factor_inv
                cost_param['price_per_unit'] = material.standard_price * material.uom_id.factor_inv
                
        if fieldUpdated in ['material','param_number_out','param_finished_quantity','process_ids']:
            cost_param['quantity_required'] = 0.0
            if not qty_param['param_number_out']:
                qty_param['param_number_out'] = 1
            
            if cost_param['finished_quantity']:
                finished_quantity_ratio = float(cost_param['param_finished_quantity'] / float(cost_param['finished_quantity']))
            else:
                finished_quantity_ratio = 0.0
                
            old_value = 0.0
            new_value = 0.0
            qty_required = 0.0
            if qty == '1':
                old_value = cost_param['quantity_required']
            elif qty == '2':
                old_value = cost_param['quantity_required']
            elif qty == '3':
                old_value = cost_param['quantity_required']
            elif qty == '4':
                old_value = cost_param['quantity_required']
            elif qty == 'run_on':
                old_value = cost_param['quantity_required']
            
            for process in self.material_ids:
                if process['overs_quantity_'+qty]:
                    qty_required += float(process['overs_quantity_'+qty])
                if not process['overs_only']:
                    if process['working_sheets_quantity_'+qty] and str(process['working_sheets_quantity_'+qty]) != 'False':
                        qty_required += float(process['working_sheets_quantity_'+qty])
            
            # Calculate the number of full size sheets required
            if 'work_twist' in cost_param and cost_param['work_twist']:
                cost_param['quantity_required'] = math.ceil(( math.ceil(qty_required * finished_quantity_ratio) / float(qty_param['param_number_out']) ) / 2)
                new_value = cost_param['quantity_required']
            else:
                cost_param['quantity_required'] = math.ceil( math.ceil(qty_required * finished_quantity_ratio) / float(qty_param['param_number_out']) )
                new_value = cost_param['quantity_required']
            
            #packs
            if cost_param['quantity_required'] > 0 and self.param_material_vendor:
                multiplier = self.param_material_vendor.multiplier if self.param_material_vendor.multiplier > 0 else 1
                cost_param['quantity_required'] =  math.ceil(cost_param['quantity_required']/multiplier) * multiplier
                cost_param['quantity_required'] = cost_param['quantity_required'] if cost_param['quantity_required'] > self.param_material_vendor.minQuantity else self.param_material_vendor.minQuantity
                
            if 'material_ids' not in qty_param and old_value != new_value:
                message = "Qty %s from %s to %s" % (qty, old_value, new_value)
                
    #end
    def onChangeEventTrigger(self,field):
        for record in self:
            if record.workcenterId or record.material:
                for qty in ['1','2','3','4','run_on']:
                    if qty=='run_on':
                        quantity = record.run_on
                    else:
                        quantity = int(eval('record.quantity_'+qty))
                    self.calc_qty_params(
                            record.workcenterId,
                            record.material,
                            quantity,
                            eval('record.param_make_ready_time_'+qty),
                            eval('record.param_machine_speed_'+qty),
                            eval('record.param_running_time_'+qty),
                            eval('record.param_wash_up_time_'+qty),
                            eval('record.param_make_ready_overs_'+qty),
                            eval('record.param_running_overs_percent_'+qty),
                            eval('record.param_finished_quantity_'+qty),
                            eval('record.quantity_required_'+qty),
                            eval('record.cost_per_unit_'+qty),
                            eval('record.price_per_unit_'+qty),
                            eval('record.margin_'+qty),
                            eval('record.total_price_'+qty),
                            eval('record.total_price_per_1000_'+qty),
                            qty,
                            record.param_additional_charge,
                            record.param_number_up,
                            record.param_number_of_colors,
                            record.param_number_of_colors_rev,
                            record.grammage,
                            record.param_die_size,
                            record.param_misc_charge_per_cm2,
                            record.param_no_of_ink_mixes,
                            int(record.quantity_1),
                            int(record.quantity_2),
                            int(record.quantity_3),
                            int(record.quantity_4),
                            int(record.run_on),
                            record.param_number_out,
                            record.param_working_width,
                            record.param_working_height,
                            record.param_printed_material,
                            record.param_duplex_sheets,
                            record.param_number_of_sheets,
                            record.param_material_line_id,
                            record.param_number_of_cuts,
                            record.param_sheets_per_pile,
                            record.param_time_per_pile,
                            record.param_env_windowpatching,
                            record.param_env_peelandstick,
                            record.param_env_inlineemboss,
                            record.param_env_gumming,
                            record.req_param_env_windowpatching,
                            record.req_param_env_peelandstick,
                            record.req_param_env_inlineemboss,
                            record.req_param_env_gumming,
                            record.param_sheets_per_box,
                            record.param_time_per_box,
                            record.staticPrice,
                            record.param_misc_charge_per_cm2_area,
                            field)
    
    def calc_qty_params(self,workcenterId,material,finished_quantity,param_make_ready_time,param_machine_speed,param_running_time,param_wash_up_time,param_make_ready_overs,param_running_overs_percent,param_finished_quantity,quantity_required,cost_per_unit,price_per_unit,margin,total_price,total_price_per_1000,qty,param_additional_charge,param_number_up,param_number_of_colors,param_number_of_colors_rev,param_grammage,param_die_size,param_misc_charge_per_cm2,param_no_of_ink_mixes,quantity_1,quantity_2,quantity_3,quantity_4,run_on,param_number_out,param_working_width,param_working_height,param_printed_material,param_duplex_sheets,param_number_of_sheets,param_material_line_id,param_number_of_cuts,param_sheets_per_pile,param_time_per_pile,param_env_windowpatching,param_env_peelandstick,param_env_inlineemboss,param_env_gumming,req_param_env_windowpatching,req_param_env_peelandstick,req_param_env_inlineemboss,req_param_env_gumming,param_sheets_per_box,param_time_per_box,static_price,param_misc_charge_per_cm2_area,fieldUpdated):
        #Variables required for calculations        
        return_values = {}
        process_type = workcenterId.process_type
        #data dictionaries which would ne updated with values in Workcenter
        
        qty_params = {
            'workcenterId':workcenterId,
            'param_number_out':param_number_out,
            'material':material,   
            'static_price':static_price,
            'param_env_windowpatching':param_env_windowpatching,
            'req_param_env_windowpatching':req_param_env_windowpatching,
            'param_sheets_per_box':param_sheets_per_box,
            'param_time_per_box':param_time_per_box,
            'param_env_peelandstick':param_env_peelandstick,
            'req_param_env_peelandstick':req_param_env_peelandstick,
            'param_env_inlineemboss':param_env_inlineemboss,
            'req_param_env_inlineemboss':req_param_env_inlineemboss,
            'param_env_gumming':param_env_gumming,
            'req_param_env_gumming':req_param_env_gumming,
            'param_number_up':param_number_up,
            'param_duplex_sheets':param_duplex_sheets,
            'param_number_of_sheets':param_number_of_sheets,
            'param_printed_material':param_printed_material,
            'param_number_of_colors':param_number_of_colors,
            'param_number_of_cuts':param_number_of_cuts,
            'param_sheets_per_pile':param_sheets_per_pile,
            'param_number_of_colors_rev':param_number_of_colors_rev,
            'param_grammage':param_grammage,
            'param_material_line_id':param_material_line_id,
            'param_time_per_pile':param_time_per_pile,
            'param_additional_charge':param_additional_charge,
            'param_die_size':param_die_size,
            'param_misc_charge_per_cm2_area':param_misc_charge_per_cm2_area,
            'param_minimum_price': 0,
            'param_misc_charge_per_cm2':param_misc_charge_per_cm2,
            'param_no_of_ink_mixes':param_no_of_ink_mixes,
            'working_width':param_working_width,
            'working_height':param_working_height,
            'quantity_1':quantity_1,
            'quantity_2':quantity_2,
            'quantity_3':quantity_3,
            'quantity_4':quantity_4,
            'run_on':run_on,
        }               
        
        if fieldUpdated in ['workcenterId','material'] and float(finished_quantity) > 0.0:
            if workcenterId:
                data = {key:val for key,val in workcenterId.process_type.get_default_field_values().items() if (key in qty_params.keys()) and ((val >= qty_params[key]) if type(val) != bool else (qty_params[key] or val)) }
                qty_params.update(data)
            elif material:
                qty_params.update(self.get_default_field_values(material))
              

        
        cost_params = {
            'finished_quantity'             : finished_quantity,
            'param_make_ready_time'         : param_make_ready_time,
            'param_machine_speed'           : param_machine_speed,
            'param_running_time'            : param_running_time,
            'param_wash_up_time'            : param_wash_up_time,
            'param_make_ready_overs'        : param_make_ready_overs,
            'param_running_overs_percent'   : param_running_overs_percent,
            'param_finished_quantity'       : param_finished_quantity,
            'quantity_required'             : quantity_required,
            'cost_per_unit'                 : cost_per_unit,
            'price_per_unit'                : price_per_unit,
            'margin'                        : margin,
            'total_price_per_1000'          : total_price_per_1000
        }
        
        if float(finished_quantity) > 0.0:  
            if self.option_type == 'process':
                workcenterId.process_type.UpdateEstimate(workcenterId,qty_params,cost_params,process_type,fieldUpdated,qty)
                
            elif self.option_type == 'material':
                self.update_field_values(material,qty_params,cost_params,fieldUpdated,qty)
                if not self.isEnvelope:
                    whiteCuttings = self.env['mrp.workcenter'].sudo().search([('paper_type','=','white')])
                    if whiteCuttings:
                        self.WhiteCutting = whiteCuttings[0]
                    printedCuttings = self.env['mrp.workcenter'].sudo().search([('paper_type','=','printed')])
                    if printedCuttings:
                        self.PrintedCutting = printedCuttings[0]
                
            elif fieldUpdated == 'workcenterId':
                cost_params['cost_per_unit'] = workcenterId.standard_price
                cost_params['price_per_unit'] = workcenterId.list_price
                cost_params['margin'] = workcenterId.margin_percent
                
            elif fieldUpdated == 'material':
                cost_params['cost_per_unit'] = material.standard_price
                cost_params['price_per_unit'] = material.list_price
                cost_params['margin'] = material.margin
                    
            self._calc_prices(qty_params, cost_params, fieldUpdated, qty)
            return_values.update(cost_params)
            self.update_values(qty_params,return_values,qty,fieldUpdated) 
                                  
    def _calc_prices(self,qty_params, cost_params, fieldUpdated, qty):
        extra_price_per_1000 = 0.0
        if ('param_additional_charge' in qty_params) and qty_params['param_additional_charge'] != 0:
            extra_price_per_1000 = qty_params['param_additional_charge'] 

        misc_charge_per_sheet = 0.0
        if qty_params.get('param_misc_charge_per_cm2') and qty_params.get('param_misc_charge_per_cm2_area'):
            misc_charge_per_sheet = qty_params['param_misc_charge_per_cm2'] * qty_params['param_misc_charge_per_cm2_area']  

        number_of_sheets = cost_params['params_working_sheets_needed'] if 'params_working_sheets_needed' in cost_params else 0.0
        
        if fieldUpdated == 'total_price_per_1000' and cost_params['quantity_required']:
            cost_params['price_per_unit'] = (((cost_params['total_price_per_1000'] - extra_price_per_1000) / 1000.0) * int(cost_params['finished_quantity'])) / cost_params['quantity_required']
            fieldUpdated = "price_per_unit"
            
        if fieldUpdated == 'quantity_required' and 'static_price' in qty_params:
            if qty == '1' and qty_params['static_price']:
                if qty_params['quantity_2'] > 0:
                    qty_params['quantity_required_2'] = cost_params['quantity_required']
                if qty_params['quantity_3'] > 0:
                    qty_params['quantity_required_3'] = cost_params['quantity_required']
                if qty_params['quantity_4'] > 0:
                    qty_params['quantity_required_4'] = cost_params['quantity_required']

        if fieldUpdated == 'cost_per_unit':
            if cost_params['margin']:
                cost_params['price_per_unit'] = ((cost_params['margin']/100)+1)*cost_params['cost_per_unit']
            elif cost_params['price_per_unit'] and cost_params['cost_per_unit']:
                cost_params['margin'] = (((cost_params['price_per_unit']/cost_params['cost_per_unit'])-1)*100)
            
            if qty=='1' and qty_params['static_price']:
                cost_params['price_per_unit'] = cost_params['cost_per_unit'] * 2
                cost_params['margin'] = (((cost_params['price_per_unit'] / cost_params['cost_per_unit']) - 1) * 100) if cost_params['cost_per_unit'] else 0
                if qty_params['quantity_2'] > 0:
                    qty_params['quantity_required_2'] = cost_params['quantity_required']
                    qty_params['cost_per_unit_2'] = cost_params['cost_per_unit']
                    qty_params['price_per_unit_2'] = cost_params['cost_per_unit'] * 2
                    qty_params['margin_2'] = (((cost_params['price_per_unit'] / cost_params['cost_per_unit']) - 1) * 100) if cost_params['cost_per_unit'] else 0
                    qty_params['total_cost_2'] = cost_params['cost_per_unit'] * cost_params['quantity_required']
                    qty_params['total_price_2'] = (cost_params['price_per_unit'] * cost_params['quantity_required']) + ((cost_params['finished_quantity'] / 1000.0) * extra_price_per_1000)
                    qty_params['total_price_per_1000_2'] = ((qty_params['total_price_2'] / cost_params['finished_quantity']) * 1000.0) if cost_params['finished_quantity'] else 0
                if qty_params['quantity_3'] > 0:
                    qty_params['quantity_required_3'] = cost_params['quantity_required']
                    qty_params['cost_per_unit_3'] = cost_params['cost_per_unit']
                    qty_params['price_per_unit_3'] = cost_params['cost_per_unit'] * 2
                    qty_params['margin_3'] = (((cost_params['price_per_unit'] / cost_params['cost_per_unit']) - 1) * 100) if cost_params['cost_per_unit'] else 0  
                    qty_params['total_cost_3'] = cost_params['cost_per_unit'] * cost_params['quantity_required']
                    qty_params['total_price_3'] = (cost_params['price_per_unit'] * cost_params['quantity_required']) + ((cost_params['finished_quantity'] / 1000.0) * extra_price_per_1000)
                    qty_params['total_price_per_1000_3'] = ((qty_params['total_price_3'] / cost_params['finished_quantity']) * 1000.0) if cost_params['finished_quantity'] else 0 
                if qty_params['quantity_4'] > 0:
                    qty_params['quantity_required_4'] = cost_params['quantity_required']
                    qty_params['cost_per_unit_4'] = cost_params['cost_per_unit']
                    qty_params['price_per_unit_4'] = cost_params['cost_per_unit'] * 2
                    qty_params['margin_4'] = (((cost_params['price_per_unit'] / cost_params['cost_per_unit']) - 1) * 100) if cost_params['cost_per_unit'] else 0
                    qty_params['total_cost_4'] = cost_params['cost_per_unit'] * cost_params['quantity_required']
                    qty_params['total_price_4'] = (cost_params['price_per_unit'] * cost_params['quantity_required']) + ((cost_params['finished_quantity'] / 1000.0) * extra_price_per_1000)
                    qty_params['total_price_per_1000_4'] = ((qty_params['total_price_4'] / cost_params['finished_quantity']) * 1000.0) if cost_params['finished_quantity'] else 0
                qty_params['quantity_required_run_on'] = 0.0
                qty_params['cost_per_unit_run_on'] = 0.0
                qty_params['price_per_unit_run_on'] = 0.0
                qty_params['margin_run_on'] = 0.0
                
        elif fieldUpdated == 'price_per_unit':
            if cost_params['price_per_unit'] and cost_params['cost_per_unit']:
                cost_params['margin'] = (((cost_params['price_per_unit']/cost_params['cost_per_unit'])-1)*100)
            elif cost_params['margin']:
                cost_params['cost_per_unit'] = cost_params['price_per_unit']/((cost_params['margin']/100)+1)
        elif fieldUpdated == "margin":
            cost_params['price_per_unit'] = ((cost_params['margin']/100) + 1) * cost_params['cost_per_unit']           

        cost_params['total_cost'] = cost_params['cost_per_unit'] * cost_params['quantity_required']
        cost_params['mat_charge'] = ((float(cost_params['finished_quantity']) / 1000.0) * extra_price_per_1000)
        
        if misc_charge_per_sheet and number_of_sheets:
            cost_params['mat_charge'] += misc_charge_per_sheet * number_of_sheets
        
        cost_params['total_price'] = (cost_params['price_per_unit'] * cost_params['quantity_required']) +  cost_params['mat_charge']
        
        if qty != 'run_on' and ('param_minimum_price' in qty_params.keys()) and qty_params['param_minimum_price']:
            if cost_params['total_price'] < qty_params['param_minimum_price']:
                cost_params['total_price'] = qty_params['param_minimum_price']
        
        if cost_params['finished_quantity']:
            if qty_params['param_number_up']:
                cost_params['total_price_per_1000'] = ((cost_params['total_price'] / float(cost_params['finished_quantity']) * 1000) / (qty_params['param_number_up']) if float(qty_params['param_number_up']) > 0 else 0.0)
            else:
                cost_params['total_price_per_1000'] = (cost_params['total_price'] / float(cost_params['finished_quantity']) * 1000) if float(cost_params['finished_quantity']) > 0 else 0.0
        else:
            cost_params['total_price_per_1000'] = 0.0
            
    def update_values(self,qty_params,return_values,qty,fieldUpdated):
        for record in self:
            record['param_make_ready_time_'+qty] = return_values['param_make_ready_time'] if qty != 'run_on' else None
            record['param_machine_speed_'+qty] = return_values['param_machine_speed'] if 'param_machine_speed' in return_values else ''
            record['param_running_time_'+qty] = return_values['param_running_time'] if 'param_running_time' in return_values else ''
            record['param_make_ready_overs_'+qty] = return_values['param_make_ready_overs'] if qty != 'run_on' else 0.0
            record['param_wash_up_time_'+qty] = return_values['param_wash_up_time'] if qty != 'run_on' else 0.0
            record['param_running_overs_percent_'+qty] = return_values['param_running_overs_percent'] if 'param_running_overs_percent' in return_values.keys() else ''
            record['quantity_required_'+qty] = return_values['quantity_required'] if 'quantity_required' in return_values else ''
            record['cost_per_unit_'+qty] = return_values['cost_per_unit'] if 'cost_per_unit' in return_values else ''
            record['price_per_unit_'+qty] = return_values['price_per_unit'] if 'price_per_unit' in return_values else ''
            record['margin_'+qty] = return_values['margin'] if 'margin' in return_values else ''
            record['total_price_per_1000_'+qty] = return_values['total_price_per_1000'] if 'total_price_per_1000' in return_values else ''
            record['total_cost_'+qty.strip()] =  return_values['total_cost'] if 'total_cost' in return_values else ''
            record['mat_charge_'+qty.strip()] = return_values['mat_charge'] if 'mat_charge' in return_values else ''
            record['total_price_'+qty] = return_values['total_price'] if 'total_price' in return_values else ''
            record['param_number_of_colors'] = qty_params.get('param_number_of_colors') 
            record['param_additional_charge'] = qty_params['param_additional_charge'] if 'param_additional_charge' in qty_params else ''
            record['param_number_out']  = qty_params['param_number_out'] if 'param_number_out' in qty_params else ''
            record['req_param_env_windowpatching'] = qty_params['req_param_env_windowpatching']
            record['req_param_env_peelandstick'] = qty_params['req_param_env_peelandstick']
            record['req_param_env_inlineemboss'] = qty_params['req_param_env_inlineemboss']
            record['req_param_env_gumming'] = qty_params['req_param_env_gumming']
            record['param_sheets_per_box'] = qty_params['param_sheets_per_box']
            record['param_time_per_box'] = qty_params['param_time_per_box']
            record['param_sheets_per_pile'] = qty_params['param_sheets_per_pile']
            record['param_time_per_pile'] = qty_params['param_time_per_pile']
            record['param_number_of_cuts'] = qty_params['param_number_of_cuts']
            record['process_working_sheets_quantity_'+qty] = qty_params['params_working_sheets_needed'] if 'params_working_sheets_needed' in qty_params else 0
            record['process_overs_quantity_'+qty] = qty_params['params_overs_needed'] if 'params_working_sheets_needed' in qty_params else 0
            record['param_misc_charge_per_cm2'] = qty_params['param_misc_charge_per_cm2']
    
    def UpdateRequiredFields(self):
        for record in self:
            if record.workcenterId:
                record.grammage = record.estimate_id.grammage
                record.documentCatergory = record.workcenterId.documentCatergory
                record.customer_description = record.workcenterId.note
                record.JobTicketText = record.workcenterId.jobTicketDescription
                record.StandardCustomerDescription = record.workcenterId.note
                record.StandardJobDescription = record.workcenterId.jobTicketDescription
                record.EstimatorNotes = record.workcenterId.notesForEstimator
                
                model_fields = {x:False for x in record._fields if x.startswith('req_') }
                fields = {x.name:True for x in record.workcenterId.process_type.requiredFields}
                record.update(model_fields)
                record.update(fields)
    
    def CreateLink(self,line,work_twist):
        link = self.env['bb_estimate.material_link'].sudo()
        processes = line.estimate_id.estimate_line.search([('estimate_id','=',line.estimate_id.id),('option_type','=','process')])
        added_working_sheets = False
        for process in processes:
            if process.workcenterId and process.workcenterId.process_type:
                if process.work_twist:
                    work_twist = True
                if process.workcenterId.process_type.MapMaterials:
                    newLink = {
                        'materialLine' : line.id,
                        'processLine' : process.id,
                        'estimate': line.estimate_id.id,
                    }
                    if (not added_working_sheets and process.workcenterId.process_type.OversOnly) and not (process.isExtra or line.isExtra):
                        newLink['overs_only'] = False
                        added_working_sheets = True
                    else:
                        newLink['overs_only'] = True
                    link.create(newLink)
        
    def CreateMaterialLink(self,process,work_twist):
        link = self.env['bb_estimate.material_link'].sudo()
        materials = process.estimate_id.estimate_line.search([('estimate_id','=',process.estimate_id.id),('option_type','=','material'),('documentCatergory','=','Material')])
        added_working_sheets = False
        for material in materials:
            if process.workcenterId and process.workcenterId.process_type:
                if material.material_ids:
                    added_working_sheets = any([(x.overs_only ^ x.processLine.workcenterId.process_type.OversOnly) for x in material.material_ids])
                if process.work_twist:
                    work_twist = True
                if process.workcenterId.process_type.MapMaterials:
                    newLink = {
                        'materialLine' : material.id,
                        'processLine' : process.id,
                        'estimate': process.estimate_id.id,
                    }
                    if (not added_working_sheets and process.workcenterId.process_type.OversOnly) and not (process.isExtra or material.isExtra):
                        newLink['overs_only'] = False
                        added_working_sheets = True
                    else:
                        newLink['overs_only'] = True
                    link.create(newLink)
    
    def RecalculatePrices(self,line,work_twist):
        if line.option_type and line.option_type == "material":
            estimate = line.estimate_id
            
            write_vals = {}

            gen_params = {
                'process_ids'               : line.process_ids or [],
                'param_number_out'          : line.param_number_out or 1,
                'param_number_up'           : line.param_number_up or 1,
            }

            # Re-calculate the totals for each quantity
            for qty in ['1','2','3','4','run_on']:

                if qty == 'run_on':
                    qty_field = 'run_on'
                else:
                    qty_field = 'quantity_'+qty
                
                if not estimate[qty_field]:
                    continue
                
                qty_params = {
                    'finished_quantity'         : estimate[qty_field],
                    'param_finished_quantity'   : line['param_finished_quantity_'+qty],
                    'quantity_required'         : 0.0,
                    'cost_per_unit'             : line['cost_per_unit_'+qty],
                    'price_per_unit'            : line['price_per_unit_'+qty],
                    'margin'                    : line['margin_'+qty],
                    'work_twist'                : work_twist,
                }
               
                line.update_field_values(line.material,gen_params,qty_params,'param_finished_quantity',qty)
                
                line._calc_prices(gen_params, qty_params, 'material', qty)
                
                write_vals.update({
                    'quantity_required_'+qty    : qty_params['quantity_required'],
                    'cost_per_unit_'+qty        : qty_params['cost_per_unit'],
                    'price_per_unit_'+qty       : qty_params['price_per_unit'],
                    'margin_'+qty               : qty_params['margin'],
                    'total_cost_'+qty           : qty_params['total_cost'],
                    'total_price_'+qty          : qty_params['total_price'],
                    'total_price_per_1000_'+qty : qty_params['total_price_per_1000'],
                })
            line.write(write_vals)
            
    @api.multi
    def unlink(self):
        estimate = self.estimate_id
        optionType = self.option_type
        work_twist = False
        materials = self.process_ids.mapped('materialLine')
        estimateData = {x : estimate[x] for x in estimate._fields if 'total_price_' in x}
        for qty in ['1','2','3','4','run_on']:
            estimateData['total_price_'+qty] -= self['total_price_'+qty]
            estimateData['total_price_1000_'+qty] -= self['total_price_per_1000_'+qty]
        estimate.write(estimateData)
        
        if self.option_type == 'material':
            recs = [x for x in self.estimate_id.estimate_line if (x.param_material_line_id.id == self.id) and x.param_material_line_id]
            for process in recs:
                process.unlink()
                
        rec = super(EstimateLine, self).unlink()
        
        if optionType == 'process':
            for m in estimate.estimate_line:
                if m.option_type == 'material' and m.documentCatergory not in ['Packing','Despatch']:
                    m.RecalculatePrices(m,work_twist)
        return rec
    
    def _checkResync(self,vals):
        resync = False
        recs = [x for x in self.estimate_id.estimate_line if (x.param_material_line_id.id == self.id) and x.param_material_line_id]
        if (len(recs) > 0) and self.option_type == 'material':
            for field in vals.keys():
                if (self[field] != vals[field]
                   ) and field != 'reSync':
                    resync = True
                    break
        elif self.option_type == 'process':
            if self.process_ids:
                for x in ['1','2','3','4','run_on']:
                    if 'process_overs_quantity_%s'%(x) in vals.keys():
                        if (self['process_overs_quantity_%s'%(x)] != vals['process_overs_quantity_%s'%(x)]):
                            resync = True
                    if 'process_working_sheets_quantity_%s'%(x) in vals.keys():
                        if (self['process_working_sheets_quantity_%s'%(x)] != vals['process_working_sheets_quantity_%s'%(x)]):
                            resync = True
        
        return resync
        
    @api.multi
    def write(self,vals):
        #check if resync is required
        #vals['reSync'] = self._checkResync(vals)
        estimateData = {x : self.estimate_id[x] for x in self.estimate_id._fields if 'total_price_' in x}
        for qty in ['1','2','3','4','run_on']:
            if 'total_price_'+qty in vals.keys():
                estimateData['total_price_'+qty] -= 0 if 'hasComputed' in vals.keys() else self['total_price_'+qty]
                estimateData['total_price_'+qty] += vals['total_price_'+qty]
            if 'total_price_per_1000_'+qty in vals.keys():
                estimateData['total_price_1000_'+qty] -= 0 if 'hasComputed' in vals.keys() else self['total_price_per_1000_'+qty]
                estimateData['total_price_1000_'+qty] += vals['total_price_per_1000_'+qty]
        vals['hasComputed'] = True
        self.estimate_id.write(estimateData)
        
        currentRecord = super(EstimateLine, self).write(vals)
        
        if self.option_type == 'process':
            for mat in self.process_ids:
                mat.ComputePrice()
        elif self.option_type == 'material':
            recs = [x for x in self.estimate_id.estimate_line if (x.param_material_line_id.id == self.id) and x.param_material_line_id]
            for process in recs:
                process.calc_param_material_line_id_charge()
                dictProcess = {key:process[key] for key in process._fields if type(process[key]) in [int,str,bool,float]}
                dictProcess.pop('hasComputed')
                process.write(dictProcess)
        return currentRecord
        
    
    @api.model
    def create(self,values):
        records = super(EstimateLine,self).create(values)
        for lineId in records:
            if lineId:
                if lineId.option_type == 'process':
                    work_twist = False
                    self.CreateMaterialLink(lineId,work_twist)
                    if lineId.workcenterId.associatedBoxId and (not lineId.estimate_id.duplicateProcess):
                        data = {}
                        material = lineId.workcenterId.associatedBoxId
                        estimate = lineId.estimate_id
                        for qty in ['1','2','3','4','run_on']:
                            if qty == 'run_on':
                                quantity = 'run_on'
                            else:
                                quantity = 'quantity_'+qty

                            if not estimate[quantity]:
                                continue

                            cost_params={
                                'finished_quantity':estimate[quantity],
                                'cost_per_unit':material.standard_price,
                                'price_per_unit':material.list_price,
                                'margin':material.margin,
                            }

                            qty_params={
                                'param_number_up':lineId.param_number_up
                            }


                            cost_params['quantity_required'] = math.ceil(cost_params['finished_quantity'] / float(lineId.param_sheets_per_box))

                            self._calc_prices(qty_params, cost_params, 'None', qty)

                            data.update({
                                'quantity_required_'+qty    : cost_params['quantity_required'],
                                'cost_per_unit_'+qty        : material.standard_price,
                                'price_per_unit_'+qty       : material.list_price,
                                'margin_'+qty               : material.margin,
                                'total_cost_'+qty           : cost_params['total_cost'],
                                'total_price_'+qty          : cost_params['total_price'],
                                'total_price_per_1000_'+qty : cost_params['total_price_per_1000']
                                })


                        newRecord = {
                            'estimate_id' : lineId.estimate_id.id,
                            'MaterialTypes': 'Stock',
                            'material': material.id,
                            'option_type':'material',
                            'documentCatergory' : 'Packing',
                            'customer_description': material.customerDescription,
                            'StandardJobDescription': material.jobTicketDescription,
                            'StandardCustomerDescription' : material.customerDescription,
                            'JobTicketText':material.jobTicketDescription,
                            'lineName' : material.name,
                            'isExtra' : True if lineId.isExtra else False
                        }
                        newRecord.update(data)
                        self.create(newRecord)
                        
                elif lineId.option_type == 'material':
                    if lineId.MaterialTypes == 'Non-Stockable':
                        product = self.env['product.product'].sudo()
                        seller = self.env['product.supplierinfo'].sudo()
                        mto =self.env['stock.location.route'].sudo().search([('name','=','Make To Order')],limit=1)
                        buy =self.env['stock.location.route'].sudo().search([('name','=','Buy')],limit=1)
                        newProduct = {
                            'name' : lineId.MaterialName,
                            'type': 'product',
                            'default_code': lineId.estimate_id.estimate_number,
                            'grammage' : lineId.grammage,
                            'sheetSize' : lineId.SheetSize.id,
                            'sheet_width' : lineId.SheetWidth,
                            'sheet_height' : lineId.SheetHeight,
                            'standard_price': lineId.CostRate,
                            'list_price': lineId.CharegeRate,
                            'productType': 'Non-Stockable',
                            'customerDescription': lineId.customer_description,
                            'jobTicketDescription': lineId.JobTicketText,
                            'lastUsedEstimateDate': str(datetime.now().date()),
                            'lastUsedEstimateNumber': lineId.estimate_id.estimate_number,
                            'margin': lineId.Margin,
                        }
                        if mto and buy and lineId.NonStockMaterialType == 'Bespoke Material':
                            newProduct['route_ids'] = [(4,mto.id),(4,buy.id)]
                            newProduct['generatesPO'] = True
                        if lineId.PurchaseUnit:
                            newProduct['uom_id'] = lineId.PurchaseUnit.id
                            newProduct['uom_po_id'] = lineId.PurchaseUnit.id

                        if  (not lineId.material) or lineId.NonStockMaterialType == 'Bespoke Material':
                            productId = product.create(newProduct)	             
                        else:
                            productId = lineId.material
                        if productId and lineId.Supplier:
                            newSeller = {
                                'product_id' : productId.id,
                                'product_tmpl_id' : productId.product_tmpl_id.id,
                                'product_name' : lineId.MaterialName,
                                'price': lineId.CharegeRate,
                                'name' : lineId.Supplier.id,
                                'minQuantity' : lineId.MinimumQty,
                                'multiplier' : lineId.PackSize
                            }
                            seller.create(newSeller)

                            lineId.write({'material':productId.id,'generatesPO':True})
                            lineId.calc_material_change()
                            lineId._onChangeNumberOut()
                            dictLine = {key:lineId[key] for key in lineId._fields if type(lineId[key]) in [int,str,bool,float]}
                            lineId.write(dictLine)
                            
                        elif productId and (not lineId.material):
                            lineId.write({'material':productId.id})    
                            lineId.calc_material_change()
                            lineId._onChangeNumberOut()
                            dictLine = {key:lineId[key] for key in lineId._fields if type(lineId[key]) in [int,str,bool,float]}
                            lineId.write(dictLine)
                    
                    if lineId.documentCatergory not in ['Packing','Despatch']:   
                        work_twist = False
                        self.CreateLink(lineId,work_twist)
                        
                    if not lineId.estimate_id.duplicateProcess:
                        if lineId.WhiteCutting:
                            newProcess = {
                                'option_type' : 'process',
                                'workcenterId' : lineId.WhiteCutting.id,
                                'param_material_line_id' : lineId.id,
                                'estimate_id' : lineId.estimate_id.id,
                                'isExtra': lineId.isExtra
                                #'param_number_of_cuts' : lineId.WhiteCutting.process_type.get_white_cuts_for_number_out(record.param_number_out)
                            }
                            process = self.create(newProcess)
                            process.calc_workcenterId_change()
                            dictProcess = {key:process[key] for key in process._fields if type(process[key]) in [int,str,bool,float]}
                            dictProcess.pop('hasComputed')
                            process.write(dictProcess)

                        if lineId.PrintedCutting:
                            newProcess = {
                                'option_type' : 'process',
                                'workcenterId' : lineId.PrintedCutting.id,
                                'param_material_line_id' : lineId.id,
                                'estimate_id' : lineId.estimate_id.id,
                                'isExtra': lineId.isExtra
                            }
                            process = self.create(newProcess)
                            process.calc_workcenterId_change()
                            dictProcess = {key:process[key] for key in process._fields if type(process[key]) in [int,str,bool,float]}
                            dictProcess.pop('hasComputed')
                            process.write(dictProcess)
                            
                    if lineId.material:
                        lineId.material.write({'lastUsedEstimateDate':str(datetime.now().date()),'lastUsedEstimateNumber':lineId.estimate_id.estimate_number})
                        
            if not lineId.hasComputed:
                lineId.write({'hasComputed': True,
                              'total_price_1':lineId.total_price_1,
                              'total_price_2':lineId.total_price_2,
                              'total_price_3':lineId.total_price_3,
                              'total_price_4':lineId.total_price_4,
                              'total_price_run_on':lineId.total_price_run_on,
                              'total_price_per_1000_1':lineId.total_price_per_1000_1,
                              'total_price_per_1000_2':lineId.total_price_per_1000_2,
                              'total_price_per_1000_3':lineId.total_price_per_1000_3,
                              'total_price_per_1000_4':lineId.total_price_per_1000_4,
                              'total_price_per_1000_run_on':lineId.total_price_per_1000_run_on
                             })
        return records    
    
    def ReSyncPrices(self):
        if self.option_type == 'process':
            for line in self.process_ids:
                line.ComputePrice()
        
        if self.option_type == 'material':
            recs = [x for x in self.estimate_id.estimate_line if (x.param_material_line_id.id == self.id) and x.param_material_line_id]
            for process in recs:
                process.calc_param_material_line_id_charge()
                dictProcess = {key:process[key] for key in process._fields if type(process[key]) in [int,str,bool,float]}
                dictProcess.pop('hasComputed')
                process.write(dictProcess)
        
        self.write({'reSync': False})

    def duplicate(self,values):
        return super(EstimateLine,self).create(values)
