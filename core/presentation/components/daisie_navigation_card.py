# -*- coding: utf-8 -*-

from . import DaisieComponent
from dash import html, dcc

class DaisieNavigationCard(DaisieComponent):
    """Navigation card.
    
    Used in DaisieNavigationLayout.
    """
    def __init__(self, app, cards_per_row = 4, id=None, lang="de"):
        """Constructor. Initialize internal variables"""

        ## Holds the via constructor delivered instance of DaisieApp
        self.app = app
        self.col_width = str(int(12 / cards_per_row))
        self.lang = lang

        super().__init__(id=id)
        # if self.app.img_path is None:          
        #     self.__img_path = "/assets/daisie/core/static/assets/img/FIDA1.jpg"
        # else:
        self.__img_path = self.app.img_path

    def get_layout(self):
        """Overloaded method to return component specific layout.
        """
        if self.lang == "de":
            button_text = "Öffnen" # self.app.title
        elif self.lang == "en":
            button_text = "Open"
        else:
            raise ValueError("Other language than de and en are not supported")

        layout = html.Div(className='navigation-card col-' + self.col_width,
        children=[
            html.Div(className='topleftsnippet'),
            html.Div(className='card h-100',
            children=[
                html.Img(className='card-img-top', src=self.__img_path),
                html.Div(className='card-body',
                children=[
                    html.H4(className='text-primary card-title',
                    children=[self.app.navigator_name]),
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