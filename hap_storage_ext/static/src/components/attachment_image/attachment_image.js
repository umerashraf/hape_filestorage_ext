 /** @odoo-module **/

 import {
     AttachmentImage
 } from '@mail/components/attachment_image/attachment_image'

 Object.assign(AttachmentImage.prototype, {
         onClickUnlink(ev) {
            ev.stopPropagation(); // prevents from opening viewer
             this.attachmentImage.update({
                 hasEditConfirmDialog: false
             });
             
             if (!this.attachment) {
                 return;
             }
             if (this.attachmentList.composerView) {
                 this.component.trigger('o-attachment-removed', {
                     attachmentLocalId: this.attachment.localId
                 });
                 this.attachment.remove();
             } else {
                 this.attachmentImage.update({
                     hasDeleteConfirmDialog: true
                 });
             }
         },
         onClickEdit(ev) {
             ev.stopPropagation();
             this.attachmentImage.update({
                 hasEditConfirmDialog: true
             });
             this.attachmentImage.update({
                 hasDeleteConfirmDialog: true
             });
         },
     }
 );

 Object.assign(AttachmentImage, {
     template: 'estate.AttachmentImage',
 });
 export {
     AttachmentImage
 };