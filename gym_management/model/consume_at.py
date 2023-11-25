from odoo import models , fields,api

class ConsumeAt(models.Model):
    _name = "consume.at"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char("Name",tracking=True)