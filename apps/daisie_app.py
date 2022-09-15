# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod, abstractproperty
from ..core.daisie_main import DaisieMain
from ..core.appStructure import AppStructure
from ..core.presentation.components import DaisieComponent
from ..core.presentation.layouts.daisie_layout import DaisieLayout
from dash import html
class DaisieApp(DaisieComponent):
    """DaisieApp

    Abstract class to provide basic structure to daisie application
    """
    def __init__(self, id, **kwargs):
        """Constructor. Initialize members according to given values"""
        super().__init__(id)
        ## Holds DaisieMain.app (instance of Dash)
        # self.main_app = DaisieMain.app ### done by DaisieComponent
        ## ID of DaisieApp instance. Use this for app specific id's
        # self.id = id ### done by DaisieComponent
        ## Title of DaisieApp instance. (e.g. used in Navigator)
        self.title = kwargs.get('title')
        self.navigator_name = kwargs.get("navigator_name")
        if self.navigator_name is None:
            self.navigator_name = self.title
        ## URL path of DaisieApp instance
        self.url = kwargs.get('url')

        ## parent of this app
        self.parent = kwargs.get('parent', 'root')
        
        # register app for DaisieMain
        is_default = kwargs.get("default_app", False)
        self.main_app.register_app(self, default_app=is_default, no_display=kwargs.get('no_display', False))

        self.security = kwargs.get('security')
        self.alternative = kwargs.get('alternative')
        ## Description of DaisieApp. (e.g. used in Navigator)
        self.description = kwargs.get('description', '')
        
        ## Holds path to application image (e.g. used in navigation card)
        self.img_path = kwargs.get('img_path')

        k_layout=kwargs.get('kwargs_layout', dict()) # {'title': self.title}
        layout_class = kwargs.get('layout')
        if layout_class:
            layout = object.__new__(layout_class)
            layout.__init__(id=id, **k_layout)
            self._layout = layout
        else:
            header, footer, navtop, navleft, navright = kwargs.get("header"), kwargs.get("footer"), kwargs.get("NavTop"), kwargs.get("NavLeft"), kwargs.get("NavRight")
            self._layout = DaisieLayout(self.id, header=header, footer=footer, NavTop=navtop, NavLeft=navleft, NavRight=navright, **k_layout)

    def get_layout(self):
        """Getter for the whole layout (including content).
        """
        if self._layout is None:
            print('No valid layout id: ' + str(self.title))
        try:
            return self._layout.get_layout(content=self.set_content())
        except Exception as E:
            print(str(E)) # logging
            
        
    def set_content(self):
        """Abstract method to fill the content-container."""
        return html.Div()

    def register_callbacks(self):
        """Abstract method to register callbacks invoked by DaisieMain."""
        pass