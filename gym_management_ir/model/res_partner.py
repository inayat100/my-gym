from odoo import models,fields,api

class MyPartner(models.Model):
    _inherit = "res.partner"


    is_member = fields.Boolean("Member",default=False)
    is_trainer = fields.Boolean("Trainer",default=False)