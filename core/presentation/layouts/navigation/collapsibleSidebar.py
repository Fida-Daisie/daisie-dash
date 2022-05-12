# -*- coding: utf-8 -*-
from ..layout_fundamental import LayoutFundamental

from dash import html, Input, Output, State
import dash_bootstrap_components as dbc

class CollapsibleSidebar(LayoutFundamental):    
    def __init__(self, id):
        self.number_of_headlines = 0
        super().__init__(id=id + '-NavSide')
        

    def get_sub_menu(self, i, headline, link, topics):
        if not topics:
            return html.Div(children=[
                    dbc.Button(
                        headline,
                        href=link,
                        id=self.id + "-collapse-button" + str(i),
                        className="mb-3",
                        #color="primary",
                        n_clicks=0,
                    ),

                    dbc.Collapse(
                        html.Div(),
                        # dbc.Nav([
                        #     dbc.NavLink(display, href=link, active="exact") for display, link in topics.items()
                        #     ],
                        #     vertical=True,
                        #     pills=True),
                        
                        id=self.id + "-collapse" + str(i)
                    )
            ])
        return html.Div(children=[
                    dbc.Button(
                        headline,
                        id=self.id + "-collapse-button" + str(i),
                        className="mb-3",
                        #color="primary",
                        n_clicks=0,
                    ),
                    dbc.Collapse(
                        dbc.Nav([
                            dbc.NavLink(display, href=link, active="exact") for display, link in topics.items()
                            ],
                            vertical=True,
                            pills=True),
                        
                        id=self.id + "-collapse" + str(i)
                    )
                ], className='sidebar-submenu-collapse')


    def get_navigation(self):
        headlines = self.main_app.tree.get_pages()
        self.number_of_headlines = len(headlines.keys())
        res = []
        i = 1
        for headline, rel_path in headlines.items():
                            topics = self.main_app.tree.get_subpages(rel_path)
                            link = self.main_app.tree.full_url(rel_path)
                            res.append(self.get_sub_menu(i, headline, link, topics))
                            i+=1
        return html.Div(className= 'left-navigator', children = res)
                

    def get_layout(self):
        return self.get_navigation()



 

    def register_callbacks(self):
        if self.number_of_headlines > 0:
            for i in range(self.number_of_headlines):
                @self.main_app.callback(Output(self.id + "-collapse" + str(i+1), 'is_open'),
                    [Input(self.id + "-collapse-button" + str(i+1), 'n_clicks')],
                    [State(self.id + "-collapse" + str(i+1), 'is_open')])
                def toggle_collapse(n, is_open):
                    if n:
                        return not is_open
                    return is_open
        