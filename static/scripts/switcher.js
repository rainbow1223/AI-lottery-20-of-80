"use strict";

window.SaleViewer = window.SaleViewer || {};

SaleViewer.Switcher = function (customParams) {
    customParams = customParams || {};
    var self = this,
        DAY_TYPE = "day",
        containerSelector = customParams.container || "#switcher",
        switcherContainer = $(containerSelector),
        type = customParams.type || DAY_TYPE,
        date = customParams.date || new Date(),
        format = type === DAY_TYPE ? { date: "medium" } : { raw: "MMMM" },
        disabledClass = "disabled",
        onChange = customParams.onChange || function (date) {

        };

    var nextContainer = $('<span class="switcher-next"><span>'),
        prevContainer = $('<span class="switcher-prev"><span>'),
        dateContainer = $('<span class="date"><span>');

    var currentDate = new Date(),
        endDate = new Date(date.getFullYear() - 2, 0, 1);
    prevContainer.appendTo(switcherContainer);
    dateContainer.appendTo(switcherContainer);
    nextContainer.appendTo(switcherContainer);

    var updateDate = function (offset) {
        var newDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
        if (type === DAY_TYPE) {
            currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate());
            newDate.setDate(newDate.getDate() + offset);
        } else {
            currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
            newDate.setDate(1);
            newDate.setMonth(newDate.getMonth() + offset);
        }
        nextContainer.removeClass(disabledClass);
        prevContainer.removeClass(disabledClass);
        if (newDate >= currentDate) {
            nextContainer.addClass(disabledClass);
            if (newDate > currentDate) {
                return;
            }
        }
        if (newDate <= endDate) {
            prevContainer.addClass(disabledClass);
            if (newDate < endDate) {
                return;
            }
        } 


        date = newDate;
        dateContainer.html(Globalize.formatDate(date, format).toUpperCase());
        onChange(date);
    };

    nextContainer.click(function () {
        updateDate(1);
    });

    prevContainer.click(function () {
        updateDate(-1);
    });

    updateDate(0);

    self.reverse = function() {
        currentDate.setDate(date.getDate() - 1);
        updateDate(-1);
    };

    self.getDate = function () {
        return date;
    };
};