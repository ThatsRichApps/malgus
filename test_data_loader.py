'''
Created on Sep 14, 2019

@author: rich
'''
import unittest

from data_loader import DataLoader
import datetime
from datetime import timedelta

class TestDataLoader(unittest.TestCase):


    def setUp(self):
        ticker = 'BTC-USD'
        start_time_str = '2018-10-31 12:00:00.000000'
        self.start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
        live_data = False
        self.data = DataLoader(ticker, self.start_time, live_data)


    def tearDown(self):
        pass


    def testDataLoader(self):
        
        self.assertEquals(self.data.ticker,'BTC-USD')
      

    def testJumpTime(self):

        dataload = self.data
        future = dataload.getFuture()
        
        print ("future_df_tail:", future.tail(5))
        
        price = dataload.getTimePrice()

        print ("initial price is:", price)
        print ("at time:", dataload.virtual_time)
        
        # increment time by more than 300 minutes (size of future_df)
        n_days = 3
            
        self.data.virtual_time = self.data.virtual_time + timedelta(seconds=(n_days*86400)-60)
        
        loopy = True
        counter = 0
    
        while (loopy):
            price = dataload.getTimePrice()

            print ("price:", price)
            
            
            counter +=1
            if (counter > 4):
                loopy = False

    
    def testFutureReturn(self):

        dataload = self.data
        
        future = dataload.getFuture()
        
        print ("dlfuture:", future.tail(5))
        
        price = dataload.getTimePrice()

        print ("initial price is:", price)
        print ("virtual time:", dataload.virtual_time)
        loopy = True
        counter = 0
        while (loopy):
            price = dataload.getTimePrice()

            print ("price:", price)
            
            
            counter +=1
            if (counter > 3):
                loopy = False      


            




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    
    