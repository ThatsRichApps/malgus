'''
Created on Oct 8, 2019

@author: rjhumphrey
'''


#import datetime
#import pandas as pd

from sklearn import svm
import pandas as pd
import collections
import datetime
import time

from sklearn.svm import SVC
from sklearn.utils import resample
#from datetime import timedelta
#from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from filedata_reader import FileDataReader
from data_loader import DataLoader

if __name__ == '__main__':
    
    # Create a dataloader for getting current price and
    # features at current time (or virtual time
    ticker = 'BTC-USD'
    virtual_time_str = '2018-12-21 21:00:00.000000'
    virtual_time = datetime.datetime.strptime(virtual_time_str, '%Y-%m-%d %H:%M:%S.%f')

    live_data = True
    do_trade = False
    all_data = DataLoader(ticker, virtual_time, live_data, do_trade)
    
    features_file = r'../data/20151031-20190930_Features_150_3.csv'
    X = FileDataReader.getFeatures(features_file)
    
    #X.dropna(axis = 0, how ='any', inplace=True) 
    
    print ('features:', X.shape)
    
    #print (X.head())
    #print (X.tail())
    
    #print ('nan count:', X.isna().sum())

    target_file = r'../data/20151031-20190930_Targets_Test.csv'
    
    y = FileDataReader.getTargets(target_file)
    
    print ('targets', y.shape)
    print (collections.Counter(y))
    
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
    # train on the whole dataset
    X_train = X
    y_train = y
    
    # we need to undersample the majority class (0) 
    # merge the datasets
    # concatenate our training data back together
    merged_df = pd.concat([X_train, y_train], ignore_index=True, axis=1)
    
    print (merged_df.shape)
    
    do_nothing = merged_df[merged_df[450]==0]
    buys = merged_df[merged_df[450]==1]
    sells = merged_df[merged_df[450]==2]
    
    print ('0:', do_nothing.shape)
    print ('1:', buys.shape)
    print ('2:', sells.shape)
    
    do_nothing_downsampled = resample(do_nothing,
                                    replace = False,
                                    n_samples = 800,
                                    random_state = 13)
    
    # recombine
    
    downsampled = pd.concat([do_nothing_downsampled, buys, sells])
    
    print (downsampled.shape)
    
    y_train = downsampled.iloc[:,-1]
    X_train = downsampled.drop(downsampled.columns[-1], axis = 1)
    
    print (y_train.shape)
    print (X_train.shape)
    
    y_train = y_train.values.ravel()
    
    svclassifier = SVC(kernel='rbf')
    svclassifier.fit(X_train, y_train)    
    
    loop = True
    
    while (loop):
    
        price = all_data.getTimePrice()
        print ('current price:', price)
        print ('start time is:', all_data.virtual_time)
    
        current_sample = all_data.getFeatures()
        
        print ('current sample:', current_sample.shape)
        
        current_sample = current_sample.reshape(1, -1)
    
        print ('after reshape:', current_sample.shape)
        
        y_pred = svclassifier.predict(current_sample)    
        
        #y_pred = svclassifier.predict(X_test)
        
        print ('current prediction:', y_pred)
        
        if (y_pred[0] == 2):
            print ('SELL!!!!!!')
            loop = False
        else:
            time.sleep(300)
        
        