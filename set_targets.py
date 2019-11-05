'''
Created on Oct 2, 2019

@author: rjhumphrey
'''

from data_loader import DataLoader
from filedata_reader import FileDataReader
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
    start_time_str = '2015-10-31 00:00:00.000000'
    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')

    last_time_str = '2019-09-30 23:59:00.000000'
    last_time = datetime.datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S.%f')

    live_data = False
    all_data = DataLoader(ticker, start_time, live_data)

    # all_data is read in as minute BTC OHLCV
    # starts at 20150801 00:00:00 to close to real time 
    # run data gatherer to get data from eof till now-5H

    # drop before and after range
    all_data.file_data.data = all_data.file_data.data[start_time:]
    all_data.file_data.data = all_data.file_data.data[:last_time]

    #print (all_data.file_data.data.head())
    #print (all_data.file_data.data.tail())

    print ('num points returned:', len(all_data.file_data.data))
    print ('nan count:', all_data.file_data.data.isna().sum())
    
    # bad data points
    all_data.file_data.data.drop('2017-04-15 23:02:00', inplace = True)
    all_data.file_data.data.drop('2017-04-15 23:03:00', inplace = True)
    all_data.file_data.data.drop('2017-04-15 23:04:00', inplace = True)
    
    #print (all_data.file_data.data['2017-04-15 19:00:00':'2017-04-15 23:30:00'])
    
    # get all data at 1 hour frequency
    granularity = 3600 # in seconds; 86400 = 1 Day
    num_points = 34320 # 
    
    duration = granularity * num_points
    end_time = start_time + timedelta(seconds=duration)
    
    range_df = all_data.getHistoryRange(start_time, end_time, granularity)

    print ('num points returned:', len(range_df))

    # add time as a column outside of the index for the plotter
    #print (range_df['2018-08-09 22:00:00':'2018-08-10 20:00:00'])
    
    #range_df.fillna(method='ffill', inplace = True)
    
    # now find zeros and ffill
    range_df['open'].replace(to_replace=0, method='ffill', inplace = True)
    range_df['high'].replace(to_replace=0, method='ffill', inplace = True)
    range_df['low'].replace(to_replace=0, method='ffill', inplace = True)
    range_df['close'].replace(to_replace=0, method='ffill', inplace = True)
    range_df['volume'].replace(to_replace=0, method='ffill', inplace = True)
    
    #print (range_df[(range_df['open']) < 300])
    
    #range_df.loc['2017-04-15 23:00:00']
    
    #print (range_df['2017-04-15 19:00:00':'2017-04-16 03:00:00'])
    
    #print ('nan count:', range_df.isna().sum())

    #print ('nan list:', range_df.loc[pd.isnull(range_df).any(1), :])
   
    #plot = Plotter.showOHLCPlot(range_df)
    
    # create a target dataframe and initialize all values to 0 (do nothing)
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
            #print ('buy on:', time, 'at', open_price)
            #print ('sell on:', highest, 'at', max_high)

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
            
    
    print (target_df.tail(10))
    
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

    #plot2 = Plotter.showSinglePlot(new_df)
    
    output_file = r'../data/coinbase_BTC_targets.csv'
        
    FileDataReader.write_to_csv(new_df, output_file)
