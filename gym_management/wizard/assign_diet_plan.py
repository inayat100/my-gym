from odoo import models,fields,api

class AssignDietPlan(models.TransientModel):
    _name = "assign.diet.plan"
    
    def get_partner_ids(self, member_ids):
        u_ids = []
        for this in member_ids:
            u_ids.append(this.partner_id.id)
        return str([u_ids]).replace('[', '').replace(']', '')

    def assign_diet_plan(self):
        for this in self.member_ids:
            self.env['member.diet.plan.line'].create({
                    'member_id':this.id,
                    'diet_plan_id':self.diet_plan_id.id,
                    'from_date':self.from_date,
                    'to_date':self.to_date,
                })
        template_diet = self.env.ref('gym_management.diet_mail_template')
        template_diet.send_mail(self.id)

    
    member_ids = fields.Many2many("member",string="Members")
    diet_plan_id = fields.Many2one("diet.plan",string="Diet Plans")
    from_date = fields.Date("From")
    to_date = fields.Date("To")