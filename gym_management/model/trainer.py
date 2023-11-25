from odoo import models , fields,api
import datetime
from odoo.exceptions import ValidationError
class Trainer(models.Model):
    _name = "trainer"
    _inherit = ['mail.thread','mail.activity.mixin']

    @api.model
    def create(self,vals): 
       sno = self.env['ir.sequence'].next_by_code('trainer')
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
        'is_trainer':True 
       })
       user_id = self.env['res.users'].create({
        'name':vals.get('name'),
        'email':vals.get('email'),
        'login':vals.get('email'),
        'partner_id':partner_id.id
       })
       vals['partner_id'] = partner_id.id
       vals['user_id'] = user_id.id
       res = super(Trainer,self).create(vals)
       return res

    def write(self, vals):
        res = super(Trainer,self).write(vals)
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

    def trainer_info(self):
        for this in self:
            return{
                'type': 'ir.actions.act_window',
                'name': 'Emplayee',
                'view_mode': 'kanban,form',
                'res_model': 'hr.employee',
                'view_type': 'form',
                'domain':[('user_id.partner_id','=',this.partner_id.id)]
                }

    def trainer_left(self):
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

    
    def trainer_join(self):
        for this in self:
            self.active = True
            if this.join_date:
                template_trainer = self.env.ref('gym_management.trainer_join_mail_template')
                template_trainer.send_mail(this.id)
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
            recs = self.search(['|',('name', operator, name),('id', operator, name)] + args, limit=limit)
        return recs.name_get()

    name = fields.Char("User Name",tracking=True)

    sequence_no = fields.Char("Trainer Id",index=True,readonly=True,copy=False,default='new')

    partner_id = fields.Many2one("res.partner",string="Partner_id",tracking=True)
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
    skills = fields.Many2many("trainer.skills",string="Skills",tracking=True)
    join_date = fields.Date("Join Date",tracking=True)
    active = fields.Boolean("Active",default=True)

