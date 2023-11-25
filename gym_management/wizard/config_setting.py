from odoo import models , fields,api

class BodyPart(models.TransientModel):
    _inherit = "res.config.settings"


    operation_type = fields.Selection([("cancel_only","Cancel Only"),("cancel_to_draft","Cancel And Reset to Draft"),("cancel_delete","Cancel Delete")])
    cancel_receipt = fields.Boolean("Cancel Receipt")
    cancel_bill_payment = fields.Boolean("Cancel Bill And Payment")