'''
This script looks at the TOM effect over a given period and generates the 
expected return, as well as best and worst case and plots the equity curve

The purpose is to compare different start and end dates around tom.

Input: daily OHLC data for desired trading symbol

Output: returns over period and plot of equity


pandas version: 0.18.1
matplotlib version: 3.0.3
mpl_finance version: 0.10.0
numpy version: 1.10.1
scipy version: 0.16.0

python version: 3.5.4

'''

import pandas as pd
import os
import numpy as np
import re
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


#open csv file, return the data in a pandas dataframe
def import_data(file_name,fields):
	#only add items in fields list to dataframe
	
	#only add date, open, high, low, last to dataframe
	# fields = ['Date','Open','High','Low','Close']
	
	#open the file using pandas, use the first row as the header
	data = pd.read_csv(file_name,header=0,usecols=fields)
	
	#change the order to most recent date on top if necessary
	data=data.sort(fields[0],ascending=0)
	data=data.reset_index(drop=True)
	# ~ print(data.head(5))
	
	return data


def slice_df(df,start_date,end_date):
	start_day_df=df.loc[df['Date'] == start_date]
	end_day_df=df.loc[df['Date'] == end_date]
	
	startidx=end_day_df.index[0].tolist()
	endidx=start_day_df.index[0].tolist()
	# print(startidx,endidx)
	# return
	return df[startidx:endidx],startidx,endidx


def start_date_detect(df,index_l,index_h,month):
	#return a list of the index of the first day of the desired month over
	#the given period
	
	index_locations=[]
	for idx in range(index_l+1,index_h-1):
		
		cur_date=df['Date'][idx]
		prev_date=df['Date'][idx+1]
		next_date=df['Date'][idx-1]
		
		# get the month value from the current, previous and next date
		cur_date_mo=re.findall(r'-(.+?)-',cur_date)[0]
		prev_date_mo=re.findall(r'-(.+?)-',prev_date)[0]
		next_date_mo=re.findall(r'-(.+?)-',next_date)[0]
		
		#if current date has month in it and prev date doesnt,append
		
		if cur_date_mo != prev_date_mo:
			if cur_date_mo == month:
				index_locations.append(idx)
			
	return index_locations



def get_returns(df,start_date,end_date,start_day,end_day):
	# this function will generate a list of the returns for each month over the given period (start_date/end_date)
	# with the given start_day and end_day
	#
	# each entry in the list will be the return for each month in % or absolute terms
	
	
	fields = ['Date','Open','High','Low','Close']
	
	#get the low and high index of the dataframe based on the start and end dates
	df_2,idxl,idxh=slice_df(df,start_date,end_date)
	
	
	#create a list of the index of the first trading day of the desired month in each year in the new dataframe
	months=['01','02','03','04','05','06','07','08','09','10','11','12']
	start_points_1=[]
	for mo in months:
		start_points_1.append(start_date_detect(df_2,idxl,idxh,mo))
	# print(start_points)
	
	# create one list with indexes in order
	start_points_2=[item for sublist in start_points_1 for item in sublist]
	start_points=sorted(start_points_2)

	# print(df.loc[[start_points[4]-1]])
	# return
	
	# next adjust those indexes by the start_day factor
	# moving down in index (ex: from 4786 to 4785) increases the date
	# moving up in index decreases date
	# using subtraction to change start date takes into consideration negative start dates
	adj_start_points=[idx-start_day for idx in start_points]
	
	# total number of days held
	
	hold_days=abs(start_day-end_day)
	
	
	#print the start date and end date of analysis
	# ~ for idx in adj_start_points:
		# ~ print('start date: '+df_2['Date'][idx]+', end date: '+df_2['Date'][idx-num_days])
	
	
	
	#get the return, the opening price at the last trading day minus the opening price
	#at the first trading day over the given period.
	abs_returns=[]
	pct_returns=[]
	dates=[]
	for idx in adj_start_points:
		start_val=df_2['Open'][idx]
		end_val=df_2['Open'][idx-hold_days]
		# ~ print('start date: '+df_2['Date'][idx]+', value: '+str(round(start_val,2))+', end date: '+df_2['Date'][idx-num_days]+', value: '+str(round(end_val,2)))
		abs_returns.append(end_val-start_val)
		pct_returns.append(round(100*(end_val-start_val)/start_val,2))
		# Generate list of dates for plotting purposes
		dates.append(df_2['Date'][idx])
	
	#print the start date and returns of analysis
	# ~ for x in range(len(adj_start_points)):
		# ~ print('start date: '+df_2['Date'][adj_start_points[x]]+', end date: '+df_2['Date'][adj_start_points[x]-num_days]+', pct return: '+str(pct_returns[x]))
	
	
	# make list of dates into datetime objects
	date_list_r = [datetime.datetime.strptime(date_item,"%Y-%m-%d").date() for date_item in dates]
	
	# Reverse all lists to go from start date to end date
	# Transpose lists
	date_list_out=date_list_r[::-1]
	pct_returns_out=pct_returns[::-1]
	abs_returns_out=abs_returns[::-1]
	
	return pct_returns_out,abs_returns_out,date_list_out
	
	
	
	
