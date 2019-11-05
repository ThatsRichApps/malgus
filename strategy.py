'''
Created on Sep 4, 2019

@author: rich
'''

from action import Action
from listener import Listener
from buyer import Buyer
from monitor import Monitor
from seller import Seller

class Strategy(object):
    '''
    classdocs
    '''
    def __init__(self, data, action, model):
        '''
        Constructor
        '''
        self.data = data
        self.current_action = action
        self.model = model
        
    def chooseNextAction(self):
        
        previous_action = self.current_action
        
        # set next state as the correct action listen, buy, monitor,sell
        next_action = Action("null")
        
        if (previous_action.descr == "Listen"):
            
            next_action = Buyer(self.data, previous_action.position, previous_action.log, 0.5)
        
        elif (previous_action.descr =="Buy"):
            
            next_action = Monitor(self.data, previous_action.position, previous_action.log, self.model)
                    
        elif (previous_action.descr == "Monitor"):
            
            next_action = Seller(self.data, previous_action.position, previous_action.log, 0.5)
            
        elif (previous_action.descr == "Sell"):
        
            next_action = Listener(self.data, previous_action.position, previous_action.log, self.model)
        
        else:
            next_action.descr = "Abort!!!"
        
        self.current_action = next_action
        
        return (next_action)
    