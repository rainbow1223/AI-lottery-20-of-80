import urllib.request, os
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import numpy as np

dataset_folder = 'dataset'
if not os.path.isdir(dataset_folder): os.mkdir(dataset_folder)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def dataset_loading():
	series = pd.read_csv(os.path.join(dataset_folder, 'dataset.csv'))
	last_year = series['Year'].values[-1]
	last_month, last_day = series['Month_Date'].values[-1].split(' ')[-2:]
	last_month, last_day = months.index(last_month) + 1, int(last_day)
	last_date = datetime(last_year, last_month, last_day)
	cur_date = datetime.now()
	cur_date = datetime(cur_date.year, cur_date.month, cur_date.day)
	diff_days = (cur_date - last_date).days + 1
	if diff_days <= 3: diff_days = 3
	elif diff_days <= 10: diff_days = 10
	elif diff_days <= 30: diff_days = 30
	elif diff_days <= 180: diff_days = 180
	if diff_days in [3, 10]:
		url = "https://www.walottery.com/WinningNumbers/PastDrawings.aspx?gamename=dailykeno&unittype=draw&unitcount=" + str(diff_days)
	else:
		url = "https://www.walottery.com/WinningNumbers/PastDrawings.aspx?gamename=dailykeno&unittype=day&unitcount=" + str(diff_days)
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")

	day = []
	date_month = []
	year = []
	col1 = []
	col2 = []
	col3 = []
	col4 = []
	col5 = []
	col6 = []
	col7 = []
	col8 = []
	col9 = []
	col10 = []
	col11 = []
	col12 = []
	col13 = []
	col14 = []
	col15 = []
	col16 = []
	col17 = []
	col18 = []
	col19 = []
	col20 = []
	colloect = soup.find_all("table", class_="table-viewport-small")
	for item in colloect:
		small = item.find('h2').text.split(',')
		day.insert(0, small[0])
		date_month.insert(0, small[1])
		year.insert(0, eval(small[2]))

		small = item.find_all('li')
		col1.insert(0, int(small[0].text))
		col2.insert(0, int(small[1].text))
		col3.insert(0, int(small[2].text))
		col4.insert(0, int(small[3].text))
		col5.insert(0, int(small[4].text))
		col6.insert(0, int(small[5].text))
		col7.insert(0, int(small[6].text))
		col8.insert(0, int(small[7].text))
		col9.insert(0, int(small[8].text))
		col10.insert(0, int(small[9].text))
		col11.insert(0, int(small[10].text))
		col12.insert(0, int(small[11].text))
		col13.insert(0, int(small[12].text))
		col14.insert(0, int(small[13].text))
		col15.insert(0, int(small[14].text))
		col16.insert(0, int(small[15].text))
		col17.insert(0, int(small[16].text))
		col18.insert(0, int(small[17].text))
		col19.insert(0, int(small[18].text))
		col20.insert(0, int(small[19].text))

	"""new = pd.DataFrame({'Day':day, ', 'Year':year,
						'Col1':col1, 'Col2':col2, 'Col3':col3, 'Col4':col4, 'Col5':col5,
						'Col6':col6, 'Col7':col7, 'Col8':col8, 'Col9':col9, 'Col10':col10,
						'Col11':col11, 'Col12':col12, 'Col13':col13, 'Col14':col14, 'Col15':col15,
						'Col16':col16, 'Col17':col17, 'Col18':col18, 'Col19':col19, 'Col20':col20
						})"""
	new = pd.DataFrame({'Day':day})
	new = new.assign(Month_Date=date_month)
	new = new.assign(Year=year)
	new = new.assign(Col1=col1)
	new = new.assign(Col2=col2)
	new = new.assign(Col3=col3)
	new = new.assign(Col4=col4)
	new = new.assign(Col5=col5)
	new = new.assign(Col6=col6)
	new = new.assign(Col7=col7)
	new = new.assign(Col8=col8)
	new = new.assign(Col9=col9)
	new = new.assign(Col10=col10)
	new = new.assign(Col11=col11)
	new = new.assign(Col12=col12)
	new = new.assign(Col13=col13)
	new = new.assign(Col14=col14)
	new = new.assign(Col15=col15)
	new = new.assign(Col16=col16)
	new = new.assign(Col17=col17)
	new = new.assign(Col18=col18)
	new = new.assign(Col19=col19)
	new = new.assign(Col20=col20)
	i = 0
	for i in range(len(new.values)):
		if (series.values[-1][:3] == new.values[i][:3]).sum() == 3: break
	pd.DataFrame(data=np.vstack([series.values, new.values[i+1:]]), columns=series.columns).to_csv(os.path.join(dataset_folder, 'dataset.csv'), index=None)
