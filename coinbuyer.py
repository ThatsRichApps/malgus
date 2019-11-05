
'''
Created on Jan 28, 2019

@author: rjhumphrey

Coinbuyer watches the current chart and tries to get in at a low price


'''

print ("Coin buyer")

from buyer import Buyer
from position import Position
from logger import Logger
from data_loader import DataLoader

import datetime

position = Position('BTC-USD')
position.usd = 7700

timenow = datetime.datetime.utcnow()

data = DataLoader(position.ticker, timenow, False)

log = Logger()

tolerance = 0.5

buyer = Buyer(data, position, log, tolerance)

buyer.buy()
