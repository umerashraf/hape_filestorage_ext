# -*- coding: utf-8 -*-
import json
import logging
from odoo import http, _
from odoo.http import  request
from odoo.addons.mail.controllers import discuss
from odoo.addons.web.controllers.main import serialize_exception,clean

_logger = logging.getLogger(__name__)

class DiscussController(discuss.DiscussController):
    
    @http.route()
    def mail_attachment_upload(self, ufile, thread_id, thread_model, is_pending=False, **kwargs):
        
        files = request.httprequest.files.getlist('ufile')
        res = None
        offending_files = []
                
        for ufile in files:
            allowed, offended_rule = request.env['attachment.upload.rule'].is_allowed(ufile.filename, thread_model)
            if not allowed:
                msg = _('File extension for %s not allowed due to rule: %s' % (ufile.filename, offended_rule))
                offending_files.append({
                    'filename': clean(ufile.filename),
                    'error': msg
                    })

        if offending_files:
            res = request.make_response(
                data=json.dumps({'error': "{0}\n{1}".format(offending_files[0]['filename'], offending_files[0]['error'])}),
                headers=[('Content-Type', 'application/json')]
            )

        else: 
            res = super(DiscussController, self).mail_attachment_upload(ufile, thread_id, thread_model, is_pending, **kwargs)
            
        return  res
    
    
    