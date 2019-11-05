'''
Created on Sep 4, 2019

@author: rich
'''

from malgus import Malgus
from strategy import Strategy
from data_loader import DataLoader
#from plotter import Plotter
from logger import Logger
from model import Model

import datetime
#import pandas as pd

if __name__ == '__main__':

    # Instantiate an algorithm for given coin, startdate (now for live), and duration
    ticker = 'BTC-USD'
    start_time_str = '2019-03-01 00:00:00.000000'
    
    #dateout = '{%Y-%m-%d %H:%M:%S.%f}'
    
    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
    days = 90
    
    log = Logger()
    
    live_data = True
    do_trade = False
    
    data = DataLoader(ticker, start_time, live_data, do_trade)

    model = Model(data)
    model.fit()
    
    algorithm = Malgus(data, days, log, model)
    
    action = algorithm.determineInitialAction()
    
    strategy = Strategy(data, action, model)
    
    within_duration = True
    
    while (within_duration):
        
        print ("start action:", action.descr)
        
        action.performAction()
        
        next_action = strategy.chooseNextAction()
        
        action = next_action
        
        within_duration = algorithm.checkStop()
        
    algorithm.evaluate()

    algorithm.showResults()
    
