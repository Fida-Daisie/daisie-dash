# -*- coding: utf-8 -*-
import  os
from oauthlib.oauth2 import WebApplicationClient
from .core.misc import config_reader

from .core import DaisieMain
# initialize main app
daisie_main = DaisieMain(__name__, 
                title='Daisie Minimal App',
                assets_folder = os.getcwd() + f'/{__package__}'
            )
img = '/assets/core/static/assets/img/FIDA1.jpg'
# initialize Navigator instance

config = config_reader().get_config()
client_id = config['oauth'].get('client_id')        
daisie_main.client = WebApplicationClient(client_id)


daisie_main.create_navigator( 
    title='Showcase-Apps', 
    id = 'showcase-nav', 
    url='/showcase', 
    root=['showcase-nav'], 
    img_path=img,
    is_default=False)

daisie_main.create_navigator( 
    title='Baukasten', 
    id = 'baukasten', 
    url='/baukasten', 
    root=['baukasten'], 
    img_path=img,
    is_default=False,
    security='admin',
    )

daisie_main.create_navigator( 
    title='Reports', 
    id = 'reports', 
    url='/reports', 
    root=['reports'], 
    img_path=img,
    is_default=False)




#creates all app instances
from .apps.app_list import create_app_instances 
create_app_instances(daisie_main)

# Flask routes for login with google oauth
from .routes.oauth import oauth_routes
oauth_routes(daisie_main)


#print(daisie_main._apps.keys())

#daisie_main.showTree()

# Update the Navigator Layout to make sure, all navigation cards are generated/all apps are registered
daisie_main.update_navigator()

# Collect the layouts from all apps
daisie_main.set_validation_layout()

# traverse through the apps and register all callbacks
daisie_main.initiate_callbacks()

#print(daisie_main.tree.get_dict_for_breadcrumbs('excel-app'))

# server variable needed for gunicorn or AWS
server = daisie_main.server
# application = server
# app = application


# run debug server for local execution under http://127.0.0.1:8051
if __name__ == '__main__':
    daisie_main.run_server(debug=True, host="127.0.0.1", port=5000, ssl_context = "adhoc")
    