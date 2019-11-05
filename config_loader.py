'''
Created on Aug 26, 2019

@author: rjhumphrey

config_loader.py

Used for importing from config.ini settings and account info

'''

from configparser import SafeConfigParser
import os


class Config:
    """Interact with configuration variables."""

    configParser = SafeConfigParser()
    configFilePath = (os.path.join(os.getcwd(), '../../../../config/config.ini'))
    print ("config file = ", configFilePath)
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
    