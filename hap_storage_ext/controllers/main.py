# -*- coding: utf-8 -*-
from odoo.addons.base_rest.controllers.main import RestController


class ValidationRestController(RestController):
    _root_path = "/api/"
    _collection_name = "hap_portal.services"
    
    
    