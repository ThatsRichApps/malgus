'''
Created on Sep 24, 2019

@author: rich
'''

from data_loader import DataLoader
import datetime
from datetime import timedelta
from filedata_reader import FileDataReader

if __name__ == '__main__':
    
    # get hostory and future data from coinbase at starttime    
    ticker = 'BTC-USD'
    start_time_str = '2018-10-31 00:00:00.000000'
    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
    livetrade = False
    data = DataLoader(ticker, start_time, livetrade)
    
    end_time_str = '2018-10-31 04:30:00.000000'
    end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S.%f')
    granularity = 60
    
    history_df = data.getHistoryRange(start_time, end_time, granularity)
    
    print ('history', history_df.tail())
    
    filedata = FileDataReader()
    
    print (filedata.data.loc['2018-10-31'].head())
