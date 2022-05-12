# -*- coding: utf-8 -*-
from ..layout_fundamental import LayoutFundamental
from dash import html

import dash_bootstrap_components as dbc

class BasicSidebar(LayoutFundamental):    
    def __init__(self, id):
        super().__init__(id=id + '-NavSide')

    def get_sub_menu(self, headline, link, topics):
        return html.Div(children=[
                                html.A(headline, href =link, className = 'left-nav-headline'), 
                                dbc.Nav([
                                    dbc.NavLink(display, href=link, active="exact") for display, link in topics.items()
                                    ],
                                    vertical=True,
                                    pills=True),
                            ], className='sidebar-submenu')

    def get_navigation(self):
        headlines = self.main_app.tree.get_pages()
        res = []
        for headline, rel_path in headlines.items():
                            topics = self.main_app.tree.get_subpages(rel_path)
                            link = self.main_app.tree.full_url(rel_path)
                            res.append(self.get_sub_menu(headline, link, topics))
        return html.Div(className= 'left-navigator', children = res)
                

    def get_layout(self):
        # sidebar = html.Div(
        #         className='sidebar-body',
        #         children=[ self.get_navigation(),
        #                 ]
        #     )
        return self.get_navigation()
