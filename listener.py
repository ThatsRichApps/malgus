'''
Created on Sep 10, 2019

@author: rjhumphrey
'''

from action import Action
import time
from datetime import timedelta

class Listener(Action):
    '''
    classdocs
    '''
    
    def __init__(self, data, position, log, model):
        '''
        Constructor
        '''
        self.descr = 'Listen'
        self.position = position
        self.data = data
        self.log = log
        self.model = model
        self.query_interval_secs = 300
        
    def performAction(self):
        '''
        Listen action gets features for current or virtual time
        sends the features to the model for a prediction
        if prediction is 'buy' then move to buy action
        '''
        print ('Listen action, wait for buy trigger')
        
        
        buy_trigger = False
        
        while not (buy_trigger):
        
            prediction = self.model.predict()[0]
            
            price = self.data.getTimePrice()
            
            try:
                buy_price = float(price['price'])
            except:
                print ('returned error, sleep and try again')
                time.sleep(10)
                #price = self.data.trade_client.get_product_ticker(product_id=self.ticker)
                price  = self.data.getTimePrice()  
                buy_price = float(price['price'])

            print ('Price:', buy_price, ', Waiting for buy signal, current prediction:', prediction, 'at', self.data.virtual_time)
        
            if (prediction == 1):
                print ('Trigger buy')
                buy_trigger = True
                continue
            
            # Wait a set number of seconds
            if (self.data.live_data):
            
                time.sleep(self.query_interval_secs)
            
            else: 
            
                #increment virtual time to simulate a wait
                self.data.virtual_time = self.data.virtual_time + timedelta(seconds=self.query_interval_secs)
    
    
    
        