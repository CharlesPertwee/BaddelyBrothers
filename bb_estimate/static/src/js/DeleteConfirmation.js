odoo.define('bb_estimate.delete_confirmation', function(require) {
"use strict";

// var editable_ListRenderer = require('web.EditableListRenderer');
var ListRenderer = require('web.ListRenderer');

ListRenderer.include({
    events: _.extend({}, ListRenderer.prototype.events, {
      'click button.fa-trash-o': '_onTrashClick',  
    }),
    
    _onTrashClick: function (event) {
        event.stopPropagation();
        var result = confirm("Are you sure you want to delete this record?");
        if (result)
        {
            var id = $(event.target).closest('tr').data('id');
            $(event.target).closest('tr').hide()
            this.trigger_up('list_record_remove', {id: id});
        }
    }
});

});