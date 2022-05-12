from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from ..misc import config_reader

class db_alchemy():
    def __init__(self, name):
        self.name = name
        self.config =  config_reader().get_config()
    
    
    def get_engine(self):
        """
        Returns an sqlalchemy engine object according to the connection details specified in the config file.
        """
        print(self.config)
        host  = self.config[self.name]['host']
        port  = self.config[self.name]['port']
        type  = self.config[self.name][ 'type']
        password  = self.config[self.name]['password']
        database  = self.config[self.name]['database']
        user_id = self.config[self.name]['user_id']
        db_config = type + '://' + user_id +':' + password + '@' +  host + ':' + port + '/'  +  database
        return create_engine(db_config, poolclass=NullPool)

    

