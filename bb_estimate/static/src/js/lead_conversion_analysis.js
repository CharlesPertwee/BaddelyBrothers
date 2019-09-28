odoo.define('bb_estimate.lead_conversion_analysis',function(require){
	'use strict' ;
	    
	var core = require('web.core');
	var framework = require('web.framework');
	var stock_report_generic = require('stock.stock_report_generic');

	var QWeb = core.qweb;
	var _t = core._t;
	    
	var CrmConversionAnalysis = stock_report_generic.extend({
		events: {
			'click .o_crm_analysis_unfoldable': '_onClickUnfold',
	        'click .o_crm_analysis_foldable': '_onClickFold',
	        'click .o_crm_analysis_action': '_onClickAction',
	        'click .o_crm_analysis_attachment_action': '_onClickShowAttachment',
		},

		get_html: function() {
	        var self = this;
            console.log("THIS IS SPARTAN")
	        var args = [
	            this.given_context.active_id,
	        ];
	        return this._rpc({
	                model: 'report.crm.conversion_analysis',
	                method: 'get_html',
	                args: args,
	                context: this.given_context,
	            })
	            .then(function (result) {
	                self.data = result;
	            });
	    },

	    set_html: function() {
	        var self = this;
	        return this._super().then(function () {
	            self.$el.html(self.data.lines);
	        });
	    },
        
        render_html: function(event, $el, result){
            $el.after(result);
            $(event.currentTarget).toggleClass('o_crm_analysis_foldable o_crm_analysis_unfoldable fa-caret-right fa-caret-down');
        },
        
        
        _get_leads_year: function(event) {
	        var self = this;
            console.log("THIS IS SPARTAN 1")
            var $parent = $(event.currentTarget).closest('tr');
            var level = $parent.data('level') || 0;
            var trId = $(this).closest('tr').eq(0).prop('id');
	        var args = [
	            this.given_context.active_id,
                $parent.prop('id')
	        ];
	        return this._rpc({
	                model: 'report.crm.conversion_analysis',
	                method: 'get_leads_year',
	                args: args,
	                context: this.given_context,
	            })
	            .then(function (result) {
	                self.data = result;
                    self.render_html(event, $parent, result);
	            });
	    },
        
        get_lead_type: function(event) {
	        var self = this;
            console.log("THIS IS SPARTAN 2")
            var $parent = $(event.currentTarget).closest('tr');
            var level = $parent.data('level') || 0;
	        var args = [
	            this.given_context.active_id,
                $parent.prop('id')
	        ];
	        return this._rpc({
	                model: 'report.crm.conversion_analysis',
	                method: 'get_lead_type',
	                args: args,
	                context: this.given_context,
	            })
	            .then(function (result) {
	                self.data = result;
                    self.render_html(event, $parent, result);
	            });
	    },
        
        _onClickUnfold: function (ev) {
            var redirect_function = $(ev.currentTarget).data('function');
            this[redirect_function](ev);
        },
        _onClickFold: function (ev) {
            console.log("I AM IN FOLD")
            this._removeLines($(ev.currentTarget).closest('tr'));
            $(ev.currentTarget).toggleClass('o_crm_analysis_foldable o_crm_analysis_unfoldable fa-caret-right fa-caret-down');
        },
        _onClickAction: function (ev) {
            ev.preventDefault();
            return this.do_action({
                type: 'ir.actions.act_window',
                res_model: $(ev.currentTarget).data('model'),
                res_id: $(ev.currentTarget).data('res-id'),
                views: [[false, 'form']],
                target: 'current'
            });
        },
        _removeLines: function ($el) {
        var self = this;
        var activeID = $el.data('id');
        _.each(this.$('tr[parent_id='+ activeID +']'), function (parent) {
            var $parent = self.$(parent);
            var $el = self.$('tr[parent_id='+ $parent.data('id') +']');
            if ($el.length) {
                self._removeLines($parent);
            }
            $parent.remove();
        });
    },
	});
    
    
    core.action_registry.add('lead_conversion_analysis', CrmConversionAnalysis);
    return CrmConversionAnalysis;
});