from odoo import models,fields,api

class GymActivity(models.Model):
    _name = "gym.activity"
    _inherit = ['mail.thread','mail.activity.mixin']


    member_id = fields.Many2one("member",string="Member",tracking=True)
    date = fields.Date("Date")
    exercise_id = fields.Many2one("exercise",string="Exercise",tracking=True)
    equipment_id = fields.Many2one("gym.equipment",string="Equipment",tracking=True)
    sets = fields.Integer("Sets",tracking=True)
    repeat = fields.Integer("Repeat",tracking=True)
    weight = fields.Float("Weight(Kg)",tracking=True)