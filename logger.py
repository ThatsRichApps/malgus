'''
Created on Sep 9, 2019

@author: rjhumphrey
'''
import pandas as pd
import datetime

class Logger(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.trades_df = pd.DataFrame(columns=['time','trade_type', 'price','qty'])
        
    def addTrade(self,trade_type,position):
 
        if (trade_type == 'buy'):
            self.trades_df = self.trades_df.append({'time' : position.time, 'trade_type' : trade_type, 'price':position.buy_price, 'qty':position.qty}, ignore_index = True)
        elif (trade_type == 'sell'):
            self.trades_df = self.trades_df.append({'time' : position.time, 'trade_type' : trade_type, 'price':position.sell_price, 'qty':position.qty}, ignore_index = True)
        
        self.write_log()

    def write_log(self):
        '''
        Use filedataloader to write trades_df to csv
        append if exists.  Use unique name (timestamp)
        '''
        
        filename = datetime.datetime.now().strftime('../logs/%Y%m%d_%H_log.csv')
        #filename = r'../logs/test_logs.csv'

        #self.trades_df.to_csv(filename, mode='a')
        self.trades_df.to_csv(filename)

        
        # then clear out the data
        #self.trades_df = self.trades_df.iloc[0:0]
