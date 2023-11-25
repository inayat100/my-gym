from odoo import models , fields,api

class Exercise(models.Model):
    _name = "exercise"
    _inherit = ['mail.thread','mail.activity.mixin']


    name = fields.Char("Name",tracking=True)
    body_part_id = fields.Many2one("bodypart",string="Body Part",tracking=True)
    equipment_id = fields.Many2one("gym.equipment",string="Equipment",tracking=True)
    steps = fields.Text("Steps",tracking=True)
    benefits = fields.Text("Benefits",tracking=True)
    