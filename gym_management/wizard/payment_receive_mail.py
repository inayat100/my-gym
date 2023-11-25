from odoo import models,fields,api


class PaymentReceiveMail(models.TransientModel):
    _inherit = 'account.payment.register'



    def action_create_payments(self):
        for this in self:
            res = super(PaymentReceiveMail,self).action_create_payments()
            am= self.env['account.move'].browse(self._context.get('active_id'))
            if am:
                am.update({
                    'payment_mode':this.journal_id.name
                })
                template_payment = self.env.ref('gym_management.payment_receive_mail_template')
                template_payment.send_mail(am.id)
        return res


