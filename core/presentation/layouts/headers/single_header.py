from ...components.daisie_component import DaisieComponent
import dash_bootstrap_components as dbc
from dash import html

class SingleHeader(DaisieComponent):
    def __init__(self, id, 
            title=None, 
            logo_link='https://www.fida.de',
            ):
        
        super().__init__(id=id + '-header', title=title)
        self.logo_link = logo_link
        


    def get_layout(self):
        header_layout = dbc.Row(children=[
                    dbc.Col(html.H1(self.title, className='header-title')),
                    #dbc.Col(html.A(id=self.id + '_banner-logo', className="banner-logo", href=self.logo_link))
                    html.Div(className='header-right',
                                children=[html.Div(html.A(id=self.id + '_banner-logo', className="banner-logo", href=self.logo_link))]
                            ),
                ], className='banner banner-row') # pl-4 pr-4')
         
    
        return header_layout

