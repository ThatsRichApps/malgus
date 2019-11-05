'''
Created on Oct 16, 2019

@author: rjhumphrey
'''

import pandas as pd
import collections
#import datetime
#import time

from sklearn.svm import SVC
from sklearn.utils import resample
#from datetime import timedelta
#from sklearn.preprocessing import StandardScaler
#from sklearn.model_selection import train_test_split
#from sklearn.metrics import classification_report, confusion_matrix

from filedata_reader import FileDataReader

class Model(object):
    '''
    classdocs
    '''


    def __init__(self, data):
        '''
        Constructor
        '''
        self.data = data

        # set the ML model here:
        self.classifier = SVC(kernel='rbf')
    
    def fit(self):
        '''
        Use features data file to fit all the data to this model
        '''
        features_file = r'../data/20151031-20190930_Features_150_3.csv'
        X = FileDataReader.getFeatures(features_file)
        
        #X.dropna(axis = 0, how ='any', inplace=True) 
        
        #print ('features:', X.shape)
        
        #print (X.head())
        #print (X.tail())
        
        #print ('nan count:', X.isna().sum())
    
        target_file = r'../data/20151031-20190930_Targets.csv'
        
        y = FileDataReader.getTargets(target_file)
        
        #print ('targets', y.shape)
        #print (collections.Counter(y))
        
        #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
        # train on the whole dataset
        X_train = X
        y_train = y
        
        # we need to undersample the majority class (0) 
        # merge the datasets
        # concatenate our training data back together
        merged_df = pd.concat([X_train, y_train], ignore_index=True, axis=1)
        
        #print (merged_df.shape)
        
        do_nothing = merged_df[merged_df[450]==0]
        buys = merged_df[merged_df[450]==1]
        sells = merged_df[merged_df[450]==2]
        
        #print ('0:', do_nothing.shape)
        #print ('1:', buys.shape)
        #print ('2:', sells.shape)
        
        do_nothing_downsampled = resample(do_nothing,
                                        replace = False,
                                        n_samples = 1200,
                                        random_state = 13)
        
        # recombine
        
        downsampled = pd.concat([do_nothing_downsampled, buys, sells])
        
        #print (downsampled.shape)
        
        y_train = downsampled.iloc[:,-1]
        X_train = downsampled.drop(downsampled.columns[-1], axis = 1)
        
        #print (y_train.shape)
        #print (X_train.shape)
        
        y_train = y_train.values.ravel()
        
        self.classifier.fit(X_train, y_train)
    
    def predict(self):
        '''
        After fitting the training data to the model, give a
        prediction for current time or virtual time
        '''
        #print ('Get features for', self.data.virtual_time)
        
        # testing - input value to test
        '''
        test_prediction = int (input("Input prediction to test:"))
        if (test_prediction != -1):
            y_pred = []
            y_pred.append(test_prediction)
            print ('returning', test_prediction)
            return (y_pred)
        '''
        
        current_sample = self.data.getFeatures()
        
        #print ('current sample:', current_sample.shape)
        
        current_sample = current_sample.reshape(1, -1)
    
        #print ('after reshape:', current_sample.shape)
        
        y_pred = self.classifier.predict(current_sample)    
                
        #print ('current prediction:', y_pred)
        
        return (y_pred)
