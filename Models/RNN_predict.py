import pandas as pd
import numpy as np
from keras.models import load_model
from keras import backend as K
from download import dataset_loading
def RNN_predict_new_numbers_simple(model_name):
	dataset_loading()

	model = load_model(model_name)
	n_input_size = int(model_name.split('-')[1].split(';')[0])
	series = pd.read_csv('dataset/dataset.csv')
	all_data1 = series.values[:, 3:]
	all_data2 = np.roll(all_data1, 1, axis=1)
	all_data2[:, 0] = 0
	all_data = all_data1 - all_data2
	x = all_data[-n_input_size:]
#	x = all_data[-n_input_size:] / 80
	x = np.expand_dims(x, 0).astype('float32')/80
	K.clear_session()
	result = model.predict(x)[0] 
	result = [abs(x) * 80 for x in result]

	numbers1, probs1 = [], []
	for item in result:
		num1 = np.round(item) 
		if num1 == 0:
			num1 += 1
			probs1.append(item)
		else:
			probs1.append(1 - abs(num1 - item))
		numbers1.append(num1)
	numbers1 = np.array(numbers1)
	probs1 = np.array(probs1)

	numbers, probs = [numbers1[0]], [probs1[0]]
	for i in range(1, len(numbers1)):
		s = np.sum(numbers1[:i+1])
		p = np.mean(probs1[:i+1])
		if s > 80:
			if 80.0 not in numbers:
				numbers.append(80)
				probs.append(p) 
			else:
				rand = np.random.randint(40+2*i, 80)
				if rand not in numbers:
					numbers.append(rand)
					probs.append(0.2)
		else:
			numbers.append(s) 
			probs.append(p)
			
	return numbers, probs

def RNN_predict_new_numbers(model_name):
	dataset_loading()

	model = load_model(model_name)
	n_input_size = int(model_name.split('-')[1].split(';')[0])
	series = pd.read_csv('dataset/dataset.csv')
	all_data1 = series.values[:, 3:]
	all_data2 = np.roll(all_data1, 1, axis=1)
	all_data2[:, 0] = 0
	all_data = all_data1 - all_data2
	x = all_data[-n_input_size:]
	x = np.expand_dims(x, 0).astype('float32') / 80
	#x = np.expand_dims(x, 0)
	K.clear_session()
	result = model.predict(x)[0]
	result = [abs(x) * 80 for x in result]
	numbers1, probs1 = [], []
	for item in result:
		num1 = np.round(item) 
		if num1 == 0:
			num1 += 1
			probs1.append(item)
		else:
			probs1.append(1 - abs(num1 - item))
		numbers1.append(num1)
	numbers1 = np.array(numbers1)
	probs1 = np.array(probs1)

	numbers, probs = [numbers1[0]], [probs1[0]]
	for i in range(1, len(numbers1)):
		s = np.sum(numbers1[0:i+1])
		p = np.mean(probs1[0:i+1])
		if s > 80:
			if 80.0 not in numbers:
				numbers.append(80)
				probs.append(p) 
			else:
				rand = np.random.randint(40+2*i, 80)
				if rand not in numbers:
					numbers.append(rand)
					probs.append(0.2)
		else:
			numbers.append(s) 
			probs.append(p)
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

def RNN_predict_past_date_simple(model_name, date):
	model = load_model(model_name)
	n_input_size = int(model_name.split('-')[1].split(';')[0])
	
	month_date, year = date.split(', '); year = int(year); month_date = ' ' + month_date
	series = pd.read_csv('dataset/dataset.csv')
	for i in range(len(series) - 1, -1, -1):
		if series.Month_Date[i] == month_date and series.Year[i] == year: break
	all_data1 = series.values[:, 3:]
	all_data2 = np.roll(all_data1, 1, axis=1)
	all_data2[:, 0] = 0
	all_data = all_data1 - all_data2
	x = all_data[i-n_input_size:i]
	x = np.expand_dims(x, 0).astype('float32') / 80
	y = all_data1[i]
	K.clear_session()
	result = model.predict(x)[0]
	result = [abs(x) * 80 for x in result]
	numbers1, probs1 = [], []
	for item in result:
		num1 = np.round(item) 
		if num1 == 0:
			num1 += 1
			probs1.append(item)
		else:
			probs1.append(1 - abs(num1 - item))
		numbers1.append(num1)
	numbers1 = np.array(numbers1)
	probs1 = np.array(probs1)
	numbers, probs = [numbers1[0]], [probs1[0]]
	for i in range(1, len(numbers1)):
		s = np.sum(numbers1[0:i+1])
		p = np.mean(probs1[0:i+1])
		if s > 80:
			if 80.0 not in numbers:
				numbers.append(80)
				probs.append(p) 
			else:
				rand = np.random.randint(40+2*i, 80)
				if rand not in numbers:
					numbers.append(rand)
					probs.append(0.2)
		else:
			numbers.append(s) 
			probs.append(p)
	return numbers, y.tolist()

def RNN_predict_past_date(model_name, date, pred_num=30):
	model = load_model(model_name)
	n_input_size = int(model_name.split('-')[1].split(';')[0])
	
	month_date, year = date.split(', '); year = int(year); month_date = ' ' + month_date
	series = pd.read_csv('dataset/dataset.csv')
	for i in range(len(series) - 1, -1, -1):
		if series.Month_Date[i] == month_date and series.Year[i] == year: break
	all_data1 = series.values[:, 3:]
	all_data2 = np.roll(all_data1, 1, axis=1)
	all_data2[:, 0] = 0
	all_data = all_data1 - all_data2
	x = all_data[i-n_input_size:i]
	y = all_data1[i]
	x = np.expand_dims(x, 0).astype('float32') / 80
	K.clear_session()
	result = model.predict(x)[0]
	result = [abs(x) * 80 for x in result]
	print(result)
	numbers1, probs1 = [], []
	for item in result:
		num1 = np.round(item) 
		if num1 == 0:
			num1 += 1
			probs1.append(item)
		else:
			probs1.append(1 - abs(num1 - item))
		numbers1.append(num1)
	numbers1 = np.array(numbers1)
	probs1 = np.array(probs1)
	print(numbers1)
	print(probs1)
	numbers, probs = [numbers1[0]], [probs1[0]]
	for i in range(1, len(numbers1)):
		s = np.sum(numbers1[0:i+1])
		p = np.mean(probs1[0:i+1])
		if s > 80:
			if 80.0 not in numbers:
				numbers.append(80)
				probs.append(p) 
			else:
				rand = np.random.randint(40+2*i, 80)
				if rand not in numbers:
					numbers.append(rand)
					probs.append(0.2)
		else:
			numbers.append(s) 
			probs.append(p)
	while len(numbers) < 40:
		num1 = np.random.randint(1, 80)
		if num1 not in numbers:
			numbers.append(num1)
			probs.append(0)

	numbers2 = numbers.copy()
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
			prob_nums[key] = [numbers2[ind]]
		else:
			prob_nums[key].append(numbers2[ind])
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
