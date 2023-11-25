from odoo import models , fields,api

class DietFood(models.Model):
    _name = "diet.food"
    _inherit = ['mail.thread','mail.activity.mixin']


    name = fields.Char("Name",tracking=True)
    