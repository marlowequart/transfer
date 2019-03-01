'''
Use this script to generate desired price data from the csv file.


'''

import pandas as pd
import os
import numpy as np
# import csv


#open csv file, return the data in a pandas dataframe
def import_data(file_name):
	#open the file using pandas, use the first row as the header
	data = pd.read_csv(file_name,header=0)
	
	return data
	
def day_stats(df,time):
	#output the open, close and volume for given time on given day.
	
	# ~ a_list=df.loc[[16769]].values.tolist()
	# ~ print(a_list[0])
	
	
	#get the data
	row_idx_list = df.index[df['Time'] == time].tolist()
	row_idx = max(row_idx_list)
	row = df.loc[[row_idx]].values.tolist()
	#save open
	open = row[0][4]
	#save close
	close = row[0][7]
	#save volume
	volume = row[0][2]
	
	return open,close,volume



def main():
	#####
	# input the file name and info here
	#####
	
	# Data location for mac:
	# ~ path = '/Users/Marlowe/Marlowe/Securities_Trading/Trading_Ideas/Data/ES_Data/'
	# ~ file_name='ES_full_dec_2007_to_nov_2018.csv'
	# ~ file_name='ESZ18_06_13_to_11_13.csv'
	# ~ file_full= os.path.join(path,file_name)
	
	# ~ df=import_data(file_full)
	# ~ print(df.head())
	# ~ return
	
	# Data location for windows:
	path = 'C:\\Users\\quartm\\Desktop\\Archive\\'
	
	in_file_name1='18ESU_05_01_to_09_30.csv'
	in_file_name2='18ESM_03_01_to_06_30.csv'
	out_file_name='18ESU_05_01_to_09_30.csv'
	
	in_file1= os.path.join(path,in_file_name1)
	in_file2= os.path.join(path,in_file_name2)
	out_file= os.path.join(path,out_file_name)
	
	
	# df_1=import_data(file_full)
	# print('num rows in df = '+str(df_1.shape[0]))
	# remove NAN rows
	# check_nan=np.where(pd.isnull(df_1))
	# df=df_1.drop(df_1.index[[check_nan[0][0]]])
	
	
	in_df1=import_data(in_file1)
	in_df2=import_data(in_file2)
	out_df1=import_data(out_file)
	
	
	
	#####
	# return data compare for a single date here
	#####
	
	# Full day starts at 18:01:00 of previous day and ends at 17:00:00 of current day
	#open_time='18:01:00'
	#close_time='17:00:00'
	#today = '2018-10-24'
	#yesterday = '2018-10-23'
	
	date = '2018-06-15'
	time = '09:10:00'
	
	# cash session starts at 09:30:00 ends at 16:00:00
	# ~ open_time='09:30:00'
	# ~ close_time='16:00:00'
	# ~ today = '2018-10-24'
	
	cur_day_df_in1 = in_df1.loc[in_df1['Date'] == date]
	cur_day_df_in2 = in_df2.loc[in_df2['Date'] == date]
	cur_day_df_out = out_df1.loc[out_df1['Date'] == date]
	
	# return the open, close, volume
	# ~ daily_stats(current_day_df,open_time,close_time)
	# ~ return
	#day_stats(cur_day_df_in1,time)
	#return
	open_in1,close_in1,vol_in1 = day_stats(cur_day_df_in1,time)
	open_in2,close_in2,vol_in2 = day_stats(cur_day_df_in2,time)
	open_out,close_out,vol_out = day_stats(cur_day_df_out,time)
	
	
	print('\n')
	print('Todays date: '+date+', Time: '+time)
	print(in_file_name1+': Volume:'+str(vol_in1)+' Open:'+str(open_in1)+' Close:'+str(close_in1))
	print(in_file_name2+': Volume:'+str(vol_in2)+' Open:'+str(open_in2)+' Close:'+str(close_in2))
	print(out_file_name+': Volume:'+str(vol_out)+' Open:'+str(open_out)+' Close:'+str(close_out))
	print('\n')
	

main()