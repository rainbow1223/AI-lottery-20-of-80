"use strict";

window.SaleViewer = window.SaleViewer || {};

SaleViewer.Legend = function (fields) {
    var legendFields = fields,
        palette = DevExpress.viz.getPalette("SaleViewPalette").simpleSet;

    this.draw = function () {
        $.each(legendFields, function(index, field) {
            var item = $("<div/>", { "class": "legend-item" });
            $("<div/>", { "class": "color" }).css({ backgroundColor: palette[index] }).appendTo(item);
            $("<div/>", { text: field }).addClass("field").appendTo(item);
            item.appendTo("#legend");
        });
    };

    this.getColorByField = function(fieldName) {
        var color = null;
        $.each(legendFields, function(index, field) {
            if(fieldName == field) {
                color = palette[index];
                return false;
            }
        });
        return color;
    };

    this.getShortFieldName = function(fieldName) {
        switch(fieldName) {
            case "Manufacturing":
                return "Manuf.";
            case "Eco Supreme":
                return "Eco Supr.";
            case "EnviroCare Max":
                return "Enviro Max";
        }
        return fieldName;
    };
};