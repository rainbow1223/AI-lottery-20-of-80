"use strict";

window.SaleViewer = window.SaleViewer || {};

SaleViewer.SharedWidgets = function () {
    var self = this;

    self.initGrid = function (options) {
        var gridContainer = $("#grid");
        gridContainer.dxDataGrid(options);
        var grid = gridContainer.data("dxDataGrid");
        var dataSource = options.dataSource;

        return {
            instance: grid,
            load: function (loadOptions, category, selectFirst) {
                grid.beginCustomLoading();
                SaleViewer.loadData(loadOptions, function (data) {
                    grid.option("dataSource", { store: JSON.parse(data)});
                    grid.endCustomLoading();
                    if (selectFirst === undefined || selectFirst) grid.selectRows(dataSource.store[0]);
                }, category);
            }
        };
    };

    self.initPopup = function () {
        $("#popup").dxPopup({
            visible: false,
            fullScreen: false,
            showTitle: false,
            showCloseButton: false,
            position: { offset:"0 -90px" },
            height: 'auto',
            width: 500
        });

        var popup = $("#popup").data("dxPopup");
                
        $("body").on("click", "#closePopupButton", function () {
            popup.option("visible", false);
        }); 

        $("body").on("click", "#downloadPopupButton", function () {
            window.open("https://js.devexpress.com/Download/", "_blank");
        });

        $("#openPopupButton").click(function () {
            popup.option("visible", true);
        });
        
    };

    self.getMaxAxisValue = function (data, dataField) {
        var maxSeries = [4000, 8000, 12000, 20000, 40000, 80000, 120000, 200000, 400000, 800000, 1200000, 2000000, 4000000, 8000000, 12000000, 20000000, 40000000, 80000000, 120000000, 200000000],
            max = 0,
            index = 0;
        $.each(data, function (_, object) {
            $.each(object, function (index, value) {
                if (dataField !== undefined && dataField != index) return;
                if ($.isNumeric(value) && value > max) max = value;
            });
        });
        $.each(maxSeries, function (i, value) {
            if (value >= max) {
                index = i;
                return false;
            }
        });
        return maxSeries[index];
    };
    
};