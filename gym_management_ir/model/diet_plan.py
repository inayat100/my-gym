from odoo import models , fields,api

class DietPlan(models.Model):
    _name = "diet.plan"
    _inherit = ['mail.thread','mail.activity.mixin']


    name = fields.Char("Name",tracking=True)
    diet_plan_line = fields.One2many("diet.plan.line","diet_plan_id",string="Diet Plan Line")


class DietPlanLine(models.Model):
    _name = "diet.plan.line"
    _inherit = ['mail.thread','mail.activity.mixin']


    diet_plan_id = fields.Many2one("diet.plan",string="Diet Plan Id",tracking=True)
    diet_food_id = fields.Many2one("diet.food",string="Diet Food",tracking=True)
    quantity = fields.Float("Quantity",tracking=True)
    consume_at = fields.Many2one("consume.at",string="Consume At",tracking=True)

