from odoo import models,fields,api

class cancelResion(models.TransientModel):
    _name = "cancel.resion"

    def cancel_resion(self):
        for this in self:
            obj = self.env['special.session'].browse(self._context.get('active_id'))
            obj.update({
                'cancel_resion':this.name,
                'status': 'canceld',
                'cancel_bool':True,
            })
            template_cancel = self.env.ref('gym_management.cancel_session_template')
            template_cancel.send_mail(obj.id)
    name = fields.Text("cancel Resion")