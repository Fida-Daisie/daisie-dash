import configparser
import os
from pathlib import Path

class config_reader():
    def __init__(self):
        self.name = 'config.ini'

    def get_config(self):
        cwd = os.getcwd()
        print(cwd)
        filepath = cwd+'/'+ self.name
        alt_filepath = cwd+'/daisie/'+ self.name
        if os.path.isfile(filepath):
            config = configparser.ConfigParser()
            config.read(filepath)            
            return config
        elif os.path.isfile(alt_filepath):
            config = configparser.ConfigParser()
            config.read(alt_filepath)            
            return config
        else:
            raise Exception('No Config file, please add config.ini')


     


        
