from odoo import api, fields, models, SUPERUSER_ID, _
import logging
_logger = logging.getLogger(__name__)

class AttachmentType(models.Model):
    _name = "ir.attachment.type"
    name  = fields.Char(string="Name", required=True)

class IrAttachment(models.Model):
    _inherit  = "ir.attachment"
    file_type = fields.Many2one('ir.attachment.type',string="File Type", required=True)
    
    @api.model_create_multi
    def create(self, vals_list):
        attachment = super(IrAttachment, self).create(vals_list)
        if attachment.type=="binary" and attachment.res_model:
            storage_backend = self.env["storage.backend"].search([("res_model","=",attachment.res_model)],limit=1)
            if storage_backend:
                file = self.env["storage.file"].create({
                    "backend_id"    :storage_backend.id,
                    "company_id"    :self.env.company.id,
                    "data"          :attachment.datas,
                    "file_type"     :False,
                    "name"          :attachment.name
                })
                new_attachment = self.env["ir.attachment"].create({
                    "type"              :'url',
                    "name"              :file.name,
                    "url"               :file.url,
                    "mimetype"          :attachment.mimetype,
                    "res_model"         :attachment.res_model,
                    "res_id"            :attachment.res_id,
                    "res_name"          :attachment.res_name,
                    "index_content"     :attachment.index_content
                })
                attachment.unlink()
                return new_attachment
        return attachment
