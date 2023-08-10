import pandas as pd
import numpy as np
from keras.models import load_model

def predict_new_numbers(numbers_all, probs):
	numbers = list(set(numbers_all))
	numbers.sort()
	numbers_str = ''
	for i, item in enumerate(numbers):
		numbers_str += '%02d  ' % item
		if i % 5 == 4:
			numbers_str += '\n'
	
	indices = np.argsort(probs)[::-1]
	thresholds = [0.9, 0.8, 0.7, 0.6, 0.5]
	threshold = thresholds.pop(0)
	prob_nums = {}
	numbers_added = []
	for ind in indices:
		if numbers_all[ind] in numbers_added: continue
		if probs[ind] < threshold:
			threshold = thresholds.pop(0)
		key = str(threshold)
		if key not in prob_nums.keys():
			prob_nums[key] = [numbers_all[ind]]
		elif numbers_all[ind] not in prob_nums[key]:
			prob_nums[key].append(numbers_all[ind])
		numbers_added.append(numbers_all[ind])
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

def predict_past_date(numbers_all, y):
	numbers = list(set(numbers_all))
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

	return predicted_numbers, origin_numbers, 'Predicted {} numbers, and\n\nCorrect Numbers: ({})\n'.format(len(numbers), len(corrected)) + ', '.join(corrected) + '\n\nNear Numbers: ({})\n'.format(len(one_diffed)) + ', '.join(one_diffed)
