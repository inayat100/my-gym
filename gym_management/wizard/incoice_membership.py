from odoo import models,fields,api
from odoo.exceptions import ValidationError
class HowmanyAmount(models.TransientModel):
    _name = "how.many.amount"

    invoice_type = fields.Selection([('delivered','Regular Invoice'),('percentags','Down Payment(Percentags)'),('fixed','Down Payment (Fixed Amount)')],default='percentags')
    amount = fields.Float("Amount")
    percentage = fields.Float("Percentage: %")
    deposit_account_id = fields.Many2one("account.account",string="Income Account")
    deposit_tax_id = fields.Many2one("account.tax",string="Customer Taxes")
    dua_date = fields.Date("Dua Date")
    dua_amount = fields.Float("Dua amount")
    is_dua_amount = fields.Boolean("is dua amount",default=True)

   
    @api.onchange('invoice_type')
    def _onchange_invoice_type(self):
        if self.invoice_type == 'delivered':
            self.is_dua_amount = False
        else:
            self.is_dua_amount = True


    @api.onchange('percentage')
    def _onchange_percentage(self):
        for this in self:
            if this.percentage >= 0 and this.percentage <= 100:
                this_id = self.env['member'].browse(self._context.get('active_id'))
                this.amount = (this_id.panding_amount * this.percentage)/100
                if this.amount == this.dua_amount:
                    this.is_dua_amount = False
                else:
                    this.is_dua_amount = True
            else:
                raise ValidationError(f"your percentage values out of range")


    @api.onchange('amount')
    def _onchange_amount(self):
        for this in self:
            if this.amount == round(this.dua_amount,2):
                this.is_dua_amount = False
            else:
                this.is_dua_amount = True

    @api.model
    def default_get(self,fields):
        res = super(HowmanyAmount,self).default_get(fields)
        this_id = self.env['member'].browse(self._context.get('active_id'))
        if this_id.panding_amount > 0:
            res['dua_amount'] = this_id.panding_amount
        else:
            res['dua_amount'] = this_id.fee
        return res

    def create_invoice(self):
        self.create_invoice_and_view()

    def create_invoice_and_view(self):
        this_id = self.env['member'].browse(self._context.get('active_id'))
        for this in self:
            data = {}
            if this.deposit_tax_id:
                data.update({'product_id':this_id.membership_id.membership_product_id.id,'name':f"{this_id.membership_id.name} [{this_id.join_date} To {this_id.end_date}]",'quantity':1,'tax_ids':[this.deposit_tax_id.id]})
            else:
                data.update({'product_id':this_id.membership_id.membership_product_id.id,'name':f"{this_id.membership_id.name} [{this_id.join_date} To {this_id.end_date}]",'quantity':1,'tax_ids':False})

            if this.invoice_type == 'delivered':
                if this_id.panding_amount >= this.amount:
                    data.update({'price_unit':this_id.panding_amount})
                    ss = self.env['account.move'].create({
                    'partner_id': this_id.partner_id.id, 
                    'move_type':'out_invoice',
                    'invoice_date':this_id.join_date,
                    'invoice_line_ids': [(0, 0, data)],
                    })
                    ids = [ss.id]
                    for invoice_id in this_id.invoice_ids:
                        ids.append(invoice_id.id)
                    this_id.update({
                        'panding_amount':this_id.panding_amount - this.dua_amount,
                        'invoice_count': this_id.invoice_count + 1,
                        'invoice_ids':ids,
                        'due_date':this.dua_date
                    })
                else:
                    raise ValidationError(f"plase enter the right values")

            if this.invoice_type == 'percentags':
                if 100 >= this.percentage:
                    data.update({'price_unit':this.amount})
                    ss = self.env['account.move'].create({
                    'partner_id': this_id.partner_id.id, 
                    'move_type':'out_invoice',
                    'invoice_date':this_id.join_date,
                    'invoice_line_ids': [(0, 0,data)],
                    })
                    ids = [ss.id]
                    for invoice_id in this_id.invoice_ids:
                        ids.append(invoice_id.id)
                    this_id.update({
                        'panding_amount':this_id.panding_amount - this.amount,
                        'invoice_count': this_id.invoice_count + 1,
                        'invoice_ids':ids,
                        'due_date':this.dua_date
                    })
                else:
                    raise ValidationError(f"plase enter the right values")

            if this.invoice_type == 'fixed':
                if this_id.panding_amount >= this.amount:
                    data.update({'price_unit':this.amount})
                    ss = self.env['account.move'].create({
                    'partner_id': this_id.partner_id.id, 
                    'move_type':'out_invoice',
                    'invoice_date':this_id.join_date,
                    'invoice_line_ids': [(0, 0,data)],
                    })
                    ids = [ss.id]
                    for invoice_id in this_id.invoice_ids:
                        ids.append(invoice_id.id)
                    this_id.update({
                        'panding_amount':this_id.panding_amount - this.amount,
                        'invoice_count': this_id.invoice_count + 1,
                        'invoice_ids':ids,
                        'due_date':this.dua_date
                    })
                else:
                    raise ValidationError(f"plase enter the right values")

            return{
                'name':'Invoices',
                'view_type':'form',
                'res_model':'account.move',
                'res_id':ss.id,
                'type':'ir.actions.act_window',
                'view_mode':'form',
            }
    
