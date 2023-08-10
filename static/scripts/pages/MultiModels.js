"use strict";

function load_training(grid, URL) {
	grid.option("dataSource", { store: []});
	grid.beginCustomLoading();
	$.ajax({
		url: URL,
		error: function (result) {
			grid.endCustomLoading();
			alert("There is a Problem, Try Again!");			
		},
		success: function (result) {
			result = JSON.parse(result)
			grid.option("dataSource", { store: result});
			grid.endCustomLoading();
		}
	});
};

var result_new_numbers, result_new_numbers_with_prob;
var date_selected, predicted_numbers, predicted_numbers_with_prob, origin_numbers, anaylsis_one_date, pred_num;
var end_date_in_dateset;
var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
var grid1;

function clear_prediction(){
	result_new_numbers.option("value", "");
	result_new_numbers_with_prob.option("value", "");
	predicted_numbers.option("value", "");
	origin_numbers.option("value", "");
	anaylsis_one_date.option("value", "");
	
	date_selected.option("min", null);
	date_selected.option("max", null);
};

function convert_date(date_str){
	var temp = date_str.split(', ');
	var temp1 = temp[0].split(' ');
	var year = parseInt(temp[1]);
	var month = months.indexOf(temp1[0]);
	var date = parseInt(temp1[1]);
	return new Date(year, month, date);
};

function convert_date_string(date){
	var dd = date.getDate();
	if (dd > 9){
		return months[date.getMonth()] + ' ' + date.getDate() + ', ' + date.getFullYear();
	}
	return months[date.getMonth()] + ' 0' + date.getDate() + ', ' + date.getFullYear();
};

$(function () {
	//////////////////////////////////////////////////////////////
	/////////////////////   Trained models   /////////////////////
	//////////////////////////////////////////////////////////////
	var gridOptions1 = {
			keyExpr: "model",
			editing: {
				mode: "row",
				allowAdding: false,
				allowUpdating: false,
				allowDeleting: false,
				useIcons: true
			},
            dataSource: {
                store: new Array()
            },
            paging: {
                pageSize: 10,
            },
			filterRow: {
				visible: true,
			},
			selection: {
				mode: 'multiple',
			},
			groupPanel: {
				visible: true,
			},
			grouping: {
				autoExpandAll: true,
			},
			summary: {
				groupItems: [{
					column: 'model',
					summaryType: 'count',
				}],
			},
            columns: [
                {
                    dataField: "type",
                    groupIndex: 0,
                },
                {
                    dataField: "model",
                    alignment: "left",
                },
                {
                    dataField: "neurons",
                    caption: "Params",
                    alignment: "center",
                },
                {
                    dataField: "end_date_in_dateset",
                    alignment: "center",
                },
 			],
			showBorders: true,
			columnAutoWidth:false,
            showColumnLines: true,
            showRowLines: false,
			hoverStateEnabled: true,
			width:1000,
        };
	var gridContainer1 = $("#trained_grid");
	gridContainer1.dxDataGrid(gridOptions1);
	grid1 = gridContainer1.data("dxDataGrid");
	load_training(grid1, '/MultiModels/trained');

	//////////////////////////////////////////////////////////////
	///////////////////////   Test model   ///////////////////////
	//////////////////////////////////////////////////////////////
	result_new_numbers = $("#result_new_numbers").dxTextArea({
        placeholder: "New Numbers",
        width: 320,
		height: 220,
		readOnly: true,
    }).dxTextArea("instance");
    result_new_numbers_with_prob = $("#result_new_numbers_with_prob").dxTextArea({
        placeholder: "New Numbers with Probability",
        width: 320,
		height: 220,
		readOnly: true,
    }).dxTextArea("instance");
    $("#pred_last_day").dxButton({
        stylingMode: "contained",
        text: "Predict the New Numbers",
        type: "success",
        onClick: function() {
			var selected_models = grid1.getSelectedRowKeys()
			if (selected_models.length == 0){
				alert('Please choose the model(s) from Trained models.');
				return;
			}
			if (selected_models.length > 10){
				alert('Please choose the 10 models at the most!');
				return;
			}
			result_new_numbers.option("value", "");
			result_new_numbers_with_prob.option("value", "");
			var model_names = selected_models[0].type + '_' + selected_models[0].model;
			for(var i=1;i<selected_models.length;i++) model_names += "/" + selected_models[i].type + '_' + selected_models[i].model;
			$.ajax({
				url: '/MultiModels/predict/new',
				data: {"model": model_names},
				error: function (result) {
					alert("There is a Problem, Try Again!");			
				},
				success: function (result) {
					result = JSON.parse(result);
					result_new_numbers.option("value", result.numbers_str);
					result_new_numbers_with_prob.option("value", result.numbers_str_prob);
					end_date_in_dateset = result['last_day'];
					document.getElementById("last_day1").textContent = "(End date in dataset is " + end_date_in_dateset + ")";
				}
			});
        }
    });

    date_selected = $("#date_selected").dxCalendar({
        value: new Date(),
        disabled: false,
        firstDayOfWeek: 0,
        zoomLevel: "month",
		height: 270,
    }).dxCalendar("instance");
    pred_num = $("#pred_num").dxTextBox({
        value: "30",
        width: 50,
    }).dxTextBox("instance");
    $("#pred_date_selected").dxButton({
        stylingMode: "contained",
        text: "Predict for the Given Date",
        type: "success",
        onClick: function() {
			var selected_models = grid1.getSelectedRowKeys()
			if (selected_models.length == 0){
				alert('Please choose the model(s) from Trained models.');
				return;
			}
			if (selected_models.length > 10){
				alert('Please choose the 10 models at the most!');
				return;
			}
			predicted_numbers.option("value", "");
			origin_numbers.option("value", "");
			anaylsis_one_date.option("value", "");
			var model_names = selected_models[0].type + '_' + selected_models[0].model;
			for(var i=1;i<selected_models.length;i++) model_names += "/" + selected_models[i].type + '_' + selected_models[i].model;
			$.ajax({
				url: '/MultiModels/predict/past_date',
				data: {"model": model_names, "date": convert_date_string(date_selected.option("value"))},
				error: function (result) {
					alert("There is a Problem, Try Again!");			
				},
				success: function (result) {
					result = JSON.parse(result);
					predicted_numbers.option("value", result.predicted_numbers);
					origin_numbers.option("value", result.origin_numbers);
					anaylsis_one_date.option("value", result.anaylsis_one_date);
				}
			});
        }
    });
	predicted_numbers = $("#predicted_numbers").dxTextArea({
        placeholder: "predicted_numbers",
        width: 220,
		height: 270,
		readOnly: true,
    }).dxTextArea("instance");
    origin_numbers = $("#origin_numbers").dxTextArea({
        placeholder: "original numbers (20)",
        width: 220,
		height: 270,
		readOnly: true,
    }).dxTextArea("instance");
    anaylsis_one_date = $("#anaylsis_one_date").dxTextArea({
        placeholder: "Analysis result",
        width: 220,
		height: 270,
		readOnly: true,
    }).dxTextArea("instance");

	$.ajax({
		url: '/FFNN/train/last_day',
		error: function (result) {
			alert("There is a Problem, Try Again!");			
		},
		success: function (result) {
			result = JSON.parse(result);
			end_date_in_dateset = result['last_day'];
			document.getElementById("last_day").textContent = "(End date in dataset is " + end_date_in_dateset + ")";
			date_selected.option("max", convert_date(end_date_in_dateset));
			date_selected.option("value", convert_date(end_date_in_dateset));
		}
	});

	clear_prediction();
});
