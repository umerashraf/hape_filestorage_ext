from odoo import _, fields, models

class saleOrder(models.Model):
    _inherit = "sale.order"

    attachment_ids = fields.One2many('ir.attachment', 'res_id', string='Attachments', domain=[('res_model', '=', 'sale.order')])

