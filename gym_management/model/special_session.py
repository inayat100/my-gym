from odoo import models,fields,api

class SpecialSession(models.Model):
    _name = "special.session"
    _inherit = ['mail.thread','mail.activity.mixin']

    def done(self):
        self.status = 'done_successfully'

    def cancel(self):
        return{
        'type': 'ir.actions.act_window',
        'name': 'cancel Special Session',
        'view_mode': 'form',
        'res_model': 'cancel.resion',
        'view_type': 'form',
        'target':'new',
        }

    def get_partner_ids(self, member_ids):
        u_ids = []
        for obj in member_ids:
            u_ids.append(obj.partner_id.id)
        return str([u_ids]).replace('[', '').replace(']', '')

    def cancel_ids(self,member_ids,trainer_ids):
        ids = []
        if member_ids:
            for member_id in member_ids:
                ids.append(member_id.partner_id.id)
        if trainer_ids:
            for trainer_id in trainer_ids:
                ids.append(trainer_id.partner_id.id)
        return str([ids]).replace('[', '').replace(']', '')

    def invite_attendees(self):
        template_member = self.env.ref('gym_management.invite_member_template')
        template_trainer = self.env.ref('gym_management.invite_trainer_template')
        if self.member_ids:
            template_member.send_mail(self.id)
        if self.trainer_ids:
            template_trainer.send_mail(self.id)
        self.status = 'invitation_sent'

    def back_to_panding(self):
        self.status = 'pending'
        self.cancel_bool = False


    name = fields.Char("Name",tracking=True)
    start_at = fields.Datetime("Start At",tracking=True)
    end_at = fields.Datetime("End At",tracking=True)
    member_ids = fields.Many2many("member",string="Member",tracking=True)
    trainer_ids = fields.Many2many("trainer",string="Trainer",tracking=True)
    description = fields.Text("Description",tracking=True)
    cancel_resion = fields.Text("cancel Resion",tracking=True)
    status = fields.Selection([("pending","Pending"),("invitation_sent","Invitation Sent"),('done_successfully','Done Successfully'),('canceld','canceld')],default='pending',copy=False)
    cancel_bool = fields.Boolean(default=False)
