from flask import Flask, render_template, request, json, session, Response
from responses import error_400_message, error_401_message, error_403_message, success_200_message
import os, base64, random
from datetime import timedelta, datetime
import _thread

app = Flask(__name__)

weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

#####################   backend (Dashboard)   ####################
Models_trained_folder = 'Models_trained'
Models_training_folder = 'Models_training'
for folder1 in os.listdir(Models_training_folder):
	type_folder = os.path.join(Models_training_folder, folder1)
	for folder2 in os.listdir(type_folder):
		model_folder = os.path.join(type_folder, folder2)
		for file in os.listdir(model_folder):
			os.remove(os.path.join(model_folder, file))
		os.rmdir(model_folder)

@app.route('/bk/Dashboard/statistics', methods=['GET'])
def bk_Dashboard_statistics():
	FFNN_folder = os.path.join(Models_trained_folder, 'FFNN')
	if not os.path.isdir(FFNN_folder):
		os.makedirs(FFNN_folder)
		ffnn_num_trained = '0'
	else:
		ffnn_num_trained = str(len(os.listdir(FFNN_folder)))
	CNN_folder = os.path.join(Models_trained_folder, 'CNN')
	if not os.path.isdir(CNN_folder):
		os.mkdir(CNN_folder)
		cnn_num_trained = '0'
	else:
		cnn_num_trained = str(len(os.listdir(CNN_folder)))
	RNN_folder = os.path.join(Models_trained_folder, 'RNN')
	if not os.path.isdir(RNN_folder):
		os.mkdir(RNN_folder)
		rnn_num_trained = '0'
	else:
		rnn_num_trained = str(len(os.listdir(RNN_folder)))
		
	FFNN_folder = os.path.join(Models_training_folder, 'FFNN')
	if not os.path.isdir(FFNN_folder):
		os.makedirs(FFNN_folder)
		ffnn_num_training = '0'
	else:
		ffnn_num_training = str(len(os.listdir(FFNN_folder)))
	CNN_folder = os.path.join(Models_training_folder, 'CNN')
	if not os.path.isdir(CNN_folder):
		os.mkdir(CNN_folder)
		cnn_num_training = '0'
	else:
		cnn_num_training = str(len(os.listdir(CNN_folder)))
	RNN_folder = os.path.join(Models_training_folder, 'RNN')
	if not os.path.isdir(RNN_folder):
		os.mkdir(RNN_folder)
		rnn_num_training = '0'
	else:
		rnn_num_training = str(len(os.listdir(RNN_folder)))
		
	if not os.path.isdir(Models_training_folder): os.makedirs(Models_training_folder)
	return json.dumps({'ffnn_num_trained': ffnn_num_trained, 'cnn_num_trained': cnn_num_trained, 'rnn_num_trained': rnn_num_trained, 'ffnn_num_training': ffnn_num_training, 'cnn_num_training': cnn_num_training, 'rnn_num_training': rnn_num_training})


############################   menu   ############################
usual_menu_items = ['Dashboard', 'FFNN', 'CNN', 'RNN', 'MultiModels']
usual_menu_texts = ['My Dashboard', 'FFNN Models', 'CNN Models', 'RNN Models', 'MultiModels Predict']
@app.route('/bk/Menu', methods=['GET'])
def get_menu_item():
	menu_items = usual_menu_items
	menu_texts = usual_menu_texts
	menu_dict = []
	for menu_item, menu_text in zip(menu_items, menu_texts):
		menu_dict.append({
			'id': menu_item,
			'text': menu_text,
			'link': "/" + menu_item
		})
	return json.dumps({'statusCode': 200, 'menu_items': menu_dict})


############################   web pages   ############################
@app.route('/')
def main_register():
	return render_template('Dashboard.html')

def load_page(param):
	if param in usual_menu_items: return render_template('{}.html'.format(param))
	return render_template('empty.html')

@app.route('/Dashboard')
def fr_Dashboard():
	return load_page('Dashboard')

@app.route('/FFNN')
def fr_FFNN():
	return load_page('FFNN')

@app.route('/CNN')
def fr_CNN():
	return load_page('CNN')

@app.route('/RNN')
def fr_RNN():
	return load_page('RNN')

