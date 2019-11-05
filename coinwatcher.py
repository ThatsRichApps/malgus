'''
Created on Jan 28, 2019

@author: rich
'''

import cbpro
import time
from config_reader import Login

# get account info from config file
myLogin = Login()

numcoins = 0.2
cointype = 'BTC-USD'
buyprice = 9947.89

stopPercent = 5.6
gainPercent = 9.0

#numcoins = 0.2
#cointype = 'BTC-USD'
#buyprice = 9947.89
#stopPercent = 5.6
#gainPercent = 9.0

doTrade = False

if (doTrade):
    print ("for reals")


if __name__ == '__main__':
    
    print ("Coinbase Pro Coin Price Watcher")
            
    # Use the real API
    
    auth_client = cbpro.AuthenticatedClient(myLogin.key, myLogin.b64secret, myLogin.passphrase)
    
    trade_client = auth_client
        
    counter = 0
    loopIt = True
    
    stopLoss = round(buyprice * (1 - stopPercent / 100), 4)
    stopGain = round(buyprice * (1 + gainPercent / 100), 4)
    
    print ("bought ", numcoins, " of ", cointype, " at ", buyprice)
    
    print ("stoploss of ", stopPercent, "% at ", stopLoss)
    print ("stopgain of ", gainPercent, "% at ", stopGain)
    
    while (loopIt):
    
        # Get the product ticker for a specific product.
        ticker = trade_client.get_product_ticker(product_id=cointype)
        
        try:
            spotprice = float(ticker['price'])
        except:
            print ("error connecting to coinbase, sleep 10 s")
            time.sleep(10)
            continue
        
        print ("Price of ", cointype, " is ", ticker['price'], " at ", ticker['time'])
    
        
        if (spotprice < stopLoss):
            print ("hit stoploss, sell at ask price ", ticker['ask'])
            
            if (doTrade):
            
                # sell at market value (could be low, but should execute)
                #response = trade_client.place_market_order(product_id=cointype, 
                #               side='sell', 
                #               size=numcoins)           
                
                # sell at ask price
                response = trade_client.place_limit_order(product_id=cointype, 
                            side='sell', 
                            price=ticker['ask'], 
                            size=numcoins)
            
                
                 
            
                print ("response: ", response)
            
            else:
                print ("Do Trade Flag Not Set")
            
            loopIt = False
    
        if (spotprice > stopGain):
            print ("hit gain goal, sell")
            
            if (doTrade):
            
                response = trade_client.place_limit_order(product_id=cointype, 
                            side='sell', 
                            price=ticker['ask'], 
                            size=numcoins)
            
                print ("response: ", response)
            
            else:
                print ("Do Trade Flag Not Set")
            
                
            loopIt = False
        
        time.sleep(20)
    
        counter += 1
        
        # set timeout?
        #if (counter == 100):
        #    loopIt = False
    
    
    print ("End Program")
    
    
    '''
    sure = int (input("Placing trade - are you sure? 1 for yes, 0 for no: "))
    
    if (sure == 0):
        print ("Exiting without trade")
        quit()

    '''

    # Limit order-specific method
    '''
    response = trade_client.place_limit_order(product_id='BTC-USD', 
                              side='sell', 
                              price='6400', 
                              size='0.001')
    
    print ("response: ", response)
    '''

        
