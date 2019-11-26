'''
Created on Sep 18, 2019

@author: rjhumphrey
'''

from config_reader import DB_Config
import mysql.connector

class MySQLDatabase(object):
    '''
    Connect to and provide access to a mysql database
    Database parameters are stored in config.ini file
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.db_config = DB_Config()

        self.mydb = mysql.connector.connect(
            host=self.db_config.host,
            user=self.db_config.user,
            passwd=self.db_config.passwd
        )

        print(self.mydb)

    def connect(self):
        print ("connect to database")
        
        
        
    def show(self):
        '''
        method
        ''' 
        mycursor = self.mydb.cursor()

        mycursor.execute("SHOW DATABASES")

        for x in mycursor:
            print(x)   


if __name__ == '__main__':
        
    database = MySQLDatabase()
    
    database.show()
    
    