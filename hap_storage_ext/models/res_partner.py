from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_id             = fields.Char(string='Customer ID')
    primary_contact_person  = fields.Char(string='Contact Person')
