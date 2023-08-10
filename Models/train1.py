# import the necessary packages
import os
import pandas as pd

# epochs to train for
dataset_folder = 'dataset'

def get_last_day():
	series = pd.read_csv(os.path.join(dataset_folder, 'dataset.csv'))
	return series.values[-1, 1].strip() + ', ' + str(series.values[-1, 2])
