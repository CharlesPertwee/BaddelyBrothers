# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Leads(models.Model):
    _inherit = 'crm.lead'
    _name = 'crm.lead'
    
    typeOfLead = fields.Selection([('Trade Counter','Trade Counter'),('Bespoke','Bespoke')],string="Type Of Opportunity",default="Trade Counter")
        
    @api.multi
    def write(self,vals):
        stage = self.env['crm.stage'].sudo().search([('id','=',vals['stage_id'])])
        
        if (self.typeOfLead == stage.typeOfLead) or (stage.isCommon):
            # stage change: update date_last_stage_update
            if 'stage_id' in vals:
                vals['date_last_stage_update'] = fields.Datetime.now()
            if vals.get('user_id') and 'date_open' not in vals:
                vals['date_open'] = fields.Datetime.now()
            # stage change with new stage: update probability and date_closed
            if vals.get('stage_id') and 'probability' not in vals:
                vals.update(self._onchange_stage_id_values(vals.get('stage_id')))
            if vals.get('probability', 0) >= 100 or not vals.get('active', True):
                vals['date_closed'] = fields.Datetime.now()
            elif 'probability' in vals:
                vals['date_closed'] = False
            return super(Leads, self).write(vals)
        else:
            raise ValidationError(_('Selected opportunity is of type %s, It cannot be moved to the selected stage %s'%(self.typeOfLead,stage.name)))
            
        
class Stages(models.Model):
    _inherit = 'crm.stage'
    _name = 'crm.stage'
    
    typeOfLead = fields.Selection([('Trade Counter','Trade Counter'),('Bespoke','Bespoke')],string="Opportunity Type",default="Trade Counter")
    isCommon = fields.Boolean(string="Is Common")
