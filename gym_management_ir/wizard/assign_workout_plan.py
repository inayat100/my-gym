from odoo import models, fields


class AssignWorkoutPlan(models.TransientModel):
    _name = "assign.workout.plan"

    def assign_workout_plan(self):
        for this in self.member_ids:
            for plan_id in self.workout_plan_ids:
                self.env['member.workout.plan.line'].create({
                    'member_id': this.id,
                    'workout_plan_id': plan_id.id,
                    'from_date': self.from_date,
                    'to_date': self.to_date,
                })

    member_ids = fields.Many2many("member", string="Members")
    workout_plan_ids = fields.Many2many("workout.plan", string="Workout Plans")
    from_date = fields.Date("From")
    to_date = fields.Date("To")
