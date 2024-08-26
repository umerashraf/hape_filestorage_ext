from odoo import models
from odoo.exceptions import AccessDenied
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class Http(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        """
        Inherit: Update the value of 'max_attachment_size' to the session. # T7329
        """
        session_info = super().session_info()
        IrConfigSudo = self.env["ir.config_parameter"].sudo()
        max_attachment_size = int(
            IrConfigSudo.get_param(
                "attachment_size_restriction.attachment_size_limit",
                default=10 * 1024 * 1024,  # 10 MB
            )
        )
        session_info.update({"max_attachment_size": max_attachment_size})
        return session_info
    
    @classmethod
    def _auth_method_token_access_denied(cls):
        ip = request.httprequest.environ["REMOTE_ADDR"] if request else "n/a"

        # this text is part of the fail2ban definition - don't change w/o reason
        # or coordination with ops!
        _logger.info(f"Auth by Authorization Token failed from {ip}")

    @classmethod
    def _auth_method_token(cls):
        """
        Provides auth="token" authn/authz method.

        This makes use of the models provided by the oca/auth_api_key module,
        but then provides a separately named authentication mechanism.  Unlike
        the original, this uses the regular `Authorization` header, which is
        already added to the CORS Access-Control-Allow-Headers by Odoo itself.
        """
        authorization = request.httprequest.headers.get("Authorization")
        if not authorization:
            cls._auth_method_token_access_denied()
            raise AccessDenied("Authorization header missing")

        if not authorization.startswith("Token "):
            cls._auth_method_token_access_denied()
            raise AccessDenied("Authorization header format not supported")

        api_key = authorization[6:]
        request.uid = 1
        auth_api_key = request.env["auth.api.key"]._retrieve_api_key(api_key)
        if not auth_api_key:
            cls._auth_method_token_access_denied()
            raise AccessDenied()

        # Taken from oca/auth_api_key 1:1:
        #
        # reset _env on the request since we change the uid...
        # the next call to env will instantiate an new
        # odoo.api.Environment with the user defined on the
        # auth.api_key
        request._env = None
        request.uid = auth_api_key.user_id.id
        request.auth_api_key = api_key
        request.auth_api_key_id = auth_api_key.id
        return True

