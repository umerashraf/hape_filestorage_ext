from odoo import _, fields, models

class storageBackend(models.Model):
    _inherit = "storage.backend"

    res_model = fields.Char(string="For Model", required=True)

class StorageFile(models.Model):
    _inherit = "storage.file"

    def unlink(self):
        attachment = self.env["ir.attachment"].search([("storage","=",self.id)])
        if attachment:
            attachment.unlink()
        super(StorageFile, self).unlink()
        return True