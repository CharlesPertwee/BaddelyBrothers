# -*- coding: utf-8 -*-

from odoo import models, fields, api
DIE_SIZES = [
    ('standard','No Die (No Charge)'),
    ('small','Crest Die'),
    ('medium','Heading Die'),
    ('large','Invitation Die')
]

DUPLEX_OPTIONS = [
    ('two', '2 Sheets'),
    ('three', '3 Sheets'),
    ('four', '4 Sheets'),
    ('five', '5 Sheets'),
]
class EstimateLine(models.Model):
    _name = 'bb_estimate.estimate_line'
    
    workcenterId = fields.Many2one('mrp.workcenter', string="Process")
    material = fields.Many2one('product.template', string="Materials")
    estimate_id = fields.Many2one('bb_estimate.estimate','Estimate')
    
    lineName = fields.Char(string='Process/Material')
    customer_description = fields.Text(string="Customer Description")

    quantity_1 = fields.Char('Quantity 1')
    quantity_2 = fields.Char('Quantity 2')
    quantity_3 = fields.Char('Quantity 3')
    quantity_4 = fields.Char('Quantity 4')
    run_on = fields.Char('Run On')
    
    # Parameters for calculation
    param_make_ready_time_1 = fields.Float('Make Ready Time (hours) Qty 1', digits=(10,2))
    param_make_ready_time_2 = fields.Float('Make Ready Time (hours) Qty 2', digits=(10,2))
    param_make_ready_time_3 = fields.Float('Make Ready Time (hours) Qty 3', digits=(10,2))
    param_make_ready_time_4 = fields.Float('Make Ready Time (hours) Qty 4', digits=(10,2))
    param_make_ready_time_run_on = fields.Float('Make Ready Time (hours) Run On', digits=(10,2))
    
    param_machine_speed_1 = fields.Float('Machine Speed Qty 1', digits=(10,2))
    param_machine_speed_2 = fields.Float('Machine Speed Qty 2', digits=(10,2))
    param_machine_speed_3 = fields.Float('Machine Speed Qty 3', digits=(10,2))
    param_machine_speed_4 = fields.Float('Machine Speed Qty 4', digits=(10,2))
    param_machine_speed_run_on = fields.Float('Machine Speed Run On', digits=(10,2))
    
    param_running_time_1 = fields.Float('Running Time Qty 1', digits=(10,2))
    param_running_time_2 = fields.Float('Running Time Qty 2', digits=(10,2))
    param_running_time_3 = fields.Float('Running Time Qty 3', digits=(10,2))
    param_running_time_4 = fields.Float('Running Time Qty 4', digits=(10,2))
    param_running_time_run_on = fields.Float('Running Time Run On', digits=(10,2))
    
    param_wash_up_time_1 = fields.Float('Wash Up Time (hours) Qty 1', digits=(10,2))
    param_wash_up_time_2 = fields.Float('Wash Up Time (hours) Qty 2', digits=(10,2))
    param_wash_up_time_3 = fields.Float('Wash Up Time (hours) Qty 3', digits=(10,2))
    param_wash_up_time_4 = fields.Float('Wash Up Time (hours) Qty 4', digits=(10,2))
    param_wash_up_time_run_on = fields.Float('Wash Up Time (hours) Run On', digits=(10,2))
    
    param_make_ready_overs_1 = fields.Integer('Make Ready Overs Qty 1')
    param_make_ready_overs_2 = fields.Integer('Make Ready Overs Qty 2')
    param_make_ready_overs_3 = fields.Integer('Make Ready Overs Qty 3')
    param_make_ready_overs_4 = fields.Integer('Make Ready Overs Qty 4')
    param_make_ready_overs_run_on = fields.Integer('Make Ready Overs Run On')
    
    param_running_overs_percent_1 = fields.Float('Running Overs (%) Qty 1', digits=(10,2))
    param_running_overs_percent_2 = fields.Float('Running Overs (%) Qty 2', digits=(10,2))
    param_running_overs_percent_3 = fields.Float('Running Overs (%) Qty 3', digits=(10,2))
    param_running_overs_percent_4 = fields.Float('Running Overs (%) Qty 4', digits=(10,2))
    param_running_overs_percent_run_on = fields.Float('Running Overs (%) Run On', digits=(10,2))
    
    param_finished_quantity_1 = fields.Integer('Material Finished Quantity Qty 1')
    param_finished_quantity_2 = fields.Integer('Material Finished Quantity Qty 2')
    param_finished_quantity_3 = fields.Integer('Material Finished Quantity Qty 3')
    param_finished_quantity_4 = fields.Integer('Material Finished Quantity Qty 4')
    param_finished_quantity_run_on = fields.Integer('Material Finished Quantity Run On')
    
    quantity_required_1 = fields.Float('Quantity/Hours Qty 1', digits=(10,2))
    quantity_required_2 = fields.Float('Quantity/Hours Qty 2', digits=(10,2))
    quantity_required_3 = fields.Float('Quantity/Hours Qty 3', digits=(10,2))
    quantity_required_4 = fields.Float('Quantity/Hours Qty 4', digits=(10,2))
    quantity_required_run_on = fields.Float('Quantity/Hours Run On', digits=(10,2))
    
    cost_per_unit_1 = fields.Float('Cost Rate (GBP) Qty 1', digits=(16,6))
    cost_per_unit_2 = fields.Float('Cost Rate (GBP) Qty 2', digits=(16,6))
    cost_per_unit_3 = fields.Float('Cost Rate (GBP) Qty 3', digits=(16,6))
    cost_per_unit_4 = fields.Float('Cost Rate (GBP) Qty 4', digits=(16,6))
    cost_per_unit_run_on = fields.Float('Cost Rate (GBP) Run On', digits=(16,6))
    
    price_per_unit_1 = fields.Float('Charge Rate (GBP) Qty 1', digits=(16,6))       
    price_per_unit_2 = fields.Float('Charge Rate (GBP) Qty 2', digits=(16,6))      
    price_per_unit_3 = fields.Float('Charge Rate (GBP) Qty 3', digits=(16,6))
    price_per_unit_4 = fields.Float('Charge Rate (GBP) Qty 4', digits=(16,6))
    price_per_unit_run_on = fields.Float('Charge Rate (GBP) Run On', digits=(16,6))
    
    margin_1 = fields.Float('Margin (%) Qty 1', digits=(10,2))
    margin_2 = fields.Float('Margin (%) Qty 2', digits=(10,2))
    margin_3 = fields.Float('Margin (%) Qty 3', digits=(10,2))
    margin_4 = fields.Float('Margin (%) Qty 4', digits=(10,2))
    margin_run_on = fields.Float('Margin (%) Run On', digits=(10,2))
    
    total_cost_1 = fields.Float('Cost Qty 1', digits=(16,2))
    total_cost_2 = fields.Float('Cost Qty 2', digits=(16,2))
    total_cost_3 = fields.Float('Cost Qty 3', digits=(16,2))
    total_cost_4 = fields.Float('Cost Qty 4', digits=(16,2))
    total_cost_run_on = fields.Float('Cost Run On', digits=(16,2))
    
    mat_charge_1 = fields.Float('Material Charge Qty 1', digits=(16,2))
    mat_charge_2 = fields.Float('Material Charge Qty 2', digits=(16,2))
    mat_charge_3 = fields.Float('Material Charge Qty 3', digits=(16,2))
    mat_charge_4 = fields.Float('Material Charge Qty 4', digits=(16,2))
    mat_charge_run_on = fields.Float('Material Charge Run On', digits=(16,2))
    
    total_price_1 = fields.Float('Price 1', digits=(16,2))
    total_price_2 = fields.Float('Price 2', digits=(16,2))
    total_price_3 = fields.Float('Price 3', digits=(16,2))
    total_price_4 = fields.Float('Price 4', digits=(16,2))
    total_price_run_on = fields.Float('Price Run On', digits=(16,2))
    
    total_price_per_1000_1 = fields.Float('Price Per 1000 Qty 1', digits=(16,2))       
    total_price_per_1000_2 = fields.Float('Price Per 1000 Qty 2', digits=(16,2))
    total_price_per_1000_3 = fields.Float('Price Per 1000 Qty 3', digits=(16,2))
    total_price_per_1000_4 = fields.Float('Price Per 1000 Qty 4', digits=(16,2))
    total_price_per_1000_run_on = fields.Float('Price Per 1000 Run On', digits=(16,2))
    
    option_type = fields.Selection([('process','Process'),('material','Material')],string="Select option")
    
    param_finished_size = fields.Many2one('bb_estimate.material_size','Finished Size')
    param_finished_width = fields.Integer('Finished Width')
    param_finished_height = fields.Integer('Finished Height')
    param_working_size = fields.Many2one('bb_estimate.material_size','Working Size')
    param_working_width = fields.Integer('Working Width')
    param_working_height = fields.Integer('Working Height')
    param_knife_number = fields.Char('Knife Number')
    
    process_working_sheets_quantity_1 = fields.Integer('Process Working Sheets Required Qty 1')
    process_working_sheets_quantity_2 = fields.Integer('Process Working Sheets Required Qty 2')
    process_working_sheets_quantity_3 = fields.Integer('Process Working Sheets Required Qty 3')
    process_working_sheets_quantity_4 = fields.Integer('Process Working Sheets Required Qty 4')
    process_working_sheets_quantity_run_on = fields.Integer('Process Working Sheets Required Run On')
    
    process_overs_quantity_1 = fields.Integer('Process Overs 1')
    process_overs_quantity_2 = fields.Integer('Process Overs 2')
    process_overs_quantity_3 = fields.Integer('Process Overs 3')
    process_overs_quantity_4 = fields.Integer('Process Overs 4')
    process_overs_quantity_run_on = fields.Integer('Process Overs Run On')
    
    process_ids = fields.Char('Process')#.One2many('bb_estimate.line_linkage','estimateLineId','Processes')
    material_ids = fields.Char('Material')#.One2many('bb_estimate.line_linkage','estimateLineId','Material')
    
    
    #General Parameters
    param_number_up = fields.Integer('Number Up')
    req_param_number_up = fields.Boolean('Req Number Up')
    
    param_number_out = fields.Integer('Number out')
    req_param_number_out = fields.Boolean('Number out')
    
    param_number_of_colors = fields.Integer('Number of Colors')
    req_param_number_of_colors = fields.Boolean('Number of Colors')
    
    param_number_of_colors_rev = fields.Integer('Number of Colors(Reverse)')
    req_param_number_of_colors_rev = fields.Boolean('Number of Colors(Reverse)')
    
    work_twist = fields.Boolean('Work and Twist')
    req_work_twist = fields.Boolean('Work and Twist')
    
    grammage = fields.Integer('Grammage(g.s.m)')
    req_grammage = fields.Boolean('Grammage(g.s.m)')
    
    param_no_of_ink_mixes = fields.Integer('No of Ink mixes')
    req_param_no_of_ink_mixes = fields.Boolean('No of Ink mixes')
    
    param_additional_charge = fields.Float('Misc. Material Charge(per 1000)')
    req_param_additional_charge = fields.Boolean('Misc. Material Charge(per 1000)')
    
    param_misc_charge_per_cm2 = fields.Float('Misc. Material Charge (Per cm2)')
    req_param_misc_charge_per_cm2 = fields.Boolean('Misc. Material Charge (Per cm2)')
    
    param_die_size = fields.Selection(DIE_SIZES,string="Size of Die")
    req_param_die_size = fields.Boolean('Size of Die')
    
    param_printed_material = fields.Boolean('Printed Material?')
    req_param_printed_material = fields.Boolean('Printed Material?')
    
    param_duplex_sheets = fields.Selection(DUPLEX_OPTIONS,string="Duplex Sheets")
    req_param_duplex_sheets = fields.Boolean('Duplex Sheets')
    
    param_number_of_sheets = fields.Integer('Number of Sections')
    req_param_number_of_sheets = fields.Boolean('Number of Sections')
    
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
    
    param_env_inlineemboss = fields.Boolean('Window Patching')
    req_param_env_inlineemboss = fields.Boolean('Window Patching')
    
    param_env_gumming = fields.Boolean('Gumming')
    req_param_env_gumming = fields.Boolean('Gumming')
    
    param_material_line_id = fields.Many2one('bb_estimate.estimate_line',string="Material")
    req_param_material_line_id = fields.Boolean('Peel & Stick')
    
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
    #end
    
    def _calc_prices(self,qty_params, cost_params, fieldUpdated, qty):
        extra_price_per_1000 = qty_params['param_additional_charge'] if qty_params['param_additional_charge'] else 0.0

        misc_charge_per_sheet = 0.0
        if qty_params.get('param_misc_charge_per_cm2') and gen_params.get('param_misc_charge_per_cm2_area'):
            misc_charge_per_sheet = gen_params['param_misc_charge_per_cm2'] * gen_params['param_misc_charge_per_cm2_area']  

        number_of_sheets = cost_params['params_working_sheets_needed'] if 'params_working_sheets_needed' in cost_params else 0.0

        if fieldUpdated == 'total_price_per_1000' and cost_params['quantity_required'] is not None:
            cost_params['price_per_unit'] = (((cost_params['total_price_per_1000'] - extra_price_per_1000) / 1000.0) * int(cost_params['finished_quantity'])) / cost_params['quantity_required']

        if fieldUpdated == 'cost_per_unit':
            if cost_params['price_per_unit'] and cost_params['cost_per_unit']:
                cost_params['margin'] = (((cost_params['price_per_unit']/cost_params['cost_per_unit'])-1)*100)
            elif cost_params['margin']:
                cost_params['price_per_unit'] = ((cost_params['margin']/100)+1)*cost_params['cost_per_unit']
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
        
        if cost_params['finished_quantity']:
            if qty_params['param_number_up']:
                cost_params['total_price_per_1000'] = ((cost_params['total_price'] / float(cost_params['finished_quantity']) * 1000) / (qty_params['param_number_up']) if float(qty_params['param_number_up']) > 0 else 0.0)
            else:
                cost_params['total_price_per_1000'] = (cost_params['total_price'] / float(cost_params['finished_quantity']) * 1000) if float(cost_params['finished_quantity']) > 0 else 0.0
        else:
            cost_params['total_price_per_1000'] = 0.0 
                                                       
    def get_gen_fields(self):
        pass    
    
    def onChangeEventTrigger(self,field):
        for record in self:
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
                        field)
                
    @api.onchange('param_additional_charge')
    def calc_param_additional_charge(self):
        self.onChangeEventTrigger('param_additional_charge')
        
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
        self.onChangeEventTrigger('material')
                
    @api.onchange('param_printed_material')
    def calc_gen_printed_mat_change(self):
        self.onChangeEventTrigger('param_printed_material')
    
    @api.onchange('param_die_size')  
    def calc_gen_param_change(self):
        self.onChangeEventTrigger('param_die_size')
    
    @api.onchange('param_make_ready_time_1')
    def calcColPrice(self):
        for record in self:
            qty = '1'
            self.calc_qty_params(
                    record.workcenterId,
                    record.material,
                    record.quantity_1,
                    record.param_make_ready_time_1,
                    record.param_machine_speed_1,
                    record.param_running_time_1,
                    record.param_wash_up_time_1,
                    record.param_make_ready_overs_1,
                    record.param_running_overs_percent_1,
                    record.param_finished_quantity_1,
                    record.quantity_required_1,
                    record.cost_per_unit_1,
                    record.price_per_unit_1,
                    record.margin_1,
                    record.total_price_1,
                    record.total_price_per_1000_1,
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
                    'None') 
    
    def calc_qty_params(self,workcenterId,material,finished_quantity,param_make_ready_time,param_machine_speed,param_running_time,param_wash_up_time,param_make_ready_overs,param_running_overs_percent,param_finished_quantity,quantity_required,cost_per_unit,price_per_unit,margin,total_price,total_price_per_1000,qty,param_additional_charge,param_number_up,param_number_of_colors,param_number_of_colors_rev,param_grammage,param_die_size,param_misc_charge_per_cm2,param_no_of_ink_mixes,quantity_1,quantity_2,quantity_3,quantity_4,run_on,param_number_out,param_working_width,param_working_height,param_printed_material,param_duplex_sheets,param_number_of_sheets,param_material_line_id,param_number_of_cuts,param_sheets_per_pile,param_time_per_pile,fieldUpdated):
        #Variables required for calculations        
        return_values = {}
        process_type = workcenterId.process_type

        return_values['customer_description'] = workcenterId.standard_description

        #data dictionaries which would ne updated with values in Workcenter
        
        qty_params = {
            'workcenterId':workcenterId,
            'param_number_out':param_number_out,
            'material':material,      
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
                return_values['lineName'] = workcenterId.name

            elif self.option_type == 'material':
                self.update_field_values(material,qty_params,cost_params,fieldUpdated,qty)
                return_values['lineName'] = material.name

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
            self.update_values(qty_params,return_values,qty)  
       
        
        


    def update_values(self,qty_params,return_values,qty):        
        for record in self:
            record['lineName'] = return_values['lineName'] if 'lineName' in return_values else ''
            record['customer_description'] = return_values['customer_description'] if 'customer_description' in return_values else ''
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
    
    def UpdateRequiredFields(self):
        for record in self:
            if record.workcenterId:
                model_fields = {x:False for x in record._fields if x.startswith('req_') }
                fields = {x.name:True for x in record.workcenterId.process_type.requiredFields}
                record.update(model_fields)
                record.update(fields)
                