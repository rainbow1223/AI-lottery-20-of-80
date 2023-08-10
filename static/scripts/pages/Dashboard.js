"use strict";

$(function () {
	$.ajax({
		url: '/bk/Dashboard/statistics',
		error: function (result) {
			alert("There is a Problem, Try Again!");			
		},
		success: function (result) {
			result = JSON.parse(result)
			document.getElementById("ffnn_num").textContent = result["ffnn_num_trained"] + '+' + result["ffnn_num_training"];
			document.getElementById("cnn_num").textContent = result["cnn_num_trained"] + '+' + result["cnn_num_training"];
			document.getElementById("rnn_num").textContent = result["rnn_num_trained"] + '+' + result["rnn_num_training"];
		}
	});
});
