from odoo import models , fields,api

class TrainerSkills(models.Model):
    _name = "trainer.skills"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char("Name",tracking=True)
    experience = fields.Integer("Experience in years",tracking=True)

    