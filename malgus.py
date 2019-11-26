'''
Created on Sep 4, 2019

@author: rich
'''

#from data_loader import DataLoader
from position import Position
#from action import Action
#from logger import Logger
from listener import Listener
#from buyer import Buyer
import pandas as pd
from monitor import Monitor
#from seller import Seller

class Malgus(object):
    '''
    classdocs
    '''
    def __init__(self, data, days, log, model):
        '''
        Constructor
        '''
        self.ticker = data.ticker
        self.coin = self.ticker[0:3]
        self.days = days
        self.data = data
        self.log = log
        self.iterations = 0
        self.position = Position(self.ticker)
        self.cash = 0.0
        self.coin_balance = 0.0
        self.model = model
    
    def determineInitialAction(self):
        '''
        Review Account information and recommend action - ask user to confirm
        '''
        
        # Get all account info and balances
        accounts = self.data.getAccountInfo()
        
        # Add try / catch if accounts variable is empty
        
        for wallet in accounts:
    
            if wallet['currency'] == 'USD':
                self.cash = float(wallet['balance'])
                print ("cash balance is", "{:.8f}".format(self.cash))
    
            if wallet['currency'] == self.coin:
                coin_balance = float(wallet['balance'])
                print (self.coin, "balance is", "{:.8f}".format(coin_balance))
        
        '''
        else:
            self.position.usd = 1000.00
            self.cash = 1000.00
        '''    
        
        # prompt user to Listen for buying with cash balance or monitor for sale of coin_balance
        # and total amount (-10%?) to put into play 
        # for now, assume start with listen and 100%
        # for testing, could use a fake amount also
        
        buy_or_sell = int (input('Buy or Sell? 1 for buy, 2 for sell:'))
        if (buy_or_sell == 1):
            #print ('Buy', self.ticker)
            buy_cash = float (input('Dollar amount to purchase?'))
            self.position.usd = float(buy_cash)
            action = Listener(self.data, self.position, self.log, self.model)
        
        elif (buy_or_sell == 2):
            #print ('Sell', self.ticker)
            sell_qty = float (input('What qty of coin to sell?'))
            self.position.qty = float(sell_qty)
            buy_price = float (input('What was your buy price (for stoploss det)?'))
            self.position.buy_price = float(buy_price)
            action = Monitor(self.data, self.position, self.log, self.model)

        else:
            exit()
        
        # Double Check if we want to go live
        if (self.data.do_trade):
            print ("For real")
            sure = int (input("Placing trade - are you sure? 1 for yes, 0 for no: "))
            if (sure == 0):
                print ("Exiting without trade")
                quit()
        else:
            print ("!!!TESTING ONLY!!!")
        
        
        
        
        # from this, create the position that we are going to make, qty, ticker, etc
        
        return (action)
    
    def loadData(self):
        pass
    
    def evaluate(self):
        
        print ("log:", self.log.trades_df)
        
        # get the first row and determine if it's a buy
        buy_position = pd.Series()
        total_gain = 0.0
        
        for index, trades in self.log.trades_df.iterrows():
        
            if buy_position.empty:    
                buy_position = trades
            else:
                sell_position = trades
                
                # determine gain/loss:
                gain = (sell_position['price'] - buy_position['price']) * sell_position.qty
                
                print ('gain: $', gain)
                total_gain += gain
                buy_position = pd.Series()
                
                
        print ("total gain $ = ", total_gain)
        print ('percent gain = ', ((total_gain / self.cash)*100))
        
        
    def showResults(self):
        pass
    
    def checkStop(self):
        self.iterations += 1
        
        rounds = 3
        
        if (self.iterations == rounds * 4):
            return (False)
        else:
            return (True)
        