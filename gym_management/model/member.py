from odoo import models , fields,api
import datetime
from odoo.exceptions import ValidationError

class Member(models.Model):
    _name = "member"
    _inherit = ['mail.thread','mail.activity.mixin']


    @api.model
    def create(self,vals): 
       sno = self.env['ir.sequence'].next_by_code('member')
       vals['sequence_no'] = str(sno)
       partner_id = self.env['res.partner'].create({
        'name':vals.get('name'),
        'email':vals.get('email'),
        'image_1920':vals.get('image',False),
        'phone':vals.get('phone') or False, 
        'city':vals.get('city') or False, 
        'street':vals.get('street') or False,  
        'zip':vals.get('zip') or False, 
        'country_id':vals.get('country_id') or False, 
        'state_id':vals.get('state_id') or False,
        'is_member':True 
       })
       user_id = self.env['res.users'].create({
        'name':vals.get('name'),
        'email':vals.get('email'),
        'login':vals.get('email'),
        'partner_id':partner_id.id
       })
       vals['partner_id'] = partner_id.id
       vals['user_id'] = user_id.id

       res = super(Member,self).create(vals)
       if vals.get('membership_id'):
        res.panding_amount = res.membership_id.fees
        res.membership_history_lines = [(0, 0, { 
                'date': datetime.datetime.today(),
                'membership_id': res.membership_id.id,
                'fees': res.membership_id.fees,
                'join_date': res.join_date,
                'end_date': res.end_date
            })]
       return res

    def write(self, vals):
        res = super(Member,self).write(vals)
        if vals.get('membership_id'):
            for obj in self:
                obj.panding_amount = obj.membership_id.fees
                self.env['membership.history'].create({
                    'member_id':obj.id,
                    'date': datetime.datetime.today(),
                    'membership_id':obj.membership_id.id,
                    'fees':obj.fee,
                    'join_date':obj.join_date,
                    'end_date':obj.end_date
                })
        for this in self:
            user_id = self.env['res.users'].browse(this.user_id.id)
            partner_id = self.env['res.partner'].browse(this.partner_id.id)
            employee_id = self.env['hr.employee'].browse(this.employee_id.id)
            if vals.get('name') or vals.get('email') or vals.get('image'):
                user_id.update({
                'name':this.name,
                'email':this.email,
                'login':this.email,
            })
                employee_id.update({
                'name': this.name,
                'image_1920': this.image,
            })
            partner_id.update({
            'name':this.name,
            'email':this.email,
            'image_1920':this.image,
            'phone':this.phone, 
            'city':this.city, 
            'street':this.street,  
            'zip':this.zip, 
            'country_id':this.country_id.id, 
            'state_id':this.state_id.id,
            })
        return res

    def creat_employee(self):
        for this in self:
            employee_id = self.env['hr.employee'].create({
                'name': this.name,
                'image_1920': this.image,
                'user_id': this.user_id.id
            })
            this.employee_id = employee_id.id
            this.is_employee = True

    @api.onchange('membership_id')
    def _onchange_membership_id(self):
        for this in self:
            this.fee = this.membership_id.fees
            if this.join_date:
                add_days = this.membership_id.number_of_month * 30
                end_date = datetime.timedelta(days=add_days)
                self.end_date = self.join_date + end_date

    @api.onchange('trainer_id')
    def _onchange_trainer_id(self):
        for this in self:
            this.skills = this.trainer_id.skills.ids

    def name_get(self):
        result = []
        for rec in self:
            name =  ' [ ' + rec.sequence_no + ' ] ' + rec.name
            result.append((rec.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if not recs:
            recs = self.search(['|','|',('name', operator, name),('id', operator, name),('sequence_no', operator, name)] + args, limit=limit)
        return recs.name_get()
        
    def invoices(self):
        ids = []
        for this in self.invoice_ids:
            ids.append(this.id)
        return{
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_type': 'form',
            'domain':[('id','in',ids)]
            }

    def create_membership_invoice(self):
        for this in self:
            if this.panding_amount > 0.0:
                return{
                'type': 'ir.actions.act_window',
                'name': 'Invoice Amount Fee',
                'view_mode': 'form',
                'res_model': 'how.many.amount',
                'view_type': 'form',
                'target': 'new',
                }
            else:
                raise ValidationError(f"Your Payable amount in {this.panding_amount}")

    def member_left(self):
        for this in self:
            this.status = 'left'
            user_id = self.env['res.users'].browse(this.user_id.id)
            partner_id = self.env['res.partner'].browse(this.partner_id.id)
            employee_id = self.env['hr.employee'].browse(this.employee_id.id)
            this.active = False
            user_id.active = False
            partner_id.active = False
            if employee_id:
                employee_id.active = False
        
    def member_join(self):
        for this in self:
            this.active = True
            if this.join_date:
                template_member = self.env.ref('gym_management.member_join_mail_template')
                template_member.send_mail(this.id)
                if this.trainer_id:
                    template_trainer_to_member = self.env.ref('gym_management.trainer_to_member_mail_template')
                    template_trainer_to_member.send_mail(this.id)
                user_id = self.env['res.users'].browse(this.user_id.id)
                partner_id = self.env['res.partner'].browse(this.partner_id.id)
                employee_id = self.env['hr.employee'].browse(this.employee_id.id)
                this.active = True
                user_id.active = True
                partner_id.active = True
                if employee_id:
                    employee_id.active = True
                this.status = 'joined'
            
            else:
                raise ValidationError("Please select the join date befor join")

        
    def view_employee(self):
        for this in self:
            return{
                'type': 'ir.actions.act_window',
                'name': 'Emplayee',
                'view_mode': 'kanban,form',
                'res_model': 'hr.employee',
                'view_type': 'form',
                'domain':[('id','=',this.employee_id.id)]
                }

    def cron_member_method(self):
        today = datetime.date.today()
        last_date = today + datetime.timedelta(days=7)
        due_date = self.env['member'].search([('due_date','=',last_date)])
        new_membership = self.env['member'].search([('end_date','=',last_date)])
        if due_date:
            for p in due_date:
                template_due_date = self.env.ref('gym_management.due_amount_mail_template')
                template_due_date.send_mail(p.id)
        if new_membership:
            for n in new_membership:
                template_new_membership = self.env.ref('gym_management.new_membership_mail_template')
                template_new_membership.send_mail(n.id)


    name=fields.Char("User Name")
    sequence_no= fields.Char("Member Id",index=True,readonly=True,copy=False,default='new')

    partner_id = fields.Many2one("res.partner",string="User",tracking=True)
    user_id = fields.Many2one("res.users",string="User",tracking=True)
    employee_id = fields.Many2one("hr.employee",string="Employee",tracking=True)
    is_employee = fields.Boolean("Created employee",default=False)

    street = fields.Char("Street")
    city = fields.Char("City")
    zip = fields.Char("Zip")
    state_id = fields.Many2one("res.country.state",string="State")
    country_id = fields.Many2one("res.country",string="Country")
    phone = fields.Char("Mobile",tracking=True)
    email = fields.Char("Email",tracking=True)
    image = fields.Binary("Image")

    status = fields.Selection([("waiting","Waiting"),("joined","Joined"),('left','Left')],default='waiting',tracking=True)

    gender = fields.Selection([("male","Male"),("female","Female")],tracking=True)
    dob = fields.Date("Date Of Birth",tracking=True)
    age = fields.Integer("Age",tracking=True)
    join_date = fields.Date("Join Date",tracking=True)
    end_date = fields.Date("Ending Date",tracking=True)
    due_date = fields.Date("Due Date",tracking=True)
    panding_amount = fields.Float("Panding Amount")

    membership_id = fields.Many2one("membership",string="Membership",tracking=True)
    fee = fields.Float("Fee")
    trainer_id = fields.Many2one("trainer",string="Trainer",tracking=True)
    skills = fields.Many2many("trainer.skills",string="Skills")

    member_workout_plan_lines = fields.One2many("member.workout.plan.line","member_id",string="Member Workout Plan Lines")
    member_Diet_plan_lines = fields.One2many("member.diet.plan.line","member_id",string="Member Diet Plan Lines")
    membership_history_lines = fields.One2many("membership.history","member_id",string="Membership History Lines")
    invoice_ids = fields.Many2many("account.move",string="invoice_ids")
    invoice_count = fields.Integer()
    active = fields.Boolean("Active",default=True)

class MemberWorkoutPlanLine(models.Model):
    _name = "member.workout.plan.line"
    _inherit = ['mail.thread','mail.activity.mixin']

    member_id = fields.Many2one("member",string="Member",tracking=True)
    workout_plan_id = fields.Many2one("workout.plan",string="Workout Plan",tracking=True)
    from_date = fields.Date("From",tracking=True)
    to_date = fields.Date("To")

class MemberDietPlanLine(models.Model):
    _name = "member.diet.plan.line"
    _inherit = ['mail.thread','mail.activity.mixin']

    member_id = fields.Many2one("member",string="Member")
    diet_plan_id = fields.Many2one("diet.plan",string="Diet Plan",tracking=True)
    from_date = fields.Date("From",tracking=True)
    to_date = fields.Date("To",tracking=True)

class MembershipHistory(models.Model):
    _name = "membership.history"
    _order = "id desc"

    member_id = fields.Many2one("member",string="Member Id")
    date = fields.Date("Date")
    membership_id = fields.Many2one("membership",string="Membership")
    fees = fields.Float("Fees")
    join_date = fields.Date("Join Date")
    end_date = fields.Date("End Date")

    





    # Cannot create unbalanced journal entry. Ids

    
