# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
import logging
import os
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class AttachmentUploadRule(models.Model):
    _name        = "attachment.upload.rule"
    _description = "Attachment Upload rules"
    _order       = 'sequence'
    
    name         = fields.Char("Name",required=True)
    models       = fields.Many2many('ir.model',string='Model')
    blacklist    = fields.Char("Black List",help="Comma separated list of file extensions to be blacklsited")
    whitelist    = fields.Char("White List",help="Comma separated list of file extensions to be whitelisted")
    sequence     = fields.Integer('Sequence', default=0)
    
    @api.onchange('blacklist')
    def _blackList_change(self):
        self.ensure_one()
        if self.blacklist and self.whitelist:
            self.blacklist = None
            raise ValidationError('You can not set both blacklist and whitelist fields ')
    
    @api.onchange('whitelist')
    def _whiteList_change(self):
        self.ensure_one()
        if self.blacklist and self.whitelist:
            self.whitelist = None
            raise ValidationError('You can not set both blacklist and whitelist fields ')
        
    def is_allowed(self, filename, model):
        """
        Check all rules that applies for the given model
            - if found 
                - and blacklist is set then apply the blacklist and if it matches then reject it. 
                - if whitelist is set then apply the whitelist. if nothing matching then reject it
            -if not found then check for the global rule where the "models" is not set and then apply the same logic as before 
             
        @return: (True if allowed, None) or (False if not allowed, <rule name>) 
        """
        is_allowed, rule_name = True, None
         
        ext = os.path.splitext(filename)[1][1:].lower().strip()
         
        #TODO first search the model order by sequence
        rules = self.env['attachment.upload.rule'].sudo().search(['|', ('models', '=', False), ('models', '=', model)]) 
 
        for rule in rules.filtered(lambda r: r.models) + rules.filtered(lambda r: not r.models) :
            if rule.blacklist and ext in [x.lower().strip() for x in rule.blacklist.split(',')]:
                 is_allowed, rule_name = False, rule.name
                 break
            elif rule.whitelist and ext not in [x.lower().strip() for x in rule.whitelist.split(',')]:
                is_allowed, rule_name = False, rule.name
                break
         
        return is_allowed, rule_name
    
  
    
   
    
    