odoo.define('bb_products_web.WebsiteSales', function (require) {
    'use strict';
    var utils = require('web.utils');
    var ProductConfiguratorMixin = require('sale.ProductConfiguratorMixin');
    var core = require('web.core');
    var config = require('web.config');
    var sAnimations = require('website.content.snippets.animation');
    var ajax = require('web.ajax');

    require("website.content.zoomodoo");

    var _t = core._t;
    sAnimations.registry.WebsiteSale.include({

        onChangeVariant: function (ev) {
            var self = this;
            var $component;
            if ($(ev.currentTarget).closest('form').length > 0){
                $component = $(ev.currentTarget).closest('form');
            } else if ($(ev.currentTarget).closest('.oe_optional_products_modal').length > 0){
                $component = $(ev.currentTarget).closest('.oe_optional_products_modal');
            } else if ($(ev.currentTarget).closest('.o_product_configurator').length > 0) {
                $component = $(ev.currentTarget).closest('.o_product_configurator');
            } else {
                $component = $(ev.currentTarget);
            }
            var qty = $component.find('input[name="add_qty"]').val();

            var $parent = $(ev.target).closest('.js_product');
            var combination = this.getSelectedVariantValues($parent);

            self._checkExclusions($parent, combination);

            ajax.jsonRpc(this._getUri('/product_configurator/get_combination_info'), 'call', {
                product_template_id: parseInt($parent.find('.product_template_id').val()),
                product_id: this._getProductId($parent),
                combination: combination,
                add_qty: parseInt(qty),
                pricelist_id: this.pricelistId || false,
            }).then(function (combinationData) {
                console.log(combinationData);
                self._onChangeCombination(ev, $parent, combinationData);
                $component.find('input[name="add_qty"]').val(combinationData['quantity']);
                $("#roundOff").val(combinationData['roundOff']);
                $("#roundOffMsg").html('Minimum Quantity and multiples of the same this product can be ordered in: '+ combinationData['roundOff'])
             });
        },

        onClickAddCartJSON: function (ev){
            ev.preventDefault();
            var $link = $(ev.currentTarget);

            var roundOff = $link.parents('td').last().children().first().val();
            if(roundOff == undefined || roundOff.length == 0)
                roundOff = $('#roundOff').val();

            if(roundOff == undefined || roundOff.length == 0)
                roundOff = "100"
            roundOff = parseInt(roundOff);
            var $input = $link.closest('.input-group').find("input");

            var min = parseFloat($input.data("min") || 0);
            var max = parseFloat($input.data("max") || Infinity);
            var quantity = ($link.has(".fa-minus").length ? -roundOff : roundOff) + parseFloat($input.val() || 0, 10);
            var newQty = (quantity > min ? (quantity < max ? quantity : max) : min);

            $input.val(newQty).trigger('change');
            return false;
        },
        /*_onClickAddCartJSON: function (ev){
            ev.preventDefault();
            var $link = $(ev.currentTarget);
            var $input = $link.closest('.input-group').find("input");
            var min = parseFloat($input.data("min") || 0);
            var max = parseFloat($input.data("max") || Infinity);
            var quantity = ($link.has(".fa-minus").length ? -100 : 100) + parseFloat($input.val() || 0, 10);
            var newQty = Math.ceil( (quantity > min ? (quantity < max ? quantity : max) : min) /100) * 100;

            $input.val(newQty).trigger('change');
            return false;
        },*/
    });
});