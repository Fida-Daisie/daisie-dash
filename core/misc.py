import configparser
import os
import numpy as np
from pathlib import Path

class config_reader():
    def __init__(self):
        self.name = 'config.ini'

    def get_config(self):
        cwd = os.getcwd()
        # print(cwd)
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
            print('No Config file, please add config.ini \n Searched path:' + filepath)
            return None

def read_config_for_oauth():
    config = config_reader().get_config()

    try: 
        if (config["google-oauth"].get('client_id') is None or config["google-oauth"].get('client_id') == ""
            or config["google-oauth"].get('client_secret') is None or config["google-oauth"].get('client_secret') == ""):
            display_google = False
        else:
            display_google = True
    except KeyError as e:
        display_google = False

    try:
        if (config["github-oauth"].get('client_id') is None or config["github-oauth"].get('client_id') == ""
            or config["github-oauth"].get('client_secret') is None or config["github-oauth"].get('client_secret') == ""):
            display_github = False
        else:
            display_github = True
    except KeyError as e:
        display_github = False
    
    try:
        if (config["linkedin-oauth"].get('client_id') is None or config["linkedin-oauth"].get('client_id') == ""
            or config["linkedin-oauth"].get('client_secret') is None or config["linkedin-oauth"].get('client_secret') == ""):
            display_linkedin = False
        else:
            display_linkedin = True
    except KeyError as e:
        display_linkedin = False

    return np.array([display_google, display_github, display_linkedin])
