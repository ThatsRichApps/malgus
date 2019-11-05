'''
Created on Sep 11, 2019

@author: rjhumphrey
'''

print ("Coin Seller")

from seller import Seller
from position import Position
from logger import Logger
from data_loader import DataLoader

import datetime

position = Position('LTC-USD')
position.qty = 20

timenow = datetime.datetime.utcnow()

data = DataLoader(position.ticker, timenow, False)

log = Logger()

tolerance = 5.0

seller = Seller(data, position, log, tolerance)

seller.sell()