@app.route('/MultiModels')
def fr_MultiModels():
	return load_page('MultiModels')


############################   FFNN model   ############################
thread_num = 3
threads = []
for i in range(thread_num):
	thread = _thread.allocate_lock()  # 分配锁对象
	threads.append(thread)

from download import dataset_loading
from Models.train import FFNN_train
@app.route('/FFNN/train/new', methods=['POST'])
def fr_FFNN_train_new():
	dataset_loading()
	
	param_str = request.form.get('param_str')
	try:
		neurons, epochs, batch_size, validation_split = param_str.split(',')
		epochs, batch_size, validation_split = int(epochs), int(batch_size), float(validation_split)
	except:
		return json.dumps(error_400_message('Model parameters are wrong. Please click to "help" for details.'))
	trainings, trained = get_trainings('FFNN'), get_trained('FFNN')
	for model in trainings:
		if neurons == model[1]: return json.dumps(error_400_message('The given model is being trained now!'))
	for model in trained:
		if neurons == model[1]: return json.dumps(error_400_message('The given model has been trained already!'))
	try:
		neurons = neurons.split(';')
		neurons = [int(neuron) for neuron in neurons]
	except:
		return json.dumps(error_400_message('[nuerons] are wrong. Please click to "help" for details.'))
	if neurons[0] % 20 > 0:	return json.dumps(error_400_message('[nuerons] are wrong. Please click to "help" for details.'))
	if neurons[-1] != 20: return json.dumps(error_400_message('[nuerons] are wrong. Please click to "help" for details.'))
	train_started = False
	for thread in threads:
		if not thread.locked():
			train_started = True
			thread.acquire()
			_thread.start_new(FFNN_train, ([neurons, epochs, batch_size, validation_split], param_str, thread))
			break
	if not train_started: return json.dumps(error_400_message('There could not be trained more than %d models to be being trained' % thread_num))
	return json.dumps(success_200_message(get_last_day()))

from Models.train import get_last_day
@app.route('/FFNN/train/last_day')
def fr_FFNN_train_last_day():
	return json.dumps({'last_day': get_last_day()})

def get_trainings(model_type):
	FFNN_folder = os.path.join(Models_training_folder, model_type)
	models = []
	for folder in os.listdir(FFNN_folder):
		model_folder = os.path.join(FFNN_folder, folder)
		with open(os.path.join(model_folder, 'param_str.txt'), 'r') as f:
			model_details = f.read()
		param_str, end_date = model_details.split('\n')
		neurons, epochs, batch_size, validation_split = param_str.split(',')
		models.append((folder, neurons, epochs, batch_size, validation_split, end_date))
	return models

def get_trained(model_type):
	FFNN_folder = os.path.join(Models_trained_folder, model_type)
	models = []
	for folder in os.listdir(FFNN_folder):
		model_folder = os.path.join(FFNN_folder, folder)
		with open(os.path.join(model_folder, 'param_str.txt'), 'r') as f:
			model_details = f.read()
		param_str, end_date = model_details.split('\n')
		neurons, epochs, batch_size, validation_split = param_str.split(',')
		models.append((folder, neurons, epochs, batch_size, validation_split, end_date))
	return models

@app.route('/FFNN/training')
def fr_FFNN_training():
	models = []
	for model_data in get_trainings('FFNN'):
		model_name, neurons, epochs, batch_size, validation_split, end_date = model_data
		models.append({
			'model': model_name,
			'neurons': neurons,
			'epochs': epochs,
			'batch_size': batch_size,
			'validation_split': validation_split,
			'end_date_in_dateset': end_date,
		})
	return json.dumps(models)

@app.route('/FFNN/trained')
def fr_FFNN_trained():
	models = []
	for model_data in get_trained('FFNN'):
		model_name, neurons, epochs, batch_size, validation_split, end_date = model_data
		models.append({
			'model': model_name,
			'neurons': neurons,
			'epochs': epochs,
			'batch_size': batch_size,
			'validation_split': validation_split,
			'end_date_in_dateset': end_date,
		})
	return json.dumps(models)

