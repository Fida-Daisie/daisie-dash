# -*- coding: utf-8 -*-

from . import DaisieComponent
from ... import DaisieMain
from dash import html, dcc

class DaisieNavigationCard(DaisieComponent):
    """Navigation card.
    
    Used in DaisieNavigationLayout.
    """
    def __init__(self, app, id=None):
        """Constructor. Initialize internal variables"""

        ## Holds the via constructor delivered instance of DaisieApp
        self.app = app
        super().__init__(id=id)
        if self.app.img_path is None:          
            self.__img_path = "/assets/daisie/core/static/assets/img/FIDA1.jpg"
        else:
            self.__img_path = self.app.img_path

    def get_layout(self):
        button_text = "Öffnen" # self.app.title
        """Overloaded method to return component specific layout.
        """
        layout = html.Div(className='col-md-3 mb-2 navigation-card',
        children=[
            html.Div(className='topleftsnippet'),
            html.Div(className='card h-100',
            children=[
                html.Img(className='card-img-top', src=self.__img_path),
                html.Div(className='card-body',
                children=[
                    html.H4(className='text-primary card-title',
                    children=[self.app.title]),
                    html.P(className='card-text',
                    children=[self.app.description])
                ]),
                html.Div(className='card-footer',
                children=[
                    html.Div([
                        html.Div([
                            dcc.Link(button_text, className='btn btn-outline-secondary', 
                            href=self.app.main_app.tree.full_url(self.app.id), refresh=False)
                        ], className="col-8", style={"textAlign": "center"})
                    ], className="justify-content-center row")
                ])
            ]),
            html.Div(className='bottomrightsnippet'),
        ])       

        return layout

    def register_callbacks(self):
        pass