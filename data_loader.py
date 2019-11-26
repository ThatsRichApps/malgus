'''
Created on Sep 3, 2019

@author: rich
'''

import cbpro
import numpy as np
import time
import datetime
import pandas as pd

from datetime import timedelta
from collections import OrderedDict
from sklearn.preprocessing import StandardScaler

from config_reader import Login
from filedata_reader import FileDataReader


class DataLoader(object):
    '''
    Class DataLoader
    
    Use to either load the data from a file or get it live.
    
    '''
    
    def __init__(self, ticker, time, live_data, do_trade):
        '''
        Constructor
        '''
        #self.GRANULARITY = (60,300,900,3600, 21600, 86400)
        self.GRANULARITY = [60]
        
        self.ticker = ticker
        self.live_data = live_data
        self.do_trade = do_trade
        
        # self.future_df = self.getFuture()
        # inialize future as empty dataframe but we might not need it
        self.future_df = pd.DataFrame()

        # we need to connect even if data is not live
        self.login = Login()
        self.trade_client = cbpro.AuthenticatedClient(self.login.key, self.login.b64secret, self.login.passphrase)
            
        if (live_data):
            
            self.virtual_time = datetime.datetime.utcnow().replace(microsecond=0,second=0)
        
        else:
        
            self.virtual_time = time
            # data is not live, get from file
            file = r'../data/coinbase_BTC_master.csv'
            self.file_data = FileDataReader(file)
                
    def getHistoryRange(self, start, end, granularity):
        '''
        getHistoryRange(self, start, end, granularity)

        For a given granularity in secs, start, and end, 
        return a dataframe with the requested frequency
        
        '''
        #print ("get history from start", start)
        #print ("to end", end)
        
        #check that start and end don't comprise more than 300 points at this granularity
        
        if (self.live_data):
        
            history = self.trade_client.get_product_historic_rates(self.ticker, start, end, granularity=granularity)
            
            history_df = pd.DataFrame.from_records(history,  columns = ['time', 'low', 'high', 'open', 'close', 'volume'])
    
            history_df['time'] = pd.to_datetime(history_df['time'], unit='s')
    
            history_df.set_index('time', inplace = True)
    
        else:
            
            #history_df = self.file_data.data[start:end].copy()
            history_df = self.file_data.data[start:end]
    
            resample_rate = str(granularity) + "S"

            history_df = history_df.resample(resample_rate).agg(
                OrderedDict([
                    ('open', 'first'),
                    ('high', 'max'),
                    ('low', 'min'),
                    ('close', 'last'),
                    ('volume', 'sum'),
                    ])
            ).ffill()
    
        
        #if history['message']:
        #    print ("error message:", history['message'])
    
        # Granularity Options are 60, 300, 900, 3600, 21600, 86400
        # Corresponding to: 1M, 5M, 15M, 1H, 6H, 1D
    
        #print ("history_df head:\n", history_df.head(5))
    
        return (history_df)
        

    def getHistoryRangeClose(self, start, end, granularity, num_points):
        '''
        getHistoryRangeClose(self, start, end, granularity)

        Just returns close value and not all

        For a given granularity in secs, start, and end, 
        return a dataframe with the requested frequency
        
        '''
        #print ("get history from start", start)
        #print ("to end", end)
        
        #check that start and end don't comprise more than 300 points at this granularity
        
        if (self.live_data):
    
            #pad = granularity * 1
            #start_pad = start - timedelta(seconds=pad)
            
            # need a try catch block here with delay retry
            try:
                history = self.trade_client.get_product_historic_rates(self.ticker, start, end, granularity=granularity)
            except:
                # now what?  retry or reconnect?
                print ('error with trade client, sleep 300s and try to reconnect')
                time.sleep(300)
                self.trade_client = cbpro.AuthenticatedClient(self.login.key, self.login.b64secret, self.login.passphrase)
                history = self.trade_client.get_product_historic_rates(self.ticker, start, end, granularity=granularity)
            
            history_df = pd.DataFrame.from_records(history,  columns = ['time', 'low', 'high', 'open', 'close', 'volume'])
    
            history_df['time'] = pd.to_datetime(history_df['time'], unit='s')
    
            history_df.set_index('time', inplace = True)
            
            resample_rate = str(granularity) + "S"

            history_df = history_df.resample(resample_rate).agg(
                OrderedDict([
                    ('open', 'first'),
                    ('high', 'max'),
                    ('low', 'min'),
                    ('close', 'last'),
                    ('volume', 'sum'),
                    ])
            ).ffill()

    
        else:
            
            #history_df = self.file_data.data[start:end].copy()
            
            # pad start and end value so that we can get agg of range
            pad = granularity * 3
            start_pad = start - timedelta(seconds=pad)
            history_df = self.file_data.data[start_pad:end].copy()
            
            #history_df = self.file_data.data[start:end].copy()
            
            #print ('history range:', history_df.shape)
    
            resample_rate = str(granularity) + "S"

            history_df = history_df.resample(resample_rate).agg(
                OrderedDict([
                    ('open', 'first'),
                    ('high', 'max'),
                    ('low', 'min'),
                    ('close', 'last'),
                    ('volume', 'sum'),
                    ])
            ).ffill()
            
        #print ('slicing from', start, 'to', end)
        #print ('history range:', history_df.shape)
        history_df = history_df.tail(num_points)
        
        history_df.drop(['open', 'high', 'low', 'volume'], axis=1, inplace=True)
        #if history['message']:
        #    print ("error message:", history['message'])
    
        # Granularity Options are 60, 300, 900, 3600, 21600, 86400
        # Corresponding to: 1M, 5M, 15M, 1H, 6H, 1D
    
        #print ("history_df head:\n", history_df.head(5))
    
        return (history_df)

    
    def getAllHistory(self, end_time):
        
        history_matrix = {}
            
        
        for gran in self.GRANULARITY:
        
            duration = gran * 300
            #print ("granularity:", gran)
            #print ("seconds:", duration)
            
            #print ("end_time:", end_time)
            
            start_time = end_time - timedelta(seconds=duration)
            
            #print ("start_time:", start_time)
            
            history_matrix[gran] = self.getHistoryRange(start_time, end_time, gran)
        
            # wait a few seconds to not overload the API
            time.sleep(10)
        

        return history_matrix

    def getAccountInfo(self):
        # get some account info:
        accts = self.trade_client.get_accounts()
        coin = self.ticker[0:3]

        if 'message' in accts:
            print (accts['message'], ": quitting")
            #quit()
        
        print ("accts:", accts)
        
        if 'currency' in accts:
            
            for wallet in accts:
        
                if wallet['currency'] == 'USD':
                    cash = float(wallet['balance'])
                    print ("cash balance is", "{:.8f}".format(cash))
        
                if wallet['currency'] == coin:
                    balance = float(wallet['balance'])
                    print (coin, "balance is", "{:.8f}".format(balance))
                    
        return (accts)
    
    
    def getFuture(self):
        '''
        Get the next 300 minute data points after virtual_time
        
        This stores the "future" from the perspective of virtual_time
        We then use the future to getTimePrice 
        '''
        
        start = self.virtual_time
        
        granularity = 60
        
        # I'm not sure why I'm subtracting a minute, 
        # has something to do with the interval
        start = start - timedelta(seconds=60)
        
        duration = granularity * 300
        #print ("granularity:", gran)
        #print ("seconds:", duration)
        
        #print ("end_time:", end_time)
        end = start + timedelta(seconds=duration)
        
        '''
        Get History
        '''
        #print ("start", start)
        #print ("end", end)
        
        #future = self.trade_client.get_product_historic_rates(self.ticker, start, end, granularity=granularity)
        future_df = self.getHistoryRange(start, end, granularity)
    
        #if history['message']:
        #    print ("error message:", history['message'])
    
        # Granularity Options are 60, 300, 900, 3600, 21600, 86400
        # Corresponding to: 1M, 5M, 15M, 1H, 6H, 1D
    
        # this was before using getHistoryRange was used for this
        #future_df = pd.DataFrame.from_records(future,  columns = ['time', 'low', 'high', 'open', 'close', 'volume'])
        #future_df['time'] = pd.to_datetime(future_df['time'], unit='s')
        #future_df.set_index('time', inplace=True)
        
        future_df.sort_index(inplace = True)
    
        #print ("future_df head:\n", future_df.head())
        
        return (future_df)
        
    def getTimePrice(self):
        '''
        
        '''
        
        #print ("get the current price")
        
        if self.live_data:
            self.virtual_time = datetime.datetime.utcnow().replace(microsecond=0,second=0)
            return_price = self.trade_client.get_product_ticker(product_id=self.ticker)
            
        else:
            # maybe get the price from history - how to get just one past data point?
            # interval of ?
            
            if (self.future_df.empty):
                print ("future is empty, get next block")
                self.future_df = self.getFuture()
            
            #time_str = pd.Timestamp(self.virtual_time)
            
            #.strftime("%m-%d-%Y %H:%M:%S")
            
            time_ts = pd.Timestamp(self.virtual_time.strftime("%m-%d-%Y %H:%M:%S"))
            #time_ts = pd.Timestamp(self.virtual_time)
            
            time_str = self.virtual_time.strftime("%Y-%m-%d %H:%M:%S")
            
            #print ("Getting item at time:", time_str)
            
            # we want the data for time time_str, if not there, get it
            if not (self.future_df.index.contains(time_str)):
                print ("Load another future block")
                self.future_df = self.getFuture()
                # wait some time to not overload coinbase api during testing
                time.sleep(5)

            # get last price off the end
            '''
            lastprice = self.future_df.iloc[-1:].to_dict()
            
            lasttime = list(lastprice['open'].keys())[0]
            
            if (lasttime==time_ts):
                print ("times match")
            else:
                print ("ERROR: times do not match!")
            '''
            
            try:        
                #price = self.future_df.loc[time_str].to_dict()
                price = self.future_df.ix[time_str].to_dict()
            except:
                print ('can not find row at time', time_str)
                print (self.future_df.tail(5))
        
            if not (price['open']):
                print ("there's nothing here!")
                # some prices evidently are not valid
                # increment time and try again?
                
                # increment virtual time by 1 minute
                self.virtual_time = self.virtual_time + timedelta(seconds=60)
            
                return_price = self.getTimePrice()
        
            
            
            # hackey hack, don't talk back!
            # to_dict seems to work differently when only one row is left
            # update - that's just how they work in python
            # hack to fix:
            elif (isinstance(price['open'],float)):
                #print ("it's a float!")
            
                print ("drop row at:", time_ts)
                self.future_df.drop(time_ts, inplace=True)
                
                print ("returning price as:", price)
                
                
                #price.rename(columns={'open':'price', 'high':'ask', 'low':'bid'}, inplace = True)
                # put historic price in same context as live price
                return_price = {}
                return_price['time'] = time_ts
                return_price['price']=price['open']
                return_price['bid'] = price['low']
                return_price['ask'] = price['high']
                
            else:    
                
                print (price['open'][time_ts])
                print (list(price['open'].keys())[0])
                
                ##self.future_df.drop(time_str)
                
                # remove last (earliest) price
                #self.future_df = self.future_df[:-1]
                print ("drop row at:", time_ts)
                self.future_df.drop(time_ts, inplace=True)
                
                #price = self.future_df.loc(time_str)
                
                print ("returning price as:", price)
                
                
                #price.rename(columns={'open':'price', 'high':'ask', 'low':'bid'}, inplace = True)
                # put historic price in same context as live price
                return_price = {}
                return_price['time'] = time_ts
                return_price['price']=price['open'][time_ts]
                return_price['bid'] = price['low'][time_ts]
                return_price['ask'] = price['high'][time_ts]
            
            # increment virtual time by 1 minute
            self.virtual_time = self.virtual_time + timedelta(seconds=60)
            
            
        return (return_price)
    
    
    
    def getFeatures(self):
        ''' 
        Given a time, get the features that we will use for our ML algorithm
        '''
        
        if self.live_data:
            self.virtual_time = datetime.datetime.utcnow().replace(microsecond=0,second=0)
            time = self.virtual_time
        else: 
            time = self.virtual_time
        
        #num_points = 9
        #granularity = (900, 3600, 21600, 86400)
        num_points = 150
        granularity = (900,3600,21600)
        
        features = []
        
        for gran in granularity:
        
            duration = gran * (num_points + 1)
            start_time = time - timedelta(seconds=duration)
            
            history_df = self.getHistoryRangeClose(start_time, time, gran, num_points)
            
            #print ('nan count:', history_df.isna().sum())
    
            if (history_df.shape[0] > num_points):
                # then drop one
                history_df.drop(history_df.index[0], inplace=True, axis=0)

            if (history_df.shape[0] != num_points):
                print ('shape,', history_df.shape)
            
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(history_df)
            
            #print ('sd flat shape', scaled_data.flatten().shape)
            
            features.append(scaled_data.flatten())
            
            #print (scaled_data)
            #print (scaled_data.flatten())
            #print(features)
            
        
        np_return = np.concatenate(features).ravel()
                
        return (np_return)    
    