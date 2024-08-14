/** @odoo-module **/

import {
    registry
} from '@mail/model/model_core';
import {
    attr
} from '@mail/model/model_field';

registry['mail.attachment_card'].factory = (function(_super) {
    return function() {

        let AttachmentCard = _super.apply(this, arguments);
        // adding a field to the model.attachement_card
        Object.assign(AttachmentCard.fields, {
            hasEditConfirmDialog: attr({
                default: false,
            })
        });
        return AttachmentCard;
    };

})(registry['mail.attachment_card'].factory);