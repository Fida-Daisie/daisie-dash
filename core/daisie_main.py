# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_login import LoginManager
from dash import dash, html, dcc, Input, Output

from .appStructure import AppStructure
from flask_login import current_user


from .authentification.User import User



class DaisieMain(dash.Dash):
    """The main application that extends Dash.

    Class variables:
    * app: Holds the global accessible instance of (singleton) object DaisieMain
    * custom_assets: Needs to be set to True if application uses a custom assets folder (and not default daisie assets)

    Relevant instance variables for control from outside:
    * authentification: Holds the authentification service used
    """
    ## Holds the global singleton instance of DaisieMain
    app = None
    # ## Global setting to allow custom assets (default when False: "/daisie/core/static/assets"). If True, take working directory as assets path.
    # custom_assets = False

    def __init__(self, *args, **kwargs):
        """Constructor
        

        Initialize DaisieMain.app to self.
        Calls constructor of Dash with given arguments.
        """
        DaisieMain.app = self
        
        
        server = Flask(__name__)
        ## Authentification service server. Must be an instance of 'IAuthentification' or None
        self.login_manager= LoginManager()
        self.login_manager.init_app(server)
        self.login_manager.session_protection = "strong"
        
        self.login_manager.secret_key = os.urandom(24)
        
        
        server.secret_key = os.urandom(24)
        kwargs['server'] = server
        
        if "meta_tags" in kwargs.keys():
            kwargs["meta_tags"].append(
                {"name": "viewport", "content": "width=device-width, initial-scale=1",}
            )
        else:
            kwargs["meta_tags"] = [{"name": "viewport", "content": "width=device-width, initial-scale=1",}]
        # meta_tags = []
        # meta_tags.append(
        #     {"name": "viewport", "content": "width=device-width, initial-scale=1",}
        # )

        # ToDo: Better understanding of importing styles, since the files below project folder will be imported in order of their name... jerkyness level >= maximum


        @self.login_manager.user_loader
        def load_user(user_id):
            return User.get(int(user_id))
        

        if "title" in kwargs.keys():
            ## Title of app
            self.title = kwargs.get('title')
            del kwargs['title']


        if "assets_folder" not in kwargs.keys():
            kwargs["assets_folder"] = os.getcwd()   
        super().__init__(*args, **kwargs)

        ## Holds the registered apps. Key: url/pathname, Value: Instance of DaisieApp
        self._apps = {}
        ## Holds the default DaisieApp
        self._default_app = None
        ## Holds the structure of the apps
        self.tree = AppStructure()
        ## Holds layout. Required for inherited logic from Dash (avoid external changes)
        self.layout = html.Div(
            [dcc.Location(id="url-out", refresh=False), dcc.Location(id="url-in", refresh=False),
            html.Div(id="page-content")],
            id="main-container",
        )
        self.daisie_navigators = []
    



    def create_navigator(self, **kwargs): 
        from ..apps import DaisieNavigator
        
        is_default = kwargs.get('is_default', True)
        navInstance = DaisieNavigator(kwargs)
        
        
        self.daisie_navigators.append(navInstance)
        self.register_app(navInstance, default_app=is_default)
        

    def update_navigator(self):
        for nav in self.daisie_navigators:
            nav.set_content()

    def GetApps(self):
        """Returns list of registered DaisieApps's"""
        return self._apps

    def GetDefaultApp(self):
        """Returns default DaisieApp instance"""
        return self._default_app

    def register_app(self, app, default_app=False):
        """Register an instance of class DaisieApp
        """
        
        # and the url doesn't occure
        if self.tree.full_url(app.id) not in self._apps.keys():
            self._apps.update({self.tree.full_url(app.id): app})

            if default_app == True:
                self._default_app = app
                self.app.tree.default_app_id = app.id
        else:
            raise Exception(f'The given url path ({app.id}) is already in by app.title({self._apps[app.url].title})')

    def set_validation_layout(self):
        """Creates and returns layout of all registered applications as list.
        """
        validation_layout = []
        validation_layout.append(self.layout)

        for app in self._apps.values():
            validation_layout.append(app.get_layout())

        ## Holds layout for validation. Required for inherited logic from Dash (avoid external changes)
        self.validation_layout = html.Div(validation_layout)

    def initiate_callbacks(self):
        """Callback registration for DaisieMain and iteratively (through all registered) call DaisieApp::register_callback()"""
        @self.callback(
            [Output("page-content", "children"),
            Output("url-out", 'pathname')],
            [Input("url-in", "pathname")])
        def display_page(pathname):
            app_to_display = None
            print(pathname)
            if pathname and pathname in self._apps.keys():
                    app_maybe_display = self._apps[pathname]
                    security = app_maybe_display.security
                    
                    if security:
                        if current_user.is_authenticated:
                            
                            app_to_display = app_maybe_display
                        else:
                            pathname = app_maybe_display.alternative
                            if pathname and pathname in self._apps.keys():
                                app_to_display=self._apps[pathname]     
                            else:
                                app_to_display=None
                    else:
                        app_to_display = app_maybe_display

            if not (app_to_display):
                pathname = self.tree.full_url(self.GetDefaultApp().id)
                app_to_display = self._default_app

            print(pathname)
            return [app_to_display.get_layout(), pathname]
            

        for app in self._apps.values():
            # ToDo: init page depending routes
            app.register_callbacks()
            for item in app._layout.collect_callbacks():
                item.register_callbacks()
            app._layout.register_callbacks()

    def showTree(self):
        self.tree.structure.show()