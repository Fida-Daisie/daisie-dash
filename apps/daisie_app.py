# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod, abstractproperty
from ..core.daisie_main import DaisieMain
from ..core.appStructure import AppStructure
from dash import html
class DaisieApp(ABC):
    """DaisieApp

    Abstract class to provide basic structure to daisie application
    """
    def __init__(self, id, **kwargs):
        """Constructor. Initialize members according to given values"""
        
        ## Holds DaisieMain.app (instance of Dash)
        self.main_app = DaisieMain.app
        ## ID of DaisieApp instance. Use this for app specific id's
        self.id = id
        ## Title of DaisieApp instance. (e.g. used in Navigator)
        self.title = kwargs.get('title')
        ## URL path of DaisieApp instance
        self.url = kwargs.get('url')
        ## parent of this app
        self.parent = kwargs.get('parent', '/home')
        # registering the app in the structure-tree
        self.main_app.tree.register_url(display=self.title, id=self.id, url=self.url, parent=self.parent, no_display=kwargs.get('no_display', False))
        self.security = kwargs.get('security')
        self.alternative = kwargs.get('alternative')
        ## Description of DaisieApp. (e.g. used in Navigator)
        self.description = kwargs.get('description', '')
        

        ## Holds path to application image (e.g. used in navigation card)
        self.img_path = kwargs.get('img_path')
        k_layout=kwargs.get('kwargs_layout', {'keywords': None})
        layout_class = kwargs.get('layout')
        layout = object.__new__(layout_class)
        layout.__init__(id=id, title=self.title, **k_layout)
        self._layout = layout
        
        self._content = kwargs.get('content')
        super().__init__()

    def get_layout(self):
        if self._layout is None:
            print('No valid layout id: ' + str(self.title))
        try:
            return self._layout.get_layout(content=self.set_content())
        except Exception as E:
            print(str(E)) # logging
            
        
    def set_content(self):
        return html.Div()

    def register_callbacks(self):
        """Abstract method to register callbacks invoked by DaisieMain"""
        pass