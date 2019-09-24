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
                    console.log("Damn")
                    console.log(result)
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
            this._reload_report_type();
        },
        
        
        get_leads: function(event) {
	        var self = this;
            console.log("THIS IS SPARTAN 1")
            var $parent = $(event.currentTarget).closest('tr');
            var level = $parent.data('level') || 0;
	        var args = [
	            this.given_context.active_id,
	        ];
	        return this._rpc({
	                model: 'report.crm.conversion_analysis',
	                method: 'get_leads',
	                args: args,
	                context: this.given_context,
	            })
	            .then(function (result) {
	                self.data = result;
	            });
	    },
        
        _onClickUnfold: function (ev) {
            var redirect_function = $(ev.currentTarget).data('function');
            this[redirect_function](ev);
        },
        _onClickFold: function (ev) {
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
	});
    
    
    core.action_registry.add('lead_conversion_analysis', CrmConversionAnalysis);
    return CrmConversionAnalysis;
});