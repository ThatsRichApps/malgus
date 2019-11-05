'''
Created on Sep 14, 2019

@author: rich
'''
import unittest

from data_loader import DataLoader
from plotter import Plotter
import datetime
from datetime import timedelta
from sklearn.preprocessing import MinMaxScaler

class TestPlotter(unittest.TestCase):


    def setUp(self):
    
        ticker = 'BTC-USD'
        start_time_str = '2015-01-01 12:00:00.000000'
        self.start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
        live_data = False
        self.data = DataLoader(ticker, self.start_time, live_data)
        
    def tearDown(self):
        pass

    @unittest.skip("demonstrating skipping")
    def testAllPlots(self):
        
        print ("does this even run?")
        return(True)
    
        history = {}
    
        history = self.data.getAllHistory(self.start_time)
    
        for granularity in self.data.GRANULARITY:
        
            df = history[granularity]
            plot = Plotter.showPlot(df)
                
        assert(True)

    @unittest.skip("demonstrating skipping")
    def testDayPlot(self):
        
        granularity = 86400
        
        end_time_str = '2016-01-01 12:00:00.000000'
        end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S.%f')
        
        duration = granularity * 300
        start_time = end_time - timedelta(seconds=duration)
        
        range_df = self.data.getHistoryRange(start_time, end_time, granularity)

        range_df['time'] = range_df.index
        print (range_df.head(20))
        
        
        plot = Plotter.showPlot(range_df)

        assert(True)


    def testFuturePercentPlot(self):
        
        granularity = 43200
        
        start_time_str = '2016-01-01 12:00:00.000000'
        start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
        
        duration = granularity * 60
        end_time = start_time + timedelta(seconds=duration)
        
        range_df = self.data.getHistoryRange(start_time, end_time, granularity)

        # add time as a column outside of the index for the plotter
        #print (range_df.head(20))
        
        new_df = range_df.loc[:,['open']]
                
        #plot = Plotter.showOHLCPlot(range_df)

        base_price = new_df['open'].iloc[0]

        new_df['open'] = ((new_df['open'] - base_price) / base_price) * 100

        print ('base price is:', base_price)
        
        new_df['target'] = 0

        new_df.at['2016-01-20 00:00:00','target'] = 1
        new_df.at['2016-01-21 00:00:00','target'] = 2

        print ('new_df:', new_df.head(20))

        plot2 = Plotter.showSinglePlot(new_df)

        assert(True)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()