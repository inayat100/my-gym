from odoo import models , fields,api

class BodyPart(models.Model):
    _name = "bodypart"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char("Name",tracking=True)