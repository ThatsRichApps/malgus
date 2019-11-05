'''
Created on Sep 23, 2019

@author: rich
'''

import time
from datetime import datetime
from datetime import timedelta
from filedata_reader import FileDataReader
from data_loader import DataLoader
import pandas as pd

if __name__ == '__main__':
    '''
    Read in data from main data file, transform columns
    merge with 2019 data file, save as new csv 
    '''

    file = r'../../../../config/coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv'
    
    history = FileDataReader(file)
    
    # make the time the index
    history.data['time'] = pd.to_datetime(history.data['Timestamp'], unit='s')
    #history.data['time'] = pd.to_datetime(history.data['time'])
    
    history.data.set_index('time', inplace=True)
            
    history.data.drop(['Timestamp'], axis = 1, inplace = True)
    
    history.data.drop(['Volume_(Currency)'], axis = 1, inplace = True)
    
    history.data.drop(['Weighted_Price'], axis = 1, inplace = True)
    
    history.data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume_(BTC)': 'volume'}, inplace=True)
    
    #print (history.data.tail())
    
    newfile = r'../logs/2019_data_all.csv'
    
    newdata = FileDataReader(newfile)

    # make the time the index
    newdata.data['time'] = pd.to_datetime(newdata.data['time'])
    
    newdata.data.set_index('time', inplace=True)
    
    #drop the extra 22:06 data
    newdata.data.drop('2019-01-07 22:06:00', inplace=True)
    
    #print (newdata.data.head())
        
    all_data = history.data.append(newdata.data)
        
    #print (all_data.loc['2019-01-07 22:02:00':'2019-01-07 22:11:00'])
    print (all_data.shape)
    
    all_data = all_data.truncate(before = '2015-08-01 00:00:00')
    
    print (all_data.isna().sum())
    
    #all_data.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
    
    print (all_data.shape)

    #print (all_data.head())
    
    #print (all_data.tail())

    all_data_file = r'../logs/coinbase_BTC_cleaned_201508-201909_w_nan.csv'

    history.write_to_csv(all_data, all_data_file)

