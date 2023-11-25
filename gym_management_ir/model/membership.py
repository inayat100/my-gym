from odoo import models , fields,api

class MemberShip(models.Model):
    _name ="membership"
    _inherit = ['mail.thread','mail.activity.mixin']

    @api.onchange('membership_product_id')
    def _onchange_product_id(self):
        for this in self:
            this.name = this.membership_product_id.name



    name = fields.Char("Name",tracking=True)
    number_of_month = fields.Integer("Number Of Month",tracking=True)
    fees = fields.Char("Fees",tracking=True)
    membership_product_id = fields.Many2one("product.product",string="Membership Product",tracking=True)
    details = fields.Text("Details")

