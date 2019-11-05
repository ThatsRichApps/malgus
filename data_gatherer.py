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
from collections import OrderedDict

if __name__ == '__main__':
    '''
    Gather the data from the end of the datafile until current time
    and then update the current data file
    '''
    
    data_file = r'../data/coinbase_BTC_master.csv'
    
    filedata = FileDataReader(data_file)
    
    filedata.data = filedata.data.resample('60S').agg(
                OrderedDict([
                    ('open', 'first'),
                    ('high', 'max'),
                    ('low', 'min'),
                    ('close', 'last'),
                    ('volume', 'sum'),
                    ])
            ).ffill()
    
    
    
    #print (filedata.data.index[-1])
    
    lastdate = filedata.data.index[-1]
    
    print ('get data from',  lastdate, 'to 300 minutes ago')
    
    #print ('exiting before actual dataload')
    #exit()
    
    # make the start the next minute
    lastdate = lastdate + timedelta(seconds=60)
    
    # get current time minus 300 secs
    timenow = datetime.now() - timedelta(seconds=(60*300))
    
    # create a data loader to get historical data    
    ticker = 'BTC-USD'
    live_data = True
    do_trade = False
    data = DataLoader(ticker, lastdate, live_data, do_trade)
    
    missing_data = pd.DataFrame(data.getFuture())
    
    # how add 300 secs to the data virtual time
    data.virtual_time += timedelta(seconds=(60*300))
    
    
    # use counter for testing a few rounds
    counter = 0
    
    # until virtual time is 300 mins from current time
    # get 300 point blocks ahead of virtual time (getFuture()) 
    # and add it to the existing dataframe
    
    while (data.virtual_time < timenow):
    
        #print ('get 300 min points from:', data.virtual_time)
    
        future_df = data.getFuture()
    
        missing_data = missing_data.append(future_df)
        
        #print (missing_data.shape)
    
        data.virtual_time += timedelta(seconds=(60*300))
    
        # don't overload the coinbase server
        time.sleep(5)
        
        # use counter for testing
        #counter += 1
        #if (counter > 1):
        #    break
        
        
    # now get the last amount of data less than 300 mins (5 hours) away?
     
    all_data = filedata.data.append(missing_data)
    
    newfile = r'../data/coinbase_BTC_master.csv'
    
    filedata.write_to_csv(all_data, newfile)

    print (missing_data.head(1))
    print (missing_data.tail(1))
    