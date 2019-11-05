'''
Created on Oct 7, 2019

@author: rjhumphrey
'''

from filedata_reader import FileDataReader
#from sklearn import svm
from data_loader import DataLoader
import datetime
from datetime import timedelta
import pandas as pd
from sklearn.preprocessing import StandardScaler

if __name__ == '__main__':
    
    file = r'../data/coinbase_BTC_targets.csv'
    file_data = FileDataReader(file)
    
    # file_data.data contains hourly OHLC data and 
    # target 0 - nothing, 1 - buy, 2 - sell
    
    # create a model and train
    #print (file_data.data.shape)
    
    hour_data = file_data.data
    
    # drop hour and target data before 02/01/2016?
    
    
    targets = hour_data.iloc[ :, -1:].copy()
    targets.reset_index(drop = True, inplace = True)
    
    print ('targets shape', targets.shape)
    #print (targets.tail())
    
    ticker = 'BTC-USD'
    start_time_str = '2015-08-01 00:00:00.000000'
    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')

    last_time_str = '2019-09-30 23:59:00.000000'
    last_time = datetime.datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S.%f')

    live_data = False
    all_data = DataLoader(ticker, start_time, live_data)
    
    # drop before and after range
    #hour_data = hour_data[start_time:]
    #hour_data = hour_data[:last_time]


    # I just want hour data features

    #features_df = pd.DataFrame(index = hour_data.index)
    features_df = pd.DataFrame()
    
    # I don't see a way to do this without a loop
    # for each time in the targets file, get a set # of past datapoints at varying granularity (same # points)
    # and add those as features to the time, standardize the interval and standardize current time price

    
    # Start with 100 points of 1H data
    # iterate (I know!) over the range, getting history data and transform into features
    
    count = 0
    
    for row in hour_data.itertuples(index=True):
        
        #print (getattr(row, "Index"), getattr(row, 'open'))    
        
        time = getattr(row,"Index")
        #open_price = getattr(row,"open")
        
        # reomoved time here, will it work?
        features = all_data.getFeatures()

        feature_series = pd.Series(features)
        feature_series.name = time
        
        features_df = features_df.append(feature_series)
       
        '''
        if (count > 1000):   
            break
        
        count +=1
        '''
        
    print ('features_df shape:', features_df.shape)
    print (features_df.head())
        
    output_file = r'../data/20151031-20190930_Features_150_3.csv'
        
    FileDataReader.write_to_csv(features_df, output_file)

    output_file = r'../data/20151031-20190930_Targets.csv'
        
    FileDataReader.write_to_csv(targets, output_file)
    
