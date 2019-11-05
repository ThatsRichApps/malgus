'''
Created on Sep 4, 2019

@author: rich
'''

class Action(object):
    '''
    classdocs
    '''
    
    def __init__(self, descr):
        '''
        #Constructor
        '''
        self.descr = descr
    
    def performAction(self, position):
        print ("main action perform method")
        print ("I am going to: ", self.descr)
            