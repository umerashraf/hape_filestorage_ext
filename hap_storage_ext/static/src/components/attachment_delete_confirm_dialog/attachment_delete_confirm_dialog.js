/** @odoo-module **/

import {
    AttachmentDeleteConfirmDialog
} from '@mail/components/attachment_delete_confirm_dialog/attachment_delete_confirm_dialog';

import {
    registerMessagingComponent
} from '@mail/utils/messaging_component';


Object.assign(AttachmentDeleteConfirmDialog.prototype, {
    /**
     *
     * @returns {boolean}
     */
    hasEditConfirmDialog(){
        if(this.attachment.attachmentCards.length>0)
            return this.attachment.attachmentCards[0].hasEditConfirmDialog;
        if(this.attachment.attachmentImages.length>0)
            return this.attachment.attachmentImages[0].hasEditConfirmDialog;
    },

    /**
     *
     * @returns {string}
     */
    getBody() {
        let hasEditConfirmDialog = this.hasEditConfirmDialog();
        if (hasEditConfirmDialog) {
            return _.str.sprintf(
                this.env._t(`Do you really want to modify "%s"?`),
                owl.utils.escape(this.attachment.displayName)
            );
        } else {
            return _.str.sprintf(
                this.env._t(`do you want to delete "%s"?`),
                owl.utils.escape(this.attachment.displayName)
            );
        }

    },

    /**
     * @returns {string}
     */
    getTitle() {
        let hasEditConfirmDialog = this.hasEditConfirmDialog();   
  
        if (hasEditConfirmDialog) {
            return this.env._t("Edit Confirmation");
        } else {
            return this.env._t("Confirmation");
        }

    },

    getEditLabel() {
        return this.env._t("New File name :");
    },
    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------
    /**
     * @private
     */
    _onClickCancel() {
        this._dialogRef.comp._close();
        if(this.attachment.attachmentCards.length>0)
            this.attachment.attachmentCards[0].update({
                 hasEditConfirmDialog: false
             });
        if(this.attachment.attachmentImages.length>0)
            this.attachment.attachmentImages[0].update({
                 hasEditConfirmDialog: false
             });
    },

    /**
     * @private
     */
    _onClickOk() {
        const _editInputRef = this.__owl__.refs.attachment_name;
        
        let hasEditConfirmDialog = this.hasEditConfirmDialog();   

        if ( hasEditConfirmDialog) {

            let data = {
                name: _editInputRef.value,
            };

            this.env.services.rpc({
                model: 'ir.attachment',
                method: 'update',
                args: [
                    [this.attachment.id], data
                ],
            }, {
                shadow: true
            }).then(() => {
                this.attachment.update(data);
            });

        } else {

            this.attachment.remove();
            this.trigger('o-attachment-removed', {
                attachmentLocalId: this.props.attachmentLocalId
            });
        }

        this._dialogRef.comp._close();
    }

});

Object.assign(AttachmentDeleteConfirmDialog, {
    template: 'estate.AttachmentDeleteConfirmDialog',
});

export {
    AttachmentDeleteConfirmDialog
};