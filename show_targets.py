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

if __name__ == '__main__':
    '''
    Read in the Historical data and set buy and sell targets (y)
    to be used for NN training
    Save in new file
    '''
    
    print ('Set buy and sell targets, save to file')
    
    ticker = 'BTC-USD'
    start_time_str = '2018-10-31 00:00:00.000000'
    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')

    last_time_str = '2019-09-30 23:59:00.000000'
    last_time = datetime.datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S.%f')

    live_data = False
    do_trade = False
    all_data = DataLoader(ticker, start_time, live_data, do_trade)

    # all_data is read in as minute BTC OHLCV
    # starts at 20150801 00:00:00 to close to real time 
    # run data gatherer to get data from eof till now-5H

    # drop before and after range
    all_data.file_data.data = all_data.file_data.data[start_time:]
    all_data.file_data.data = all_data.file_data.data[:last_time]

    #print (all_data.file_data.data.head())
    #print (all_data.file_data.data.tail())

    # get 6 months at a time
    #granularity = 21600 # in seconds; 86400 = 1 Day
    #num_points = 728 #728 = 6 mos, w 6H int
    
    granularity = 3600 # in seconds; 86400 = 1 Day
    num_points = 4320 # try to make it 180 days
    
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

    # iterate (I know!) over the range, getting future slices and creating a new df with targets
    for row in range_df.itertuples(index=True):
        #print (getattr(row, "Index"), getattr(row, "high"))    
        time = getattr(row,"Index")
        open_price = getattr(row,"open")

        if (time < skip_to):
            continue

        # get future at same interval 4/day at 6H
        num_points = 28 # 7 days?
        
        duration = granularity * num_points
        end_time = time + timedelta(seconds=duration)
        
        # stop when the end of interval is at last point
        if (end_time > last_time):
            break
        
        future_df = all_data.getHistoryRange(time, end_time, granularity)

        # get the index of the maximum high in the future
        highest_series = future_df.idxmax()
        highest = highest_series['open']
        max_high = future_df.loc[highest]['open']
        
        #print ('next highest:', highest, 'is', max_high)
        
        max_percent = ((max_high - open_price) / open_price) * 100
                
        if (max_percent > 4.0):
            print ('buy,', time, ',', open_price)
            print ('sell,', highest, ',', max_high)

            # check to see if there's a lower low between time and high
            min_series = future_df[time:highest].idxmin()
            lowest = min_series['open']
            low_price = future_df.loc[lowest]['open']

            # set targets and skip to sell point
            target_df.at[lowest, 'target'] = 1
            target_df.at[highest, 'target'] = 2
            skip_to = highest + timedelta(seconds = granularity)
            
            # calculate stats for gain and num trades
            gain = ((max_high-low_price)/low_price)
            print ('gain,', gain)
            compound_gain = (1+gain) * compound_gain
            gain_sum = gain_sum + gain
            num_sales += 1
            
    
    #print (target_df.tail(10))
    
    print ('num sales:', num_sales)
    print ('compound_gain', compound_gain)
    print ('average gain', (gain_sum / num_sales))
    
    # then merge target and range_df
    new_df = pd.concat([range_df,target_df], axis=1)
    
    '''
    base_price = new_df['open'].iloc[0]

    # normalize open price by base price
    new_df['open'] = ((new_df['open'] - base_price) / base_price) * 100

    print ('base price is:', base_price)
    
    new_df['target'] = 0
    
    '''
    
    #print ('new_df:', new_df.tail(20))

    plot2 = Plotter.showSinglePlot(new_df)
    
    #output_file = file = r'../data/coinbase_BTC_targets.csv'
        
    #FileDataReader.write_to_csv(new_df, output_file)
