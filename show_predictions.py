'''
Created on Oct 2, 2019

@author: rjhumphrey

Show Targets uses an algorithm to determine targets for a
limited range and number of points, depending upon granularity
then uses the plotter to show buy and sell spots
'''

from data_loader import DataLoader
#from filedata_reader import FileDataReader
from plotter import Plotter
import datetime
from datetime import timedelta
import pandas as pd
from model import Model

if __name__ == '__main__':
    '''
    Read in the Historical data and show prediction (y)
    returned from NN training
    '''
    
    print ('Show predictions for a time range')
    
    ticker = 'BTC-USD'
    start_time_str = '2019-09-30 00:00:00.000000'
    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')

    
    live_data = False
    do_trade = False
    all_data = DataLoader(ticker, start_time, live_data, do_trade)

    # all_data is read in as minute BTC OHLCV
    # starts at 20150801 00:00:00 to close to real time 
    # run data gatherer to get data from eof till now-5H

    # get 6 months at a time
    #granularity = 21600 # in seconds; 86400 = 1 Day
    #num_points = 728 #728 = 6 mos, w 6H int
    
    granularity = 300 # in seconds; 86400 = 1 Day
    num_points = 160000 # try to make it 180 days
    
    duration = granularity * num_points
    end_time = start_time + timedelta(seconds=duration)
    
    range_df = all_data.getHistoryRange(start_time, end_time, granularity)

    print ('num points returned:', len(range_df))

    # add time as a column outside of the index for the plotter
    #print (range_df.head(20))
    
    print ('nan count:', range_df.isna().sum())
    
    #plot = Plotter.showOHLCPlot(range_df)

    target_df = pd.DataFrame(index = range_df.index)
    target_df['target'] = 0
    
    last_time = range_df.index[-1]
    print ('last time is:', last_time)

    skip_to = range_df.index[0]
    print ('starting at:', skip_to)

    compound_gain = 1
    num_sales = 0
    gain_sum = 0
    
    '''

    model = Model(all_data)
    model.fit()

    # iterate (I know!) over the range, getting future slices and creating a new df with targets
    for row in range_df.itertuples(index=True):
        #print (getattr(row, "Index"), getattr(row, "high"))    
        time = getattr(row,"Index")
        open_price = getattr(row,"open")

        all_data.virtual_time = time

        prediction = model.predict()[0]

        # set targets and skip to sell point
        target_df.at[time, 'target'] = prediction
    
    #print (target_df.tail(10))
       
    '''
    
    # then merge target and range_df
    #new_df = pd.concat([range_df,target_df], axis=1)
    new_df = range_df
    
    print ('new_df:', new_df.tail(20))

    plot2 = Plotter.showSinglePlot(new_df)
    
    #output_file = file = r'../data/coinbase_BTC_targets.csv'
        
    #FileDataReader.write_to_csv(new_df, output_file)
