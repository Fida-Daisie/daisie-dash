from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from ..misc import config_reader
import os
class db_alchemy():
    def __init__(self, name):
        self.name = name
        self.config =  config_reader().get_config()
    
    
    def get_engine(self):
        
        """
        Returns an sqlalchemy engine object according to the connection details specified in the config file.
        """
        try:
            host  = self.config[self.name]['host']
            port  = self.config[self.name]['port']
            type  = self.config[self.name][ 'type']
            password  = self.config[self.name]['password']
            database  = self.config[self.name]['database']
            user_id = self.config[self.name]['user_id']
            db_config = type + '://' + user_id +':' + password + '@' +  host + ':' + port + '/'  +  database
            return create_engine(db_config, poolclass=NullPool)
        except Exception as e:
            print(str(e) + "/n Datenbank not found, please make user the database is connected and the right parameters are set /n Using sqlite as a default")
            db_config = 'sqlite:///' + os.getcwd() + '\\default_' + self.name + '.db'
            return create_engine(db_config, poolclass=NullPool)



    

