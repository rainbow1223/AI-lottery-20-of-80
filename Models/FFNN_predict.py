import pandas as pd
import numpy as np
from keras.models import load_model
import os  
from keras import backend as K
from download import dataset_loading
def FFNN_predict_new_numbers_simple(model_name):
	dataset_loading()

	model = load_model(model_name)
	n_input_size = int(model_name.split('-')[1].split(';')[0]) // 20
	series = pd.read_csv('dataset/dataset.csv')
	all_data = series.values[:, 3:]
	x = np.reshape(all_data[-n_input_size:], (-1))
	x = np.expand_dims(x, 0).astype('float32')
	K.clear_session()
	result = model.predict(x)[0]
	K.clear_session()
	numbers, probs = [], []
	for item in result:
	#	num1 = int(item)
	#	num2 = int(item) + 1
		num1 = min(int(abs(np.rint(item))), 80)
		num2 = min(int(abs(np.rint(item))) + 1, 80)
		if num1 == 0:
			numbers.append(num2)
			probs.append(1 - abs(num2 - item))
		else:
			numbers.append(num1)
			probs.append(1 - abs(num1 - item))
	return numbers, probs

def FFNN_predict_new_numbers(model_name):
	dataset_loading()

	model = load_model(model_name)
	n_input_size = int(model_name.split('-')[1].split(';')[0]) // 20
	series = pd.read_csv('dataset/dataset.csv')
	all_data = series.values[:, 3:]
	x = np.reshape(all_data[-n_input_size:], (-1))
	x = np.expand_dims(x, 0).astype('float32')
	# x = tf.convert_to_tensorflow(x)
##  x = np.array(x).astype('float32')
	K.clear_session()
	result = model.predict(x)[0]
	K.clear_session()
	numbers, probs = [], []
	for item in result:
		num1 = min(int(abs(np.rint(item))), 80)
		num2 = min(int(abs(np.rint(item))) + 1, 80)
		if num1 not in numbers and num1 > 0:
			numbers.append(num1)
			probs.append(1 - abs(num1 - item))
		if num2 not in numbers:
			numbers.append(num2)
			probs.append(1 - abs(num2 - item))
	while len(numbers) < 40:
		num1 = np.random.randint(1, 80)
		if num1 not in numbers:
			numbers.append(num1)
			probs.append(0)

	numbers1 = numbers.copy()
	numbers.sort()
	numbers_str = ''
	for i, item in enumerate(numbers):
		numbers_str += '%02d  ' % item
		if i % 5 == 4:
			numbers_str += '\n'
	
	indices = np.argsort(probs)[::-1]
	thresholds = [0.8, 0.6, 0.4, 0.2, 0.0]
	threshold = thresholds.pop(0)
	prob_nums = {}
	for ind in indices:
		if probs[ind] < threshold and len(thresholds) > 0:
			threshold = thresholds.pop(0)
		key = str(threshold)
		if key not in prob_nums.keys():
			prob_nums[key] = [numbers1[ind]]
		else:
			prob_nums[key].append(numbers1[ind])
	numbers_str_prob = ''
	for key in prob_nums.keys():
		numbers = prob_nums[key]
		if len(numbers) < 1:
			continue
		numbers.sort()
		numbers_str_prob += key +':'
		for item in numbers:
			numbers_str_prob += '  %02d' % item
		numbers_str_prob += '\n'
	return numbers_str, numbers_str_prob

def FFNN_predict_past_date_simple(model_name, date):
	model = load_model(model_name)
	n_input_size = int(model_name.split('-')[1].split(';')[0]) // 20
	
	month_date, year = date.split(', '); year = int(year); month_date = ' ' + month_date
	series = pd.read_csv('dataset/dataset.csv')
	for i in range(len(series) - 1, -1, -1):
		if series.Month_Date[i] == month_date and series.Year[i] == year: break
	all_data = series.values[:, 3:]
	x = np.reshape(all_data[i-n_input_size:i], (-1))
	y = all_data[i]
	x = np.expand_dims(x, 0).astype('float32')
	K.clear_session()
	result = model.predict(x)[0]
	K.clear_session()
	numbers, probs = [], []
	for item in result:
	#	num1 = int(item)
	#	num2 = int(item) + 1
		num1 = min(int(abs(np.rint(item))), 80)
		num2 = min(int(abs(np.rint(item))) + 1, 80)
		if  num1 == 0:
			numbers.append(num2)
			probs.append(1 - abs(num2 - item))
		else:
			numbers.append(num1)
			probs.append(1 - abs(num1 - item))
	return numbers, y.tolist()

def FFNN_predict_past_date(model_name, date, pred_num=30):
	model = load_model(model_name)
	n_input_size = int(model_name.split('-')[1].split(';')[0]) // 20
	
	month_date, year = date.split(', '); year = int(year); month_date = ' ' + month_date
	series = pd.read_csv('dataset/dataset.csv')
	for i in range(len(series) - 1, -1, -1):
		if series.Month_Date[i] == month_date and series.Year[i] == year: break
	all_data = series.values[:, 3:]
	x = all_data[i-n_input_size:i]
	y = all_data[i]
	x = np.expand_dims(x, 0).astype('float32')
	K.clear_session()
	result = model.predict(x)[0]
	K.clear_session()
	numbers, probs = [], []
	for item in result:
		num1 = min(np.rint(abs(item)), 80)
		num2 = min(np.rint(abs(item)) + 1, 80)
		if num1 not in numbers and num1 > 0:
			numbers.append(num1)
			probs.append(1 - abs(num1 - item))
		if num2 not in numbers:
			numbers.append(num2)
			probs.append(1 - abs(num2 - item))
	while len(numbers) < 40:
		num1 = np.random.randint(1, 80)
		if num1 not in numbers:
			numbers.append(num1)
			probs.append(0)

	numbers1 = numbers.copy()
	numbers = np.array(numbers)[np.argsort(probs)[::-1][:pred_num]]
	numbers.sort()
	predicted_numbers = ''
	corrected, one_diffed = [], []
	for i, item in enumerate(numbers):
		predicted_numbers += '%02d  ' % item
		if i % 5 == 4:
			predicted_numbers += '\n'
		if item in y:
			corrected.append(str(item))
		elif item - 1 in y:
			one_diffed.append(str(item))
		elif item + 1 in y:
			one_diffed.append(str(item))
	origin_numbers = ''
	for i, item in enumerate(y):
		origin_numbers += '%02d  ' % item
		if i % 5 == 4:
			origin_numbers += '\n'
	
	indices = np.argsort(probs)[::-1][:pred_num]
	thresholds = [0.8, 0.6, 0.4, 0.2, 0.0]
	threshold = thresholds.pop(0)
	prob_nums = {}
	for ind in indices:
		if probs[ind] < threshold and len(thresholds) > 0:
			threshold = thresholds.pop(0)
		key = str(threshold)
		if key not in prob_nums.keys():
			prob_nums[key] = [numbers1[ind]]
		else:
			prob_nums[key].append(numbers1[ind])
	numbers_str_prob = ''
	for key in prob_nums.keys():
		numbers = prob_nums[key]
		if len(numbers) < 1:
			continue
		numbers.sort()
		numbers_str_prob += key +':'
		for item in numbers:
			numbers_str_prob += '  %02d' % item
		numbers_str_prob += '\n'

	return predicted_numbers, numbers_str_prob, origin_numbers, 'Correct Numbers: ({})\n'.format(len(corrected)) + ', '.join(corrected) + '\n\nNear Numbers: ({})\n'.format(len(one_diffed)) + ', '.join(one_diffed)
