'''
Created on Oct 8, 2019

@author: rjhumphrey
'''


#import datetime
#import pandas as pd

from sklearn import svm
import pandas as pd
import collections
from sklearn.svm import SVC
from sklearn.utils import resample
#from datetime import timedelta
#from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from filedata_reader import FileDataReader
#from data_loader import DataLoader

if __name__ == '__main__':
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
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
    
    # we need to undersample the majority class (0) 
    # merge the datasets
    # concatenate our training data back together
    merged_df = pd.concat([X_train, y_train], ignore_index=True, axis=1)
    
    print (merged_df.shape)
    
    do_nothing = merged_df[merged_df[450]==0]
    buys = merged_df[merged_df[450]==1]
    sells = merged_df[merged_df[450]==2]
    
    print (do_nothing.shape)
    print (buys.shape)
    print (sells.shape)
    
    do_nothing_downsampled = resample(do_nothing,
                                    replace = False,
                                    n_samples = 600,
                                    random_state = 13)
    
    # recombine
    
    downsampled = pd.concat([do_nothing_downsampled, buys, sells])
    
    print (downsampled.shape)
    
    y_train = downsampled.iloc[:,-1]
    X_train = downsampled.drop(downsampled.columns[-1], axis = 1)
    
    print (y_train.shape)
    print (X_train.shape)
    
    y_train = y_train.values.ravel()
    y_test = y_test.values.ravel()
    
    svclassifier = SVC(kernel='rbf')
    svclassifier.fit(X_train, y_train)
    
    y_pred = svclassifier.predict(X_test)
    
    print (collections.Counter(y_pred))
    
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    