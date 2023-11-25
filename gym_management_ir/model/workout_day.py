from odoo import models , fields,api

class WorkoutDay(models.Model):
    _name = "workout.day"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char("Name",tracking=True)
    