# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from .model import FFNN, CNN, RNN
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np
import os, shutil
import pandas as pd

# epochs to train for(
INIT_LR = 0.001
dataset_folder = 'dataset'
Models_trained_folder = 'Models_trained'
Models_training_folder = 'Models_training'

def get_last_day():
	series = pd.read_csv(os.path.join(dataset_folder, 'dataset.csv'))
	return series.values[-1, 1].strip() + ', ' + str(series.values[-1, 2])

def FFNN_train(params, param_str, thread, new_training=True):
	neurons, EPOCHS, batch_size, validation_split = params
	n_input_size = neurons[0] // 20
	
	series = pd.read_csv(os.path.join(dataset_folder, 'dataset.csv'))
	all_data = series.values[:, 3:]
	x, y = [], []
	for i in range(n_input_size, len(all_data)):
		x.append(np.reshape(all_data[i - n_input_size:i], (-1)))
		y.append(all_data[i])
	x = np.array(x).astype('float32')
	y = np.array(y).astype('float32')
	indices = np.arange(len(x))
	np.random.shuffle(indices)
	x = x[indices]
	y = y[indices]
	# initialize the optimizer and model
	opt = Adam(lr=INIT_LR, decay=INIT_LR / 200)
	model = FFNN(neurons)
	model.compile(loss="mse", optimizer=opt)
	model.summary()
	FFNN_folder1 = os.path.join(Models_trained_folder, 'FFNN')
	FFNN_folder2 = os.path.join(Models_training_folder, 'FFNN')

	model_folder2 = os.path.join(FFNN_folder2, 'model-' + param_str.split(',')[0])
	os.makedirs(model_folder2)
	model_path = os.path.join(model_folder2, 'model')
	with open(os.path.join(model_folder2, 'param_str.txt'), 'w') as f:
		f.write(param_str + '\n' + series.values[-1, 1].strip() + ', ' + str(series.values[-1, 2]))
#	H = model.fit(x, y, epochs=EPOCHS, verbose=0, batch_size=batch_size, validation_split=validation_split, callbacks=[ModelCheckpoint(filepath=model_path, monitor='val_loss', save_best_only=True)])
	model.fit(x, y, epochs=EPOCHS, verbose=0, batch_size=batch_size, validation_split=validation_split, callbacks=[ModelCheckpoint(filepath=model_path, monitor='val_loss', save_best_only=True)])
	
	model_folder1 = os.path.join(FFNN_folder1, 'model-' + param_str.split(',')[0])
	os.makedirs(model_folder1)
	shutil.move(os.path.join(model_folder2, 'param_str.txt'), os.path.join(model_folder1, 'param_str.txt'))
	shutil.move(os.path.join(model_folder2, 'model'), os.path.join(model_folder1, 'model'))
	os.rmdir(model_folder2)
	thread.release()

def CNN_train(params, param_str, thread, new_training=True):
	neurons, EPOCHS, batch_size, validation_split = params
	n_input_size = neurons[0]
	
	series = pd.read_csv(os.path.join(dataset_folder, 'dataset.csv'))
	all_data = series.values[:, 3:]
	x, y = [], []
	for i in range(n_input_size, len(all_data)):
		x.append(all_data[i - n_input_size:i])
		y.append(all_data[i])
	x = np.array(x, dtype=np.float) / 80
	y = (np.array(y, dtype=np.float) - 40) / 40
	indices = np.arange(len(x))
	np.random.shuffle(indices)
	x = x[indices]
	y = y[indices]
	# initialize the optimizer and model
	opt = Adam(lr=INIT_LR, decay=INIT_LR / 200)
	model = CNN(neurons)
	model.compile(loss="ame", optimizer=opt)
	model.summary()
	CNN_folder1 = os.path.join(Models_trained_folder, 'CNN')
	CNN_folder2 = os.path.join(Models_training_folder, 'CNN')

	model_folder2 = os.path.join(CNN_folder2, 'model-' + param_str.split(',')[0])
	os.makedirs(model_folder2)
	model_path = os.path.join(model_folder2, 'model')
	with open(os.path.join(model_folder2, 'param_str.txt'), 'w') as f:
		f.write(param_str + '\n' + series.values[-1, 1].strip() + ', ' + str(series.values[-1, 2]))
	model.fit(x, y, epochs=EPOCHS, verbose=0, batch_size=batch_size, validation_split=validation_split, callbacks=[ModelCheckpoint(filepath=model_path, monitor='val_loss', save_best_only=True)])
	
	model_folder1 = os.path.join(CNN_folder1, 'model-' + param_str.split(',')[0])
	os.makedirs(model_folder1)
	shutil.move(os.path.join(model_folder2, 'param_str.txt'), os.path.join(model_folder1, 'param_str.txt'))
	shutil.move(os.path.join(model_folder2, 'model'), os.path.join(model_folder1, 'model'))
	os.rmdir(model_folder2)
	thread.release()

def RNN_train(params, param_str, thread, new_training=True):
	neurons, EPOCHS, batch_size, validation_split = params
	n_input_size = neurons[0]
	
	series = pd.read_csv(os.path.join(dataset_folder, 'dataset.csv'))
	all_data1 = series.values[:, 3:]
	all_data2 = np.roll(all_data1, 1, axis=1)
	all_data2[:, 0] = 0
	all_data = all_data1 - all_data2
	x, y = [], []
	for i in range(n_input_size, len(all_data)):
		x.append(all_data[i - n_input_size:i])
		y.append(all_data[i])
	x = np.array(x).astype('float32') / 80
	y = np.array(y).astype('float32') / 80
	indices = np.arange(len(x))
	np.random.shuffle(indices)
	x = x[indices]
	y = y[indices]
	# initialize the optimizer and model
	opt = Adam(lr=INIT_LR, decay=INIT_LR / 200)
	model = RNN(neurons)
	model.compile(loss="mse", optimizer=opt)
	model.summary()
	RNN_folder1 = os.path.join(Models_trained_folder, 'RNN')
	RNN_folder2 = os.path.join(Models_training_folder, 'RNN')

	model_folder2 = os.path.join(RNN_folder2, 'model-' + param_str.split(',')[0])
	os.makedirs(model_folder2)
	model_path = os.path.join(model_folder2, 'model')
	with open(os.path.join(model_folder2, 'param_str.txt'), 'w') as f:
		f.write(param_str + '\n' + series.values[-1, 1].strip() + ', ' + str(series.values[-1, 2]))
	model.fit(x, y, epochs=EPOCHS, verbose=0, batch_size=batch_size, validation_split=validation_split, callbacks=[ModelCheckpoint(filepath=model_path, monitor='val_loss', save_best_only=True)])
	
	model_folder1 = os.path.join(RNN_folder1, 'model-' + param_str.split(',')[0])
	os.makedirs(model_folder1)
	shutil.move(os.path.join(model_folder2, 'param_str.txt'), os.path.join(model_folder1, 'param_str.txt'))
	shutil.move(os.path.join(model_folder2, 'model'), os.path.join(model_folder1, 'model'))
	os.rmdir(model_folder2)
	thread.release()
