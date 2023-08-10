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

function clear_prediction(){
	document.getElementById("test_current_model").textContent = "The model is not chosen yet.";
	result_new_numbers.option("value", "");
	result_new_numbers_with_prob.option("value", "");
	predicted_numbers.option("value", "");
	predicted_numbers_with_prob.option("value", "");
	origin_numbers.option("value", "");
	anaylsis_one_date.option("value", "");
	pred_num.option("value", "30");
	
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
	///////////////   Models to be being trained   ///////////////
	//////////////////////////////////////////////////////////////
	var gridOptions = {
			keyExpr: "model",
			editing: {
				allowAdding: false,
				allowUpdating: false,
				allowDeleting: false,
			},
            dataSource: {
                store: new Array()
            },
            paging: {
                enabled:false
            },
            selection: {
                enabled: false
            },
			summary: {
				totalItems: [{
					column: "model",
					summaryType: "count",
				}]
			},
            columns: [
                {
                    dataField: "model",
                    alignment: "center",
                },
                {
                    dataField: "neurons",
                    caption: "Params",
                    alignment: "center",
                },
                {
                    dataField: "epochs",
                    alignment: "center",
                },
                {
                    dataField: "batch_size",
                    alignment: "center",
                },
                {
                    dataField: "validation_split",
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
			width:900,
        };
	var gridContainer = $("#training_grid");
	gridContainer.dxDataGrid(gridOptions);
	var grid = gridContainer.data("dxDataGrid");
	load_training(grid, '/CNN/training');

	//////////////////////////////////////////////////////////////
	////////////////////   Train New model   /////////////////////
	//////////////////////////////////////////////////////////////
    $("#help").dxButton({
        stylingMode: "outlined",
        text: "help",
        type: "success",
        onClick: function() {
			var result = "\nThe parameters should be typed as following:\n";
			result += "    [params], [epochs], [batch_size], [validation_split]\nHere\n"
			result += "    'params' consists of 6 integers splitted by ';'.\n"
			result += "              the first integer could be an integer between 16 and 32 and\n"
			result += "              the next 3 integers should be an integer such as 8, 16, 32, 64 and\n"
			result += "              the 5-th integer should be a an integer such as 64, 128, 256, 512 and\n"
			result += "              the last integer should be a 20.\n"
			result += "              ex: 20;8;16;16;128;20, 20;16;32;64;256;20, etc.\n"
			result += "    'epochs' is epochs to train the model (order of 3 in general).\n"
			result += "    'batch_size' is the size of batch to train the model.\n              (16, 32, 64, etc)\n"
			result += "    'validation_split' is ratio of the validation dataset.\n             (smaller than 0.2)\n"
			alert(result);
        }
    });

    $("#load_default_values").dxButton({
        stylingMode: "contained",
        text: "Load default parameters",
        type: "default",
        onClick: function() {
			parameters.option("value", "20;8;16;16;128;20, 200, 64, 0.1")
        }
    });
	
    $("#training").dxButton({
        stylingMode: "contained",
        text: "Train new model",
        type: "success",
        onClick: function() {
			if (parameters.option("value") == ''){
				alert('Model parameters are empty. Please click "help" for details.');
				return;
			}
			$.ajax({
				url: '/CNN/train/new',
				data: {'param_str': parameters.option("value")},
				type: 'POST',
				error: function (result) {
					alert("There is a Problem, Try Again!");			
				},
				success: function (result) {
					result = JSON.parse(result);
					if (result.status == 'ERROR'){
						alert(result.message);
					}
					else {
						alert('Started to train the new model!');
						end_date_in_dateset = result['message'];
						document.getElementById("last_day").textContent = "(End date in dataset is " + end_date_in_dateset + ")";
						parameters.option("value", "");
						load_training(grid, '/CNN/training');
					}
				}
			});
        }
    });
	
    var parameters = $("#parameters").dxTextBox({
        placeholder: "Ex: 20;8;16;16;128;20, 200, 64, 0.1",
        width: 220,
    }).dxTextBox("instance");

	$.ajax({
		url: '/FFNN/train/last_day',
		error: function (result) {
			alert("There is a Problem, Try Again!");			
		},
		success: function (result) {
			result = JSON.parse(result);
			end_date_in_dateset = result['last_day'];
			document.getElementById("last_day").textContent = "(End date in dataset is " + end_date_in_dateset + ")";
		}
	});
	
	//////////////////////////////////////////////////////////////
	///////////////////////   Test model   ///////////////////////
	//////////////////////////////////////////////////////////////
	result_new_numbers = $("#result_new_numbers").dxTextArea({
        placeholder: "40 New Numbers",
        width: 320,
		height: 220,
		readOnly: true,
    }).dxTextArea("instance");
    result_new_numbers_with_prob = $("#result_new_numbers_with_prob").dxTextArea({
        placeholder: "40 New Numbers with Probability",
        width: 320,
		height: 220,
		readOnly: true,
    }).dxTextArea("instance");
    $("#pred_last_day").dxButton({
        stylingMode: "contained",
        text: "Predict the New Numbers",
        type: "success",
        onClick: function() {
			if (document.getElementById("test_current_model").textContent == "The model is not chosen yet."){
				alert('Please choose the model from Trained models.');
				return;
			}
			result_new_numbers.option("value", "");
			result_new_numbers_with_prob.option("value", "");
			$.ajax({
				url: '/CNN/predict/new',
				data: {"model": document.getElementById("test_current_model").textContent.split(': ')[1]},
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
			if (document.getElementById("test_current_model").textContent == "The model is not chosen yet."){
				alert('Please choose the model from Trained models.');
				return;
			}
			var pred_num_val = parseInt(pred_num.option("value"));
			if (pred_num_val < 20 || pred_num_val > 40){
				alert("The predicted numbers should be set an integer from 20 to 40!\n(current value is " + pred_num_val.toString() + ")");
				return
			}
			predicted_numbers.option("value", "");
			predicted_numbers_with_prob.option("value", "");
			origin_numbers.option("value", "");
			anaylsis_one_date.option("value", "");
			$.ajax({
				url: '/CNN/predict/past_date',
				data: {"model": document.getElementById("test_current_model").textContent.split(': ')[1], "date": convert_date_string(date_selected.option("value")), "pred_num": pred_num_val.toString()},
				error: function (result) {
					alert("There is a Problem, Try Again!");			
				},
				success: function (result) {
					result = JSON.parse(result);
					predicted_numbers.option("value", result.predicted_numbers);
					predicted_numbers_with_prob.option("value", result.predicted_numbers_with_prob);
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
	predicted_numbers_with_prob = $("#predicted_numbers_with_prob").dxTextArea({
        placeholder: "predicted_numbers_with_prob",
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

	clear_prediction();
	
	//////////////////////////////////////////////////////////////
	/////////////////////   Trained models   /////////////////////
	//////////////////////////////////////////////////////////////
	var gridOptions1 = {
			keyExpr: "model",
			editing: {
				mode: "row",
				allowAdding: false,
				allowUpdating: false,
				allowDeleting: true,
				useIcons: true
			},
            dataSource: {
                store: new Array()
            },
            paging: {
                enabled:false
            },
            selection: {
                enabled: false
            },
			summary: {
				totalItems: [{
					column: "model",
					summaryType: "count",
				}]
			},
            columns: [
                {
                    dataField: "model",
                    alignment: "center",
                },
                {
                    dataField: "neurons",
                    caption: "Params",
                    alignment: "center",
                },
                {
                    dataField: "epochs",
                    alignment: "center",
                },
                {
                    dataField: "batch_size",
                    alignment: "center",
                },
                {
                    dataField: "validation_split",
                    alignment: "center",
                },
                {
                    dataField: "end_date_in_dateset",
                    alignment: "center",
                },
                {
					type: "buttons",
					width: 100, 
					buttons: ["delete",
					{
						hint: "Test",
						icon: "check",
						visible: true,
						onClick: function(e) {
							clear_prediction();
							document.getElementById("test_current_model").textContent = 'Chosen Model: ' + e.row.data.model;							
							date_selected.option("min", convert_date(e.row.data.end_date_in_dateset));
							date_selected.option("max", convert_date(end_date_in_dateset));
							date_selected.option("value", convert_date(end_date_in_dateset));
						},
					},
					{
						hint: "Retrain",
						icon: "fa fa-spinner",
						visible: true,
						onClick: function(e) {
							parameters.option("value", e.row.data.model.split('-')[1] + ", 200, 64, 0.1")
							$.ajax({
								url: "/CNN/trained",
								type: "DELETE",
								data: {"id": e.row.data.model},
								error: function (result) {
									alert("There is a Problem, Try Again!");
								},
								success: function (result) {
									if (document.getElementById("test_current_model").textContent.split(': ')[1] == e.row.data.model){
										clear_prediction();
									}
									load_training(grid1, '/CNN/trained');
								}
							});
						},
					},
					]
				},
 			],
			showBorders: true,
			columnAutoWidth:false,
            showColumnLines: true,
            showRowLines: false,
			hoverStateEnabled: true,
			width:1000,
			onRowRemoving: function(e) {
				$.ajax({
                    url: "/CNN/trained",
					type: "DELETE",
					data: {"id": e.data.model},
					error: function (result) {
						alert("There is a Problem, Try Again!");
						e.cancel = true;
					},
					success: function (result) {
						if (document.getElementById("test_current_model").textContent.split(': ')[1] == e.data.model){
							clear_prediction();
						}
					}
				});
			},
        };
	var gridContainer1 = $("#trained_grid");
	gridContainer1.dxDataGrid(gridOptions1);
	var grid1 = gridContainer1.data("dxDataGrid");
	load_training(grid1, '/CNN/trained');
});
