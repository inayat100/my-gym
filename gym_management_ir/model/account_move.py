from odoo import models , fields,api

class AccountMoveInherit(models.Model):
    _inherit = "account.move"


    def due_method(self):
        for this in self:
            obj = self.env['member'].search([('partner_id','=',this.partner_id.id)])
            if obj:
                data = {'due_date':obj.due_date,'due_amount':obj.panding_amount}
                return data
            else:
                return {}

    payment_mode = fields.Char("Payment type")


  