def main():
	#####
	# input main info here
	#####
	
	# Data location for mac:
	# path = '/Users/Marlowe/Marlowe/Securities_Trading/_Ideas/Data/'
	# path = '/Users/Marlowe/gitsite/transfer/'
	
	# Data location for PC:
	path = 'C:\\Python\\transfer\\TOM\\'
	
	# input the names of the fields if they are different from ['Date','Open','High','Low','Close'], use that order
	fields = ['Date','Open','High','Low','Close']
	
	
	#####
	# Input files to analyze
	#####
	
	#input file names of interest
	# file_name='^RUT.csv'
	file_name='^GSPC.csv'
	
	
	in_file= os.path.join(path,file_name)
	
	
	# add a header to the file if no header exists
	#add_header(in_file)
	
	#use csv module to pull out proper data
	#file_noblanks=remove_blanks(in_file)
	
	
	# create dataframe from the data
	df=import_data(in_file,fields)
	
	#####
	# input the date range of interest for overall analysis
	#####
	
	#first date in russell: 1987-09-10
	#first date in GSPC: 1950-01-04
	# start_date='1950-01-04'
	start_date='1987-09-10'
	# start_date='1999-09-10'
	# ~ start_date='2000-09-11'
	
	# end_date='2000-09-11'
	end_date='2019-05-10'
	
	
	# input month start date. 0=first day, 1=second day, -1=day before 1st day, etc
	start_day=-4
	# input end date. 0=first day, 1=second day, -1=day before 1st day, etc
	end_day=1
	
	
	#####
	# generate a list of returns over the desired period
	#####
	
	pct_rtns,abs_rtns,dates=get_returns(df,start_date,end_date,start_day,end_day)
	
	# print(len(dates))
	# ~ print(sc_pct_returns)
	# print(len(pct_rtns))
	# return
	
	
	#####
	# provide statistics on returns
	#####
	'''
	mean_sc_returns=round(np.mean(sc_pct_returns),2)
	std_dev_sc_returns=round(np.std(sc_pct_returns),2)
	
	mean_lc_returns=round(np.mean(lc_pct_returns),2)
	std_dev_lc_returns=round(np.std(lc_pct_returns),2)
	
	win_count=0
	sc_minus_lc_wins=[]
	sc_minus_lc_losses=[]
	for r in range(len(lc_pct_returns)):
		sc_minus_lc=round(sc_pct_returns[r]-lc_pct_returns[r],1)
		if sc_pct_returns[r] > lc_pct_returns[r]:
			win_count=win_count+1
			sc_minus_lc_wins.append(sc_minus_lc)
		if sc_pct_returns[r] <= lc_pct_returns[r]:
			sc_minus_lc_losses.append(sc_minus_lc)
		
	bankroll=10000
	edge=sum(sc_minus_lc_wins)-sum(sc_minus_lc_losses)
	odds=round(win_count/len(sc_pct_returns),1)
	
	print()
	print('Period under consideration: '+start_date+' to '+end_date)
	print('Mean small cap returns: '+str(mean_sc_returns)+', std_dev: '+str(std_dev_sc_returns))
	print('Mean large cap returns: '+str(mean_lc_returns)+', std_dev: '+str(std_dev_lc_returns))
	print('Number of years tested: '+str(len(sc_pct_returns)))
	print()
	print('Number of years sc > lc: '+str(win_count)+', odds of win '+str(odds))
	print('Expected edge: '+str(edge))
	print('Current bankroll: '+str(bankroll)+', bet size: '+str(bankroll*edge/odds))
	'''
	
	#####
	# Look at returns of strategy
	#####
	'''
	worst_case_return=min(pct_rtns)
	mean_return=round(np.mean(pct_rtns),2)
	std_dev_return=round(np.std(pct_rtns),2)
	
	print()
	print('Testing from '+start_date+' to '+end_date)
	print('Purchase on day '+str(start_day)+', sell on day '+str(end_day))
	print('Mean returns: '+str(mean_return)+', std_dev: '+str(std_dev_return)+', worst case return: '+str(worst_case_return))
	print()
	# ~ print(yearly_abs_return)
	
	'''
	#####
	# Plot equity curve
	#####
	
	
	
	#####
	# Plot total returns over the given period for the following time frames:
	# 6mo, 1yr, 2yr, 5yr, 10yr
	# So at each point in time you can see how successful the strategy has been
	# historically in short term and long term durations. The idea is that this is helpful to find out
	# if a strategy is becoming less effective. We can use this to look through historical periods
	# where it has been shown that a given strategy that was once effective has become ineffective.
	# Will this early warning system help us to know when to stop using this strategy?
	#####
	# Total return over a period is defined as the sum of all gains minus all losses in % terms
	
	# Need to start 10yrs after start_date, 120 months
	six_mo_rtns=[]
	one_yr_rtns=[]
	two_yr_rtns=[]
	five_yr_rtns=[]
	ten_yr_rtns=[]
	for idx in range(120,len(pct_rtns)):
		ten_yr_rtns.append(sum(pct_rtns[idx-120:idx]))
		five_yr_rtns.append(sum(pct_rtns[idx-60:idx]))
		two_yr_rtns.append(sum(pct_rtns[idx-24:idx]))
		one_yr_rtns.append(sum(pct_rtns[idx-12:idx]))
		six_mo_rtns.append(sum(pct_rtns[idx-6:idx]))
	
	# print(len(ten_yr_rtns))
	# print(len(six_mo_rtns))
	# print(len(dates[120:]))
	# return
	# Plot returns over dates
	fig = plt.figure()
	ax = plt.subplot()
	
	ax.plot(dates[120:],ten_yr_rtns,color='b',label='6mo Returns')
	ax.plot(dates[120:],five_yr_rtns,color='r',label='1yr Returns')
	ax.plot(dates[120:],two_yr_rtns,color='g',label='2yr Returns')
	ax.plot(dates[120:],one_yr_rtns,color='k',label='5yr Returns')
	ax.plot(dates[120:],six_mo_rtns,color='c',label='10yr Returns')
	
	ax.set_ylabel('Returns')
	ax.set_xlabel('Date')
	
	
	ax.grid()
	plt.legend()
	plt.show()

	
	
	return

main()
