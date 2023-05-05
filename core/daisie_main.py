# -*- coding: utf-8 -*-
import os
from flask import Flask, send_file
from flask_login import LoginManager, current_user
from dash import dash, html, dcc, Input, Output, State
from oauthlib.oauth2 import WebApplicationClient
from datetime import datetime
from xml.dom.minidom import Document, Element, Text
from io import BytesIO

from .appStructure import AppStructure

from .authentification.User import User
from .authentification.routes import google_routes, github_routes, linkedin_routes

from .misc import config_reader, read_config_for_oauth

class DaisieMain(dash.Dash):
    """The main application that extends Dash.

    Class variables:
    * app: Holds the global accessible instance of (singleton) object DaisieMain

    Relevant instance variables for control from outside:
    * authentification: Holds the authentification service used
    """
    ## Holds the global singleton instance of DaisieMain
    app = None

    def __init__(self, *args, **kwargs):
        """Constructor
        

        Initialize DaisieMain.app to self.
        Calls constructor of Dash with given arguments.
        """
        DaisieMain.app = self
        
        self.__lastModified = str(datetime.now().date())
        
        server = Flask(__name__)

        ## bind robots.txt if in working directory
        if os.path.exists('./robots.txt'): # os.getcwd()+
            print("robots.txt found at "+os.path.abspath('./robots.txt'))
            @server.route("/robots.txt")
            def static_robotstxt():
                return send_file(os.path.abspath('./robots.txt'))

        ## Authentification service server. Must be an instance of 'IAuthentification' or None
        self.login_manager = LoginManager()
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

        # ToDo: Better understanding of importing styles, since the files below project folder will be imported in order of their name... jerkyness level >= maximum


        @self.login_manager.user_loader
        def load_user(user_id):
            return User.get(int(user_id))
        

        if "title" in kwargs.keys():
            ## Title of app
            self.title = kwargs.get('title')
            # del kwargs['title']


        if "assets_folder" not in kwargs.keys():
            kwargs["assets_folder"] = os.getcwd()
        
        self.oauth = kwargs.get("oauth", False)
        if "oauth" in kwargs.keys():
            kwargs.pop("oauth")

        self.black_screen=kwargs.get('black_screen', True)
        if "black_screen" in kwargs.keys():
            kwargs.pop("black_screen")

        super().__init__(*args, **kwargs)

        ## Holds all DaisieComponents. Used to register their callbacks
        self._components = []
        ## Holds the default DaisieApp
        self._default_app = None
        ## Holds the structure of the apps
        self.tree = AppStructure()
        ## Holds layout. Required for inherited logic from Dash (avoid external changes)
        self.set_persistence_layout()
                
        self.daisie_navigators = []
        
        # oauth
        self.config_file = config_reader().get_config()
        if self.config_file is None or all(~read_config_for_oauth()):
            self.oauth = False
        if self.oauth:
            self.google_client = WebApplicationClient(self.config_file['google-oauth'].get('client_id'))
            self.github_client = WebApplicationClient(self.config_file['github-oauth'].get('client_id'))
            self.linkedin_client = WebApplicationClient(self.config_file['linkedin-oauth'].get('client_id'))

            google_callback_url = self.config_file['google-oauth'].get('callback_url')
            github_callback_url = self.config_file['github-oauth'].get('callback_url')
            linkedin_callback_url = self.config_file['linkedin-oauth'].get('callback_url')
            self.callback_urls = {"google":google_callback_url, "github":github_callback_url, "linkedin":linkedin_callback_url}


    def create_navigator(self, **kwargs): 
        """Creates a DaisieNavigator app and registers it.
        """
        from ..apps import DaisieNavigator
        
        # is_default = kwargs.get('is_default', True)
        navInstance = DaisieNavigator(**kwargs)
        
        self.daisie_navigators.append(navInstance)
        # self.register_app(navInstance, default_app=is_default)
        

    def update_navigator(self):
        """Call this at the end of main.py to initialize the content of the navigators after every app has been registered.
        """
        for nav in self.daisie_navigators:
            nav.set_content()

    def GetApps(self):
        """Returns list of registered DaisieApps's"""
        return self.tree.get_apps()

    def GetDefaultApp(self):
        """Returns default DaisieApp instance"""
        return self._default_app

    def register_app(self, app, default_app=False, no_display=False, no_sitemap=False):
        """Register an instance of class DaisieApp
        """
        if app.url not in self.tree.get_apps().keys():
            self.tree.register_app(app, default_app=default_app, no_display=no_display, no_sitemap=no_sitemap)
            if default_app == True:
                self._default_app = app
                self.app.tree.default_app_id = app.id
        else:
            raise Exception(f'The given url path ({app.id}) is already in by app.title({self.tree.get_apps()[app.url].title})')

    def set_validation_layout(self):
        """Creates and returns layout of all registered applications as list.
        """
        validation_layout = []
        validation_layout.append(self.layout)

        for app in self.tree.get_apps().values():
            validation_layout.append(app.get_layout())

        ## Holds layout for validation. Required for inherited logic from Dash (avoid external changes)
        self.validation_layout = html.Div(validation_layout)

    def set_persistence_layout(self, content=None, place="above"):
        if place not in ["above", "below", "top", "bottom"]:
            raise ValueError("\"place\" must be one of above, below, top, bottom")
        #if content:
        self.layout = html.Div(html.Div(
            [
                dcc.Location(id="url-out", refresh=False), 
                dcc.Location(id="url-in", refresh=False),
                dcc.Store(id="last-url", storage_type="session"), # TODO: Save language settings for default app in Browser Cache
                content if place in ["above", "top"] else None,
                html.Div(id="page-content"),
                content if place in ["below", "bottom"] else None,
                html.Div(html.Div("Bitte im Querformat darstellen!"), className="black-screen", style={"display": "none"}) if self.black_screen else None
            ],
            className = "main-container",
            id = "main-container"
        ), className="base-background")
    
    def initiate_callbacks(self):
        """Callback registration for DaisieMain and iteratively (through all registered) call DaisieApp::register_callback()"""
        @self.callback(
            [
                Output("page-content", "children"),
                Output("url-out", 'href'),
                Output("last-url", "data")
            ],
            [
                Input("url-in", "pathname")
            ],
            [
                State("url-in", "href"),
                State("last-url", "data")
            ]
        )
        def display_page(pathname, url, last_url):
            if self.oauth and pathname in self.callback_urls.values():
                if pathname == self.callback_urls["google"]:
                    google_routes(self.app, url)
                elif pathname == self.callback_urls["github"]:
                    github_routes(self.app, url)
                elif pathname == self.callback_urls["linkedin"]:
                    linkedin_routes(self.app, url)
                        
                return [self.choose_app(last_url), last_url, dash.no_update]
            
            else:    
                return [self.choose_app(pathname), pathname, pathname]

        # register component callbacks, i. e. all apps, layouts & components
        for component in self._components:
            component.register_callbacks()

    def choose_app(self, pathname):
        app_to_display = None
            
        if pathname and pathname in self.tree.get_apps().keys():
                app_maybe_display = self.tree.get_apps()[pathname]
                security = app_maybe_display.security
                
                if security:
                    if current_user is not None and current_user.is_authenticated:
                        app_to_display = app_maybe_display
                    else:
                        pathname = app_maybe_display.alternative
                        if pathname and pathname in self.tree.get_apps().keys():
                            app_to_display=self.tree.get_apps()[pathname]     
                        else:
                            app_to_display=None
                else:
                    app_to_display = app_maybe_display

        if not (app_to_display):
            pathname = self.tree.full_url(self.GetDefaultApp().id)
            app_to_display = self.GetDefaultApp()

        return app_to_display.get_layout()

    def showTree(self):
        """Prints all registered apps and their hierarchy.
        """
        self.tree.structure.show()

    def create_sitemap(self):
        """Creates from hierarchy tree a xml sitemap, that is accessible under "/sitemap.xml".
        """
        base_url = self.config_file["url"].get("base_url")
        rel_urls = self.tree.get_urls_for_sitemap()
        
        if base_url and len(rel_urls):
            urls = [base_url+url for url in rel_urls]
        else:
            print("Sitemap could not be created! base_url or app urls are missing.")
            return
        
        

        doc = Document()

        urlset = doc.createElement("urlset")
        urlset.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        
        for url in urls:
            url_el = Element("url")
            
            loc = Element("loc")
            loc_text = Text()
            loc_text.appendData(url)
            loc.appendChild(loc_text)
            
            lastmod = Element("lastmod")
            lastmod_text = Text()
            lastmod_text.appendData(self.__lastModified)
            lastmod.appendChild(lastmod_text)
            
            url_el.appendChild(loc)
            url_el.appendChild(lastmod)
            
            urlset.appendChild(url_el)
        
        doc.appendChild(urlset)

        @self.server.route("/sitemap.xml")
        def static_sitemap():
            return send_file(BytesIO(doc.toprettyxml(encoding="utf-8")), mimetype="application/xml")