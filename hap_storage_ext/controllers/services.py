import json
import logging
import base64
from http import HTTPStatus

from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi
from odoo.addons.datamodel.core import Datamodel
from odoo.http import Response, request
from odoo.tools import date_utils
from odoo import _
from marshmallow import fields
_logger = logging.getLogger(__name__)

class AttachmentUploadParams(Datamodel):
    _name = "attachment.data.param"

    data            = fields.Raw(required=True,metadata={'type': 'string', 'format': 'binary'})
    resource_model  = fields.String(required=True)
    resource_id     = fields.Number(required=True)

class AttachmentUploadService(Component):
    _inherit        = "base.rest.service"
    _name           = "attachment.service"
    _usage          = "attachment"
    _collection     = "hap_portal.services"
    _description    = """
        Attachment services
        Services developed to upload attachments
    """

    def _get_rec_by_id(self, resource, resource_id):
        resModel = self.env[resource]
        record = resModel.browse(resource_id)
        return record
    
    def _file_valid(self, ufile, file_binary, resource_model):
        if ufile and ufile.mimetype:
            try:
                allowed, offended_rule = request.env['attachment.upload.rule'].is_allowed(ufile.filename, resource_model)
                
                if not allowed or allowed==False:
                    msg = _('File extension for %s not allowed due to rule: %s' % (ufile.filename, offended_rule))
                    return {'status':False,'message':msg}
                return {'status':True}
            except Exception:
                attachmentData = {'error': ("Something horrible happened"), 'filename': ufile.filename}
                _logger.exception("Fail to upload attachment %s" % ufile.filename)
                return {'status':False,'message':"Fail to upload attachment %s" % ufile.filename}

    @restapi.method(
        [(["/create"], "POST")],
        input_param=restapi.Datamodel("attachment.data.param"),
        auth="token",
        cors="*",
    )
    def post_attachment(self, attachment_data_params):
        ufile           = attachment_data_params.data
        file_binary     = ufile.read()
        resource_model  = attachment_data_params.resource_model
        resource_id     = int(attachment_data_params.resource_id)
        record          = self._get_rec_by_id(resource_model, resource_id)
        if not record:
            return Response(status=HTTPStatus.NOT_FOUND)
        file_valid      = self._file_valid(ufile, file_binary, resource_model)
        if not file_valid or file_valid["status"]==False:
            return Response(file_valid["message"], status=HTTPStatus.BAD_REQUEST)
        vals = {
            'name'      : ufile.filename,
            'datas'     : base64.b64encode(file_binary),
            'res_id'    : resource_id,
            'res_model' : resource_model,
            'mimetype'  : ufile.mimetype,
            'type'      : 'binary'
        }
        Attach = request.env['ir.attachment']
        attachment = Attach.create(vals)
        response_data = json.dumps(
            {"success": True, "attachment_id": attachment.id}, default=date_utils.json_default
        )
        return Response(response_data, status=HTTPStatus.OK)