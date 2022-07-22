from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from ..misc import config_reader
import os

class db_alchemy():
    def __init__(self, name="database"):
        self.name = name
    
    def get_engine(self, kind = "config"):
        
        """
        Returns an sqlalchemy engine object according to the connection details specified in the config file.
        """
        if kind == "config":
            try:
                conf = config_reader().get_config()[self.name]
                host  = conf['host']
                port  = conf['port']
                type  = conf[ 'type']
                password  = conf['password']
                database  = conf['database']
                user_id = conf['user_id']
                db_config = type + '://' + user_id +':' + password + '@' +  host + ':' + port + '/'  +  database
                return create_engine(db_config, poolclass=NullPool)
            except Exception as e:
                print(str(e) + "\n Datenbank not found, please make user the database is connected and the right parameters are set \n Using sqlite as a default")
                return self.get_engine(kind="sqlite")
        elif kind == ".env":
            try:
                load_dotenv()
                conf = os.environ
                host = conf.get("host")
                port = conf.get("port", "5432")
                type = conf.get("type", "postgresql")
                password = conf.get("password", conf.get("pwd"))
                database = conf.get("database")
                user_id = conf.get("uid")
                db_config = type + '://' + user_id +':' + password + '@' +  host + ':' + port + '/'  +  database
                return create_engine(db_config, poolclass=NullPool)
            except Exception as e:
                print(str(e) + "\n Datenbank not found, please make user the database is connected and the right parameters are set \n Using sqlite as a default")
                return self.get_engine(kind="sqlite")
        elif kind == "sqlite":
            db_config = 'sqlite:///' + os.getcwd() + '\\default_' + self.name + '.db'
            return create_engine(db_config, poolclass=NullPool)
        else:
            raise ValueError("Invalid type. Please choose one of [ 'config', '.env', 'sqlite' ]")
