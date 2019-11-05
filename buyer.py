'''
Created on Aug 29, 2019

@author: rjhumphrey
'''

import config_reader
import cbpro
import time
from datetime import datetime
from action import Action
#import position

class Buyer(Action):
    '''
    classdocs
    '''

    def __init__(self, data, position, log, tolerance):
        '''
        Constructor
        '''
        self.descr = 'Buy'
        self.position = position
        self.buy_price = 0
        self.data = data
        self.log = log
        self.tolerance = tolerance
        
    def performAction(self):
        print ("buyer perform action method")
        print ("I am going to: ", self.descr)
        self.buy()
        
    def buy(self):
        
        # spending self.position.usd for current price of ticker
        
        print ("about to buy", self.position.usd, "of", self.position.ticker)
        
        '''
        if (self.data.do_trade):
            print ("For real")
            sure = int (input("Placing trade - are you sure? 1 for yes, 0 for no: "))
            if (sure == 0):
                print ("Exiting without trade")
                quit()
        else:
            print ("!!!TESTING ONLY!!!")
        '''
        
        #trade_client = cbpro.AuthenticatedClient(self.login.key, self.login.b64secret, self.login.passphrase)
        
        # get the current price
        price  = self.data.getTimePrice()        
        #price = self.data.trade_client.get_product_ticker(product_id=self.position.ticker)
        
        try:
            spotprice = float(price['price'])
        except:
            print ('returned error, sleep and try again')
            time.sleep(10)
            spotprice  = self.data.getTimePrice()        
            
        counter = 0
        loopIt = True
        
        buy_tolerance = 1 + (self.tolerance / 100)

        print ("buy tolerance = ", buy_tolerance)
        current_low = spotprice
        
        while (loopIt):
        
            # Get the product ticker for a specific product.
            # wrap in try catch
            
            price = self.data.getTimePrice()
            
            try:
                spotprice = float(price['price'])
            except:
            
                print ('returned error, sleep and try again')
                time.sleep(10)
                continue
        
            #tickerDT = tickerDT + offset
            #print ("Price of ", self.position.ticker, " is ", price['price'], " at ", tickerDT.strftime("%d %b %Y (%I:%M:%S:%f %p) %Z"))
        
            print ("buy if spotprice ", spotprice, "gets above ", current_low * buy_tolerance)
            self.position.qty = round(self.position.usd / float(price['bid']), 4)
            print ("quantity =", self.position.qty)
                
            if (spotprice > (current_low * buy_tolerance)):
                print ("buy it!", price['bid'])
                
                self.position.qty = round(self.position.usd / float(price['bid']), 4)
                #print ("quantity =", self.position.qty)
                
                if (self.data.do_trade):
                
                    response = self.data.trade_client.place_limit_order(product_id=self.position.ticker, 
                                side='buy', 
                                price=price['bid'], 
                                size=self.position.qty)
        
                    print ("response: ", response)
                
                else:
                    print ("Do Trade Flag Not Set")
                    print ('Simulate buy of', self.position.qty, 'at', price['bid'])
                    
                loopIt = False
            
            current_low = min(current_low, spotprice)
            
            # only need to sleep for live trading
            if self.data.live_data:
                time.sleep(30)
        
            counter += 1
            
            # set timeout?
            if (counter == 1000):
                print ('buy timeout')
                # set qty to 0
                loopIt = False
        
        self.position.buy_price = price['bid']        
        self.position.time = self.data.virtual_time
        print ("BUY:", self.position.qty, "of", self.position.ticker, "at", price['bid'], "at", self.position.time)
        
        # Log the buy in Logger
        self.log.addTrade("buy", self.position)
        
        # Add here, monitor to see if executed?
        if (self.data.do_trade):
            # If we made a read trade, sleep 
            # 1 day - 86400, 4H - 21600
            time.sleep(21600)
        
            