@app.route('/FFNN/trained', methods=['DELETE'])
def fr_FFNN_trained_delete():
	model = request.form.get('id')
	model_folder = os.path.join(Models_trained_folder, 'FFNN', model)
	for file in os.listdir(model_folder):
		os.remove(os.path.join(model_folder, file))
	os.rmdir(model_folder)
	return json.dumps(success_200_message('ok'))

from Models.FFNN_predict import FFNN_predict_new_numbers
@app.route('/FFNN/predict/new')
def fr_FFNN_predict_new():
	model = request.args.get('model')
	model_path = os.path.join(Models_trained_folder, 'FFNN', model, 'model')
	numbers_str, numbers_str_prob = FFNN_predict_new_numbers(model_path)
	return json.dumps({'numbers_str': numbers_str, 'numbers_str_prob': numbers_str_prob, 'last_day': get_last_day()})

from Models.FFNN_predict import FFNN_predict_past_date
@app.route('/FFNN/predict/past_date')
def fr_FFNN_predict_past_date():
	model = request.args.get('model')
	date = request.args.get('date')
	pred_num = int(request.args.get('pred_num'))
	model_path = os.path.join(Models_trained_folder, 'FFNN', model, 'model')
	predicted_numbers, predicted_numbers_with_prob, origin_numbers, anaylsis_one_date = FFNN_predict_past_date(model_path, date, pred_num)
	return json.dumps({'predicted_numbers': predicted_numbers, 'predicted_numbers_with_prob': predicted_numbers_with_prob, 'origin_numbers': origin_numbers, 'anaylsis_one_date': anaylsis_one_date})


############################   CNN model   ############################
@app.route('/CNN/training')
def fr_CNN_training():
	models = []
	for model_data in get_trainings('CNN'):
		model_name, neurons, epochs, batch_size, validation_split, end_date = model_data
		models.append({
			'model': model_name,
			'neurons': neurons,
			'epochs': epochs,
			'batch_size': batch_size,
			'validation_split': validation_split,
			'end_date_in_dateset': end_date,
		})
	return json.dumps(models)

from Models.train import CNN_train
@app.route('/CNN/train/new', methods=['POST'])
def fr_CNN_train_new():
	dataset_loading()
	
	param_str = request.form.get('param_str')
	try:
		neurons, epochs, batch_size, validation_split = param_str.split(',')
		epochs, batch_size, validation_split = int(epochs), int(batch_size), float(validation_split)
	except:
		return json.dumps(error_400_message('Model parameters are wrong. Please click to "help" for details.'))
	trainings, trained = get_trainings('CNN'), get_trained('CNN')
	for model in trainings:
		if neurons == model[1]: return json.dumps(error_400_message('The given model is being trained now!'))
	for model in trained:
		if neurons == model[1]: return json.dumps(error_400_message('The given model has been trained already!'))
	try:
		neurons = neurons.split(';')
		neurons = [int(neuron) for neuron in neurons]
	except:
		return json.dumps(error_400_message('[nuerons] are wrong. Please click to "help" for details.'))
	if len(neurons) != 6:	return json.dumps(error_400_message('[nuerons] are wrong. Please click to "help" for details.'))
	if neurons[-1] != 20: return json.dumps(error_400_message('[nuerons] are wrong. Please click to "help" for details.'))
	train_started = False
	for thread in threads:
		if not thread.locked():
			train_started = True
			thread.acquire()
			_thread.start_new(CNN_train, ([neurons, epochs, batch_size, validation_split], param_str, thread))
			break
	if not train_started: return json.dumps(error_400_message('There could not be trained more than %d models to be being trained' % thread_num))
	return json.dumps(success_200_message(get_last_day()))

@app.route('/CNN/trained')
def fr_CNN_trained():
	models = []
	for model_data in get_trained('CNN'):
		model_name, neurons, epochs, batch_size, validation_split, end_date = model_data
		models.append({
			'model': model_name,
			'neurons': neurons,
			'epochs': epochs,
			'batch_size': batch_size,
			'validation_split': validation_split,
			'end_date_in_dateset': end_date,
		})
	return json.dumps(models)

@app.route('/CNN/trained', methods=['DELETE'])
def fr_CNN_trained_delete():
	model = request.form.get('id')
	model_folder = os.path.join(Models_trained_folder, 'CNN', model)
	for file in os.listdir(model_folder):
		os.remove(os.path.join(model_folder, file))
	os.rmdir(model_folder)
	return json.dumps(success_200_message('ok'))

