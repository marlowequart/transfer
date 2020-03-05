'''
Use this script to determine the quality of data in a .csv file.
The statistics generated by this script can help determine if the data
is fake or real data.

Statistics by column:
plot a histogram of the values in a column and look for abnormal values
create a list of %change from value to value in a given column. plot this in a normal distribution.

Check for blank columns, rows, cells
check for % of duplicates
check for outliers in the data


Six key dimensions of data quality
https://www.whitepapers.em360tech.com/wp-content/files_mf/1407250286DAMAUKDQDimensionsWhitePaperR37.pdf
1. Completeness
2. Uniqueness
3. Timeliness
4. Validity
5. Accuracy
6. Consistency


If the data is human made, there is more 1s 4s and 7s because people think those numbers are random
1n general, 1 tends to be 50% of data
In general, the number distribution is logrithmic, 1 is highest number,
falling off as numbers get larger

Ask accountants or SEC when looking through numbers, which numbers brings concern of cooking the books


2/12/20: Include a function to check each column against the std dev of the surrounding 20 entries for wierd outliers


'''

import pandas as pd
import re
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
# from matplotlib.ticker import PercentFormatter


#open csv file, return the data in a pandas dataframe
def import_data(file_name):
	#open the file using pandas, use the first row as the header
	data = pd.read_csv(file_name,header=0)
	
	
	#want to check data for duplicate dates and remove any duplicates
	
	
	return data

def hist_basic(list):
	
	plt.hist(list,bins=30)
	plt.show()

def plot_hist(list):
	#this funciton will plot a histogram to bring out the data in the tails
	#the limit val will limit the top of the bars in order to bring out the tail values
	
	#create bins of data
	n_bins=20
	max_data=max(list)
	min_data=min(list)
	dx=(max_data-min_data)/n_bins
	xs = np.arange(min_data,max_data+dx,dx).round(decimals=1)
	
	#####
	#Plot a histogram of the normalized (%) number of values in each range
	#####
	df=pd.DataFrame(list)
	# out=pd.cut(df[0],bins=xs,include_lowest=True)
	# out_norm = out.value_counts(sort=False, normalize=True).mul(100)
	# ax=out_norm.plot.bar(color="b")
	# plt.show()
	
	#####
	#Plot a histogram with the frequency of values in each range
	#####
	out, bins  = pd.cut(df[0], bins=xs, include_lowest=True, right=False, retbins=True)
	# ax=out.value_counts(sort=False).plot.bar()
	# plt.show()
	
	#####
	#print the frequency for each interval, mean, std deviation
	#####
	print(out.value_counts(sort=False))
	print('The mean is '+str(round(np.mean(list),4)))
	print('The std dev is '+str(round(np.std(list),4)))
	
def check_duplicates(list):
	#####
	# Check for number of duplicate entries
	#####
	dups=Counter(list)
	max_dup=max(dups.values())
	store=max_dup/len(list)
	max_dup_pct=round(store*100,3)
	print()
	print('Largest number of repeated values in dataset is '+str(max_dup))
	print('This represents '+str(max_dup_pct)+'% of the total number of values')
	
def countnums(dataframe,cols):
	#count the number of each digit in the columns in a dataframe
	#then plot the result
	numcount = {'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
	# print(numcount)
	
	for col in cols:
		for i in range(len(dataframe)):
			test = str(dataframe[col][i])
			for item in numcount:
				count = test.count(item)
				numcount[item]=numcount[item]+count
	print(numcount)
	#list the numbers from 9 to 0
	numlist=[]
	nums=[9,8,7,6,5,4,3,2,1,0]
	for num in nums:
		numlist.append(numcount[str(num)])
	
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	ax1.plot(nums,numlist)
	ax1.grid('on')
	plt.show()
	
	
def main():
	
	# import the data from an existing file
	# generate the latest date in the file
	
	#####
	# Change the file name here
	#####
	#windows path:
	# ~ path = 'C:\\Python\\Data\\ES_data_test\\'
	# file_name='all_data_v1.csv'
	file_name='ESH08_12_01_to_03_30.csv'
	
	#mac path:
	# ~ current_working_dir='/Users/Marlowe/gitsite/transfer/trend/data/working_dir/'
	# ~ file_name='ESH08_12_01_to_03_30.csv'
	
	
	df=import_data(path+file_name)

	#print column headings
	# print (*df.columns, sep=', ')
	
	#####
	# Input here the column you wish to study
	#####
	data_list=df['Close'].tolist()
	# print(data_list[:20])
	# plot_hist(data_list)
	# hist_basic(data_list)
	# check_duplicates(data_list)
	
	#####
	# Create list of % change by row and plot histogram
	#####
	
	returns=[]
	for i in range(1,len(data_list)):
		# print(str(set[i][0])+' '+str(set[i][1]))
		returns.append(data_list[i-1]-data_list[i])
	
	# plot_hist(returns)
	# check_duplicates(returns)
	
	#####
	# Check for blank entries
	#####
	# check_nan=np.where(pd.isnull(df))
	# check_blank=np.where(df.applymap(lambda x: x == ''))
	# print(check_blank)
	
	
	#####
	# count all individual numbers in file
	#####
	#columns to check
	# cols=['Date','Time','Open','High','Low','Close']
	cols=['Open','High','Low','Close']
	countnums(df,cols)
	# test = str(df['Open'][13])


	
main()
