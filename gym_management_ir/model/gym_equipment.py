from odoo import models , fields,api

class GymEquipment(models.Model):
    _name = "gym.equipment"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char("Name",tracking=True)
    