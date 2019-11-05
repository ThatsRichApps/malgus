'''
Created on Aug 28, 2019

@author: rich
'''

from configparser import SafeConfigParser
import os

class Config:
    """Interact with configuration variables."""
    
    configParser = SafeConfigParser()
    configFilePath = (os.path.join(os.getcwd(), '../../../../config/config.ini'))
    #print ("config file = ", configFilePath)
    configParser.read(configFilePath)

    @classmethod
    def initialize(cls):
        """Start config by reading config.ini."""
        cls.configParser.read(cls.configFilePath)

    @classmethod
    def prod(cls, key):
        """Get prod values from config.ini."""
        return cls.configParser.get('PROD', key)

    @classmethod
    def dev(cls, key):
        """Get dev values from config.ini."""
        return cls.configParser.get('DEV', key)

    @classmethod
    def database(cls, key):
        '''
        Get database names and login
        '''
        return cls.configParser.get('DATABASE', key)


class Login(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        #print ("config file reader test")   
        
        try:
            self.key = Config.prod('key')
            self.b64secret = Config.prod('b64secret')
            self.passphrase = Config.prod('passphrase')
            #print ("key =", self.key)
            #print ("b64secret =", self.b64secret)
            #print ("passphrase =", self.passphrase)
        
        except Exception as e: 
            print ("error with config file")
            print(e)

class DB_Config:
    '''
    classdocs
    '''

    
    def __init__(self):
        '''
        Read the config.ini file and create a config object
        that contains the hostname, username, and password
        
        '''
        
        try:
            self.host = Config.database('host')
            self.user = Config.database('user')
            self.passwd = Config.database('passwd')
            #print ("host =", self.host)
        
        except Exception as e: 
            print ("error with config file")
            print(e)


