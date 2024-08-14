/** @odoo-module **/

import {
    registry
} from '@mail/model/model_core';
import {
    attr
} from '@mail/model/model_field';

registry['mail.attachment_image'].factory = (function(_super) {
    return function() {

        let AttachmentImage = _super.apply(this, arguments);
        // adding a field to the model.attachement_card
        Object.assign(AttachmentImage.fields, {
            hasEditConfirmDialog: attr({
                default: false,
            })
        });
        return AttachmentImage;
    };

})(registry['mail.attachment_image'].factory);