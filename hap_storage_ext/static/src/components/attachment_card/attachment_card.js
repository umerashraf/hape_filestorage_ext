 /** @odoo-module **/

 import {
     AttachmentCard
 } from '@mail/components/attachment_card/attachment_card'

 Object.assign(AttachmentCard.prototype, {
         onClickDownload(ev) {
             ev.stopPropagation();

             this.attachmentCard.update({
                 hasEditConfirmDialog: false
             });

             window.location = `/web/content/ir.attachment/${this.attachment.id}/datas?download=true`;
         },
         onClickUnlink(ev) {
            //console.log(this.attachmentCard.hasEditConfirmDialog);
            ev.stopPropagation(); // prevents from opening viewer
             this.attachmentCard.update({
                 hasEditConfirmDialog: false,
                 hasDeleteConfirmDialog: true
             });
             //console.log(this.attachmentCard.hasEditConfirmDialog);
             if (!this.attachment) {
                 return;
             }
             if (this.attachmentList.composerView) {
                 this.component.trigger('o-attachment-removed', {
                     attachmentLocalId: this.attachment.localId
                 });
                 this.attachment.remove();
             } else {
                 this.attachmentCard.update({
                     hasDeleteConfirmDialog: true
                 });
             }
         },
         onClickEdit(ev) {
            console.log(this.attachmentCard.hasEditConfirmDialog)
             ev.stopPropagation();
             this.attachmentCard.update({
                 hasEditConfirmDialog: true
             });
             this.attachmentCard.update({
                 hasDeleteConfirmDialog: true
             });
         },
     }

 );

 Object.assign(AttachmentCard, {
     template: 'estate.AttachmentCard',
 });
 export {
     AttachmentCard
 };