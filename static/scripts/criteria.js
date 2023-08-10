"use strict";

window.SaleViewer = window.SaleViewer || {};

SaleViewer.Criteria = function(criteria) {
    var self = this,
        fields = (criteria == "sectors") ?
            ["Banking", "Energy", "Health", "Insurance", "Manufacturing", "Telecom"] :
            ["Eco Max", "Eco Supreme", "EnviroCare", "EnviroCare Max", "SolarMax", "SolarOne"];
    SaleViewer.legend = new SaleViewer.Legend(fields);
    var category = criteria,
        maxSalesValue = 0,
        maxUnitsValue = 0,
        chartOptions = {
            onIncidentOccurred: null,
            palette: "SaleViewPalette",
            dataSource: [],
            commonSeriesSettings: {
                argumentField: "Criteria",
                type: "bar",
                hoverMode: "onlyPoint",
                selectionMode: "onlyPoint",
                minBarSize: 5
            },
            legend: {
                visible: false
            },
            argumentAxis: {
                label: {
                    customizeText: function() {
                        return SaleViewer.legend.getShortFieldName(this.value);
                    }
                }
            },
            customizePoint: function() {
                if(this.seriesName == "Today" || this.seriesName == "ThisMonth")
                    return {
                        color: SaleViewer.legend.getColorByField(this.argument),
                        hoverStyle: {
                            color: SaleViewer.legend.getColorByField(this.argument),
                            hatching: {
                                opacity: 0
                            }
                        }
                    };
            },
            tooltip: {
                enabled: true,
                font: {
                    opacity: 1,
                    size: 22
                },
                paddingTopBottom: 8,
                customizeTooltip: function() {
                    var value = isCurrencyBySeriesName(this.seriesName)
                        ? Globalize.formatCurrency(this.originalValue, "USD", { maximumFractionDigits: 0 })
                        : Globalize.formatNumber(this.originalValue, { maximumFractionDigits: 0 });

                    return {
                        text: "<span style='font-size: 14px; color: " + SaleViewer.lightColor + ";'>" + this.argumentText.toUpperCase() + "</span><br />"
                            + "<span style='color: " + SaleViewer.legend.getColorByField(this.argumentText) + ";'>" + value + "</span><br />"
                            + "<span style='font-size: 14px; color: " + SaleViewer.lightColor + ";'>" + getDateName(this.seriesName) + "</span>"
                    };
                },
                shadow: {
                    opacity: 0.15,
                    blur: 0,
                    color: "#000000",
                    offsetX: 3,
                    offsetY: 3
                }
            }
        },

        salesOptions = {
            series: [
                {
                    valueField: "YesterdaySales",
                    name: "Yesterday",
                    color: "rgba(175, 175, 175, 0.45)",
                    hoverStyle: {
                        color: "rgba(175, 175, 175, 0.45)",
                        hatching: {
                            opacity: 0
                        }
                    }
                },
                {
                    valueField: "TodaySales",
                    name: "Today"
                }
            ],
            valueAxis: {
                axisDivisionFactor: 40,
                placeholderSize: 45,
                label: {
                    format: "currency thousands",
                    customizeText: function() {
                        if(this.value != maxSalesValue) {
                            return this.valueText;
                        }
                        return "";
                    }
                }
            }

        },

        unitsOptions = {
            series: [
                {
                    valueField: "LastMonthUnits",
                    name: "LastMonth",
                    color: "rgba(175, 175, 175, 0.45)",
                    hoverStyle: {
                        color: "rgba(175, 175, 175, 0.45)",
                        hatching: {
                            opacity: 0
                        }
                    }
                },
                {
                    valueField: "ThisMonthUnits",
                    name: "ThisMonth"
                }
            ],
            valueAxis: {
                axisDivisionFactor: 40,
                placeholderSize: 40,
                label: {
                    format: "thousands",
                    customizeText: function() {
                        if(this.value != maxUnitsValue) {
                            return this.valueText;
                        }
                        return "";
                    }
                }
            }
        },

        getDateName = function(seriesName) {
            var dayDate = daySwitcher.getDate(),
                monthDate = monthSwitcher.getDate();
            switch(seriesName) {
                case "Yesterday":
                    return SaleViewer.getCurrentDate().getDate() == dayDate.getDate() ?
                        seriesName :
                        Globalize.formatDate(new Date(dayDate.getFullYear(), dayDate.getMonth(), dayDate.getDate() - 1), { skeleton: "yMd" });
                case "Today":
                    return (SaleViewer.getCurrentDate().getDate() == dayDate.getDate()) ?
                        seriesName :
                        (SaleViewer.getCurrentDate().getDate() - 1 == dayDate.getDate()) ?
                        "Yesterday" :
                        Globalize.formatDate(dayDate, { raw: "MM/dd/yyyy" });
                case "LastMonth":
                    return Globalize.formatDate(new Date(monthDate.getFullYear(), monthDate.getMonth() - 1), { raw: "MMMM" });
                case "ThisMonth":
                    return Globalize.formatDate(monthDate, { raw: "MMMM" });
            }
        },
        
        isCurrencyBySeriesName = function(seriesName) {
            if(seriesName == "Today" || seriesName == "Yesterday") return true;
            return false;
        },

        salesChart = SaleViewer.sharedWidgets.initChart(category, $.extend({}, chartOptions, salesOptions), "chart", "sales"),
        unitsChart = SaleViewer.sharedWidgets.initChart(category, $.extend({}, chartOptions, unitsOptions), "chart", "units"),



        updateSales = function(date) {
            SaleViewer.loadData({
                twoDays: Globalize.formatDate(date, { raw: "yyyy-MM-dd" })
            }, function(data) {
                maxSalesValue = SaleViewer.sharedWidgets.getMaxAxisValue(data);
                salesChart.instance.option("valueAxis.max", maxSalesValue);
                salesChart.instance.option("dataSource", data);
            }, category);
        },
        updateUnits = function(date) {
            SaleViewer.loadData({
                twoMonths: Globalize.formatDate(date, { raw: "yyyy-MM-dd" })
            }, function(data) {
                maxUnitsValue = SaleViewer.sharedWidgets.getMaxAxisValue(data);
                unitsChart.instance.option("valueAxis.max", maxUnitsValue);
                unitsChart.instance.option("dataSource", data);
            }, category);
        },

        daySwitcher = new SaleViewer.Switcher({
            container: "#daySwitcher",
            type: "day",
            onChange: function(date) {
                updateSales(date);
            },
            date: SaleViewer.getCurrentDate()
        }),

        monthSwitcher = new SaleViewer.Switcher({
            container: "#monthSwitcher",
            type: "month",
            onChange: function(date) {
                updateUnits(date);
            },
            date: SaleViewer.getCurrentDate()
        });


    self.init = function() {
        SaleViewer.loadData({
            now: Globalize.formatDate(SaleViewer.getCurrentDate(), { raw: "yyyy-MM-dd HH:mm" })
        }, function (data) {
            $.each(data, function(index, value) {
                var object = $("#" + index);
                if((index.indexOf("Sales") == -1))
                    object.text(Globalize.formatNumber(value, { maximumFractionDigits: 0 }));
                else
                    object.text(Globalize.formatCurrency(value / 1000, "USD", { maximumFractionDigits: 0 }) + "K");
            });
        }, category);
    };
};

$(function () {
    SaleViewer.criteriaModel = new SaleViewer.Criteria(SaleViewer.criteria);
    SaleViewer.criteriaModel.init();
    SaleViewer.dashboard = new SaleViewer.Dashboard(SaleViewer.criteria);
    SaleViewer.dashboard.init();
});