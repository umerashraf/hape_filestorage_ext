from odoo import _, fields, models

class storageBackend(models.Model):
    _inherit = "storage.backend"

    res_model = fields.Char(string="For Model", required=True)
