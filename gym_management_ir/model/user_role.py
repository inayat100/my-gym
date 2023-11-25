from odoo import models,fields

class UserRole(models.Model):
    _inherit = "res.users"

    user_role = fields.Selection([('meneger','Manager'),('trainer','Trainer'),('member','Member')],tracking=True)