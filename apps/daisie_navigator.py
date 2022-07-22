# -*- coding: utf-8 -*-

from . import DaisieApp
from dash import html

from ..core.presentation.components import DaisieNavigationCard

class DaisieNavigator(DaisieApp):
    """Navigator app for Daisie"""
            
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.cards_per_row = kwargs.get('cards_per_row', 4)
        self.navigator_root = kwargs.get('root', ['/home'])
        
    def set_content(self):
        navigation_cards = []
        if type(self.navigator_root) is not list:
            self.navigator_root = [self.navigator_root]
        app_list = self.main_app.GetApps().values()
        for app in app_list:
            if app.parent in self.navigator_root:
                if app is not self:
                    navigation_cards.append(DaisieNavigationCard(app=app, cards_per_row=self.cards_per_row).get_layout())
        
        return html.Div(
                    className="container-fluid content-row",
                    children=[html.Br(), html.Div(className="row", children=navigation_cards)],
                )
        
    def register_callbacks(self):
        pass