from Models.CNN_predict import CNN_predict_new_numbers
@app.route('/CNN/predict/new')
def fr_CNN_predict_new():
	model = request.args.get('model')
	model_path = os.path.join(Models_trained_folder, 'CNN', model, 'model')
	numbers_str, numbers_str_prob = CNN_predict_new_numbers(model_path)
	return json.dumps({'numbers_str': numbers_str, 'numbers_str_prob': numbers_str_prob, 'last_day': get_last_day()})

from Models.CNN_predict import CNN_predict_past_date
@app.route('/CNN/predict/past_date')
def fr_CNN_predict_past_date():
	model = request.args.get('model')
	date = request.args.get('date')
	pred_num = int(request.args.get('pred_num'))
	model_path = os.path.join(Models_trained_folder, 'CNN', model, 'model')
	predicted_numbers, predicted_numbers_with_prob, origin_numbers, anaylsis_one_date = CNN_predict_past_date(model_path, date, pred_num)
	return json.dumps({'predicted_numbers': predicted_numbers, 'predicted_numbers_with_prob': predicted_numbers_with_prob, 'origin_numbers': origin_numbers, 'anaylsis_one_date': anaylsis_one_date})


############################   RNN model   ############################
@app.route('/RNN/training')
def fr_RNN_training():
	models = []
	for model_data in get_trainings('RNN'):
		model_name, neurons, epochs, batch_size, validation_split, end_date = model_data
		models.append({
			'model': model_name,
			'neurons': neurons,
			'epochs': epochs,
			'batch_size': batch_size,
			'validation_split': validation_split,
			'end_date_in_dateset': end_date,
		})
	return json.dumps(models)

from Models.train import RNN_train
@app.route('/RNN/train/new', methods=['POST'])
def fr_RNN_train_new():
	dataset_loading()
	
	param_str = request.form.get('param_str')
	try:
		neurons, epochs, batch_size, validation_split = param_str.split(',')
		epochs, batch_size, validation_split = int(epochs), int(batch_size), float(validation_split)
	except:
		return json.dumps(error_400_message('Model parameters are wrong. Please click to "help" for details.'))
	trainings, trained = get_trainings('RNN'), get_trained('RNN')
	for model in trainings:
		if neurons == model[1]: return json.dumps(error_400_message('The given model is being trained now!'))
	for model in trained:
		if neurons == model[1]: return json.dumps(error_400_message('The given model has been trained already!'))
	try:
		neurons = neurons.split(';')
		neurons = [int(neuron) for neuron in neurons]
	except:
		return json.dumps(error_400_message('[nuerons] are wrong. Please click to "help" for details.'))
	if len(neurons) < 4:	return json.dumps(error_400_message('[nuerons] are wrong. Please click to "help" for details.'))
	if neurons[-1] != 20: return json.dumps(error_400_message('[nuerons] are wrong. Please click to "help" for details.'))
	train_started = False
	for thread in threads:
		if not thread.locked():
			train_started = True
			thread.acquire()
			_thread.start_new(RNN_train, ([neurons, epochs, batch_size, validation_split], param_str, thread))
			break
	if not train_started: return json.dumps(error_400_message('There could not be trained more than %d models to be being trained' % thread_num))
	return json.dumps(success_200_message(get_last_day()))

@app.route('/RNN/trained')
def fr_RNN_trained():
	models = []
	for model_data in get_trained('RNN'):
		model_name, neurons, epochs, batch_size, validation_split, end_date = model_data
		models.append({
			'model': model_name,
			'neurons': neurons,
			'epochs': epochs,
			'batch_size': batch_size,
			'validation_split': validation_split,
			'end_date_in_dateset': end_date,
		})
	return json.dumps(models)

@app.route('/RNN/trained', methods=['DELETE'])
def fr_RNN_trained_delete():
	model = request.form.get('id')
	model_folder = os.path.join(Models_trained_folder, 'RNN', model)
	for file in os.listdir(model_folder):
		os.remove(os.path.join(model_folder, file))
	os.rmdir(model_folder)
	return json.dumps(success_200_message('ok'))

