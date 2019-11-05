'''
Created on Sep 19, 2019

@author: rich
'''

from os import path
import pandas as pd

class FileDataReader(object):
    '''
    FileDataReader
    
    reads and writes data to a csv file and 
    does any required formatting to put into a dataframe
    with a minute frequency time index and features: open, close, high, low, volume

    '''

    def __init__(self, file):
        '''
        Create a FileDataLoader instance by reading the given file
        and putting data in self.data
        
        '''
        #file = '../../../../config/coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv'
        
        #file = '../logs/2019_data_all.csv'
                
        if path.exists(file):
        
            self.data = pd.read_csv(file)
            
            # and index on datetime
            self.data['time'] = pd.to_datetime(self.data['time'])
            self.data.set_index('time', inplace=True)
            
        else:
            
            print ("file not found")
            
            
    @staticmethod
    def write_to_csv(df_to_write, filename):
        '''
        Wrapper to write a dataframe to a file
        '''
        #timenow = datetime.datetime.now()
        #filename = r'../logs/2019_data_all.csv'

        if path.exists(filename):
            print ("file exists, overwriting")
        
        df_to_write.to_csv(filename)
        
        '''
        if not path.exists(filename):
            export_csv = df_to_write.to_csv(filename)
            print (export_csv)
        else:
            print ("file already exists")
            return(False)
        '''
        
    @staticmethod
    def getFeatures(file):
        '''
        Get the features data from a file
        
        '''
        
        if path.exists(file):
        
            data = pd.read_csv(file)
            
            # add index on datetime
            #data['time'] = pd.to_datetime(data[data.columns[0]])
            #data.set_index('time', inplace=True)
            
            data.drop(data.columns[0], inplace=True, axis=1)
            data.reset_index(drop=True, inplace=True)
         
        else:
            
            print ("file not found")

        return (data)
    
    @staticmethod
    def getTargets(file):
        '''
        Targets should be in a file with just a classifier of 0,1,2
        '''
        
        
        if path.exists(file):
        
            data = pd.read_csv(file, index_col=0)
            #data.reset_index(drop=True, inplace=True)
            
        else:
            
            print (file, "not found")
        
        return (data)
        
        
if __name__ == '__main__':
    
    file = r'../data/coinbase_BTC_master.csv'
            
    data_reader = FileDataReader(file)
    
    print ('data shape:', data_reader.data.shape)
    
    print (data_reader.data.tail())
    