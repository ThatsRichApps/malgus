'''
Created on Sep 11, 2019

@author: rich
'''
from action import Action
import time
from datetime import timedelta

class Monitor(Action):
    '''
    classdocs
    ''' 
    def __init__(self, data, position, log, model):
        '''
        Constructor
        '''
        self.descr = 'Monitor'
        self.position = position
        self.data = data
        self.log = log
        self.model = model
        self.query_interval_secs = 300
        
    def performAction(self):
        '''
        Monitor action should get features for current or virtual time
        send features to the model to get a prediction
        if prediction is 'sell' (2) then move to sell action
        '''
        
        print ("Monitor price for sell signal")
        
        sell_trigger = False
        
        while not (sell_trigger):
        
            prediction = self.model.predict()[0]
            print ('Waiting for sell signal, recc:', prediction)
        
            if (prediction == 2):
                print ('Trigger sell')
                sell_trigger = True
                continue
            
            # also check to see if we have passed a stoploss:
            # 4%?
            stoploss = 0.20
            price  = self.data.getTimePrice()        

            try:
                spotprice = float(price['price'])
                print ('Price:', spotprice)

            except:
                print ('returned error, sleep and try again')
                time.sleep(10)
                continue
            

            if (spotprice < (self.position.buy_price * (1-stoploss))):
                print ('hit stoploss,', spotprice, ' is below stoploss for', self.position.buy_price)
                sell_trigger = True
                continue 
            
            # Wait a set number of seconds
            if (self.data.live_data):
            
                time.sleep(self.query_interval_secs)

            else: 
            
                #increment virtual time to simulate a wait
                self.data.virtual_time = self.data.virtual_time + timedelta(seconds=self.query_interval_secs)
    
    
    