from Models.RNN_predict import RNN_predict_new_numbers
@app.route('/RNN/predict/new')
def fr_RNN_predict_new():
	model = request.args.get('model')
	model_path = os.path.join(Models_trained_folder, 'RNN', model, 'model')
	numbers_str, numbers_str_prob = RNN_predict_new_numbers(model_path)
	return json.dumps({'numbers_str': numbers_str, 'numbers_str_prob': numbers_str_prob, 'last_day': get_last_day()})

from Models.RNN_predict import RNN_predict_past_date
@app.route('/RNN/predict/past_date')
def fr_RNN_predict_past_date():
	model = request.args.get('model')
	date = request.args.get('date')
	pred_num = int(request.args.get('pred_num'))
	model_path = os.path.join(Models_trained_folder, 'RNN', model, 'model')
	predicted_numbers, predicted_numbers_with_prob, origin_numbers, anaylsis_one_date = RNN_predict_past_date(model_path, date, pred_num)
	return json.dumps({'predicted_numbers': predicted_numbers, 'predicted_numbers_with_prob': predicted_numbers_with_prob, 'origin_numbers': origin_numbers, 'anaylsis_one_date': anaylsis_one_date})


############################   MultiModels   ############################
@app.route('/MultiModels/trained')
def fr_MultiModels_trained():
	models = []
	for model_type in ['FFNN', 'CNN', 'RNN']:
		for model_data in get_trained(model_type):
			model_name, neurons, epochs, batch_size, validation_split, end_date = model_data
			models.append({
				'type': model_type,
				'model': model_name,
				'neurons': neurons,
				'end_date_in_dateset': end_date,
			})
	return json.dumps(models)

from Models.FFNN_predict import FFNN_predict_new_numbers_simple
from Models.CNN_predict import CNN_predict_new_numbers_simple
from Models.RNN_predict import RNN_predict_new_numbers_simple
from Models.MultiModels import predict_new_numbers
@app.route('/MultiModels/predict/new')
def fr_MultiModels_predict_new():
	model = request.args.get('model')
	models = model.split('/')
	numbers_all, probs_all = [], []
	for model_info in models:
		model_type, model_name = model_info.split('_')
		model_path = os.path.join(Models_trained_folder, model_type, model_name, 'model')
		if model_type == 'FFNN':
			numbers, probs = FFNN_predict_new_numbers_simple(model_path)
		elif model_type == 'CNN':
			numbers, probs = CNN_predict_new_numbers_simple(model_path)
		else:
			numbers, probs = RNN_predict_new_numbers_simple(model_path)
		numbers_all += numbers
		probs_all += probs
	numbers_str, numbers_str_prob = predict_new_numbers(numbers_all, probs_all)
	return json.dumps({'numbers_str': numbers_str, 'numbers_str_prob': numbers_str_prob, 'last_day': get_last_day()})

from Models.FFNN_predict import FFNN_predict_past_date_simple
from Models.CNN_predict import CNN_predict_past_date_simple
from Models.RNN_predict import RNN_predict_past_date_simple
from Models.MultiModels import predict_past_date
@app.route('/MultiModels/predict/past_date')
def fr_MultiModels_predict_past_date():
	model = request.args.get('model')
	date = request.args.get('date')
	models = model.split('/')
	numbers_all, exact_numbers = [], []
	for model_info in models:
		model_type, model_name = model_info.split('_')
		model_path = os.path.join(Models_trained_folder, model_type, model_name, 'model')
		if model_type == 'FFNN':
			numbers, numbers_y = FFNN_predict_past_date_simple(model_path, date)
		elif model_type == 'CNN':
			numbers, numbers_y = CNN_predict_past_date_simple(model_path, date)
		else:
			numbers, numbers_y = RNN_predict_past_date_simple(model_path, date)
		numbers_all += numbers
		exact_numbers = numbers_y
	predicted_numbers, origin_numbers, anaylsis_one_date = predict_past_date(numbers_all, exact_numbers)
	return json.dumps({'predicted_numbers': predicted_numbers, 'origin_numbers': origin_numbers, 'anaylsis_one_date': anaylsis_one_date})


if __name__ == "__main__":
	dataset_loading()
	app.run(debug=True, host='0.0.0.0', port=2000, threaded=True)
