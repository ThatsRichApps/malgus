'''
Created on Sep 11, 2019

@author: rjhumphrey
'''

import config_reader
import cbpro
import time
from datetime import datetime
from action import Action
#from position import Position

class Seller(Action):
    '''
    classdocs
    '''

    def __init__(self, data, position, log, tolerance = 0.5):
        '''
        Constructor
        '''
        self.descr = 'Sell'
        self.position = position
        self.data = data
        self.log = log
        self.sell_price = 0.0
        self.sell_tolerance = tolerance
        
    def performAction(self):
        print ("Seller perform action method")
        self.sell()
            
    def sell(self):
                # spending self.cash for current price of ticker
        
        print ("about to sell position: ", self.position)
        
        '''
        if (self.data.do_trade):
            print ('Do Live Trade Flag Set')
            sure = int (input("Placing trade - are you sure? 1 for yes, 0 for no: "))
            if (sure == 0):
                print ("Exiting without trade")
                quit()
        else:
            print ("!!!TESTING ONLY!!!")
        '''
        
        price  = self.data.getTimePrice()        
        
        try:
            self.sell_price = float(price['price'])
        except:
            print ('returned error, sleep and try again')
            time.sleep(10)
            #price = self.data.trade_client.get_product_ticker(product_id=self.ticker)
            price  = self.data.getTimePrice()  
            self.sell_price = float(price['price'])

        print ('price =', self.sell_price)
        print ("quantity =", self.position.qty)
        
        # round to the nearest?
            
        counter = 0
        loopIt = True
        
        # determine offset from UTC time
        #offset = datetime.now() - datetime.utcnow()
        
        # set % sell tolerance
        sell_tolerance = 1 - (self.sell_tolerance / 100)

        print ("sell tolerance = ", sell_tolerance)
        current_high = self.sell_price
        
        while (loopIt):
        
            # Get the product ticker for a specific product.
            # wrap in try catch
            
            #price = self.data.trade_client.get_product_ticker(product_id=self.position.ticker)
            price  = self.data.getTimePrice()        

            try:
                spotprice = float(price['price'])
            except:
                print ('returned error, sleep and try again')
                time.sleep(10)
                continue

            #tickerDT = datetime.strptime(price['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            # convert to MT
            #tickerDT = tickerDT + offset
        
            #print ("Price of ", self.position.ticker, " is ", price['price'], " at ", tickerDT.strftime("%d %b %Y (%I:%M:%S:%f %p) %Z"))
            
            print ("sell if spotprice ", spotprice, "goes below ", current_high * sell_tolerance)
        
            if (spotprice < (current_high * sell_tolerance)):
                print ("SELL!!! at", price['ask'])
                
                if (self.data.do_trade):
                
                    response = self.data.trade_client.place_limit_order(product_id=self.position.ticker, 
                            side='sell', 
                            price=price['ask'], 
                            size=self.position.qty)
        
                    print ("response: ", response)
                
                else:
                    print ("Do Trade Flag Not Set")
                    print ('simulate sale at', price['ask'])
                
                loopIt = False
            
            current_high = max(current_high, spotprice)
            
            # only need to sleep on live trading
            if self.data.live_data:
                time.sleep(20)
        
            counter += 1
            
            # set timeout?
            if (counter == 1000):
                print ('sell timeout')
                loopIt = False
        

        # Add here, monitor to see if executed?
        
        self.position.sell_price = price['ask']        
        self.position.time = self.data.virtual_time
        print ("Sell:", self.position.qty, "of", self.position.ticker, "at", price['ask'], "at", self.position.time)
        
        # Log the sell in Logger
        self.log.addTrade("sell", self.position)
        
        # clear position?
        # Add here, monitor to see if executed
        if (self.data.do_trade):
            # If we made a read trade, sleep 
            # 1 day - 86400, 4H - 21600
            time.sleep(21600)
        
        
        
        
        
        
        
            
