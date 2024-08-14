/** @odoo-module **/

import {human_size, patch} from "web.utils";
import {_t} from "web.core";
import Dialog from "web.Dialog"; // eslint-disable-line sort-imports
import {FileUploader} from "@mail/components/file_uploader/file_uploader";
import session from "web.session";

const components = {FileUploader};

patch(
    components.FileUploader.prototype,
    "hap_storage_ext/static/src/components/file_uploader/file_uploader.esm.js",
    {
        setup(...args) {
            this._super(...args);
            this.max_attachment_size = session.max_attachment_size || 10 * 1024 * 1024;
        },

        /**
         * @inherit
         * */
        // eslint-disable-next-line no-unused-vars
        async _performUpload({composer, files, thread}) {
            var larger_files = [];
            for (const file of files) {
                if (file.size > this.max_attachment_size) {
                    larger_files.push(file);
                }
            }
            // Raise the validation error.
            if (larger_files.length !== 0) {
                Dialog.alert(
                    this,
                    _.str.sprintf(
                        _t("The selected file exceeds the maximum file size of %s"),
                        human_size(this.max_attachment_size)
                    ),
                    {title: _t("Validation Error")}
                );
                return false;
            }
            return this._super(...arguments);
        },
    }
);
