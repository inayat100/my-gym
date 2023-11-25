from odoo import models , fields,api

class WorkoutPlan(models.Model):
    _name = "workout.plan"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char("Name",tracking=True)
    workout_days_ids = fields.Many2many("workout.day",string="Workout Days",tracking=True)
    workout_plan_line  = fields.One2many("workout.plan.line","workout_plan_id",string="Workout Plan Line")

class WorkoutPlanLine(models.Model):
    _name = "workout.plan.line"

    workout_plan_id = fields.Many2one("workout.plan",string="Workout Plan Id")

    exercise_id =fields.Many2one("exercise",string="Exercise",tracking=True)
    body_part_id = fields.Many2one("bodypart",string="Body Part",tracking=True)
    equipment_id = fields.Many2one("gym.equipment",string="Equipment",tracking=True)
    sets = fields.Integer("Sets",tracking=True)
    repeat = fields.Integer("Repeat",tracking=True)
    weight = fields.Integer("Weight(kgs)",tracking=True)
    