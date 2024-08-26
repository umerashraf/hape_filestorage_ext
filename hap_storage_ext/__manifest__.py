{

    # App information
    'name': 'Storage Extended',
    'version': '17.0.0.1',
    'category': 'Services',
    'license': 'OPL-1',
    'summary': """ 
    """,
    'description': """
    """,

    # Dependencies
    'depends': ['base','web','mail','sale', 'storage_backend'],
    "data": [
        'security/ir.model.access.csv',
        "data/ir_config_parameter_data.xml",
        "views/res_config_settings_views.xml",
        'views/attachment.xml',
        'views/storage_backend.xml',
        'views/sale_order_views.xml',
        'views/ir_attachment_views.xml'
    ],
    "assets": {
        'web.assets_qweb': [
            ('after','mail/static/src/components/attachment_card/attachment_card.xml','hap_storage_ext/static/src/components/attachment_card/attachment_card.xml'),
            ('after','mail/static/src/components/attachment_delete_confirm_dialog/attachment_delete_confirm_dialog.xml','hap_storage_ext/static/src/components/attachment_delete_confirm_dialog/attachment_delete_confirm_dialog.xml'),
            ('after','mail/static/src/components/attachment_image/attachment_image.xml','hap_storage_ext/static/src/components/attachment_image/attachment_image.xml'),
        ],
        "web.assets_backend": [
            "hap_storage_ext"
            "/static/src/components/file_uploader/file_uploader.esm.js",
            ('after','mail/static/src/models/attachment_card/attachment_card.js','hap_storage_ext/static/src/models/attachment_card/attachment_card.js'),
            ('after','mail/static/src/components/attachment_card/attachment_card.js','hap_storage_ext/static/src/components/attachment_card/attachment_card.js'),
            ('after','mail/static/src/components/attachment_delete_confirm_dialog/attachment_delete_confirm_dialog.js','hap_storage_ext/static/src/components/attachment_delete_confirm_dialog/attachment_delete_confirm_dialog.js'),
            ('after','mail/static/src/models/attachment_image/attachment_image.js','hap_storage_ext/static/src/models/attachment_image/attachment_image.js'),
            ('after','mail/static/src/components/attachment_image/attachment_image.js','hap_storage_ext/static/src/components/attachment_image/attachment_image.js'),
            
        ],
        
    },

    # Odoo Store Specific
    'images': [],

    # Author
    'author':'HAPE Mountain Software GmbH',
    'maintainer':'HAPE Mountain Software GmbH',
    'website':'https://mountain.co.at',

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
