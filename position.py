'''
Created on Sep 9, 2019

@author: rjhumphrey
'''

import datetime

class Position(object):
    '''
    classdocs
    '''

    def __init__(self, ticker):
        '''
        Constructor
        '''
        self.time = datetime.datetime.utcnow()
        self.usd = 0.0
        self.ticker = ticker
        self.trade_type = 'na'
        self.qty = 0.0
        self.buy_price = 0.0
        self.sell_price = 0.0    
        