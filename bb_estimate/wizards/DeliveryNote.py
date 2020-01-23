import odoo
from odoo import models, fields, api
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError

class DeliveryLines(models.TransientModel):
    _name = 'bb_estimate.delivery_lines'
    _desc = 'Delivery Note Lines'

    name = fields.Char('Name')
    value = fields.Char('Quantity')
    note_id = fields.Many2one('bb_estimate.delivery_note')
    picking_line_id = fields.Many2one('bb_estimate.delivery_material_lines','Picking Line')

class DeliveryNote(models.TransientModel):
    _name = 'bb_estimate.delivery_note'
    _desc = 'Delivery Note for materials'

    lines = fields.One2many('bb_estimate.delivery_lines','note_id','Lines')
    delivery_id = fields.Many2one('stock.picking', string="Delivery")

    @api.onchange('delivery_id')
    def PrepareLines(self):
        for record in self:
            if record.delivery_id:
                if record.delivery_id.Materials:
                    record.lines = [(0,0,{'name':x.Name,'value':x.Quantity,'picking_line_id':x.id}) for x in record.delivery_id.Materials]
                else:
                    estimate = record.delivery_id.getEstimateData()
                    if estimate:
                        record.lines = [(0,0, {
                                'name': line.JobTicketText,
                                'value': '%0.0f'%((line['param_finished_quantity_'+line.estimate_id.selectedQuantity] * line.estimate_id.SelectedQtyRatio) + (line.param_finished_quantity_run_on * line.estimate_id.selectedRatio))
                            }) for line in estimate.estimate_line if (not line.isExtra) and (line.option_type == 'material') and (line.documentCatergory not in ['Packing','Despatch']) and (line.JobTicketText)]

    def Confirm(self):
        self.delivery_id.write({"Materials":[(1 if x.picking_line_id else 0,x.picking_line_id.id if x.picking_line_id else 0,{'Name':x.name,'Quantity':x.value}) for x in self.lines if int(x.value) > 0]})
        return #self.env.ref('bb_estimate.delievery_note_two').report_action(self)                            

    


