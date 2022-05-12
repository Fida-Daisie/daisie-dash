from . import LayoutFundamental
import dash_bootstrap_components as dbc
from dash import html



class DoubleHeader(LayoutFundamental):
    def __init__(self, id,  
            title=None, 
            logo_link='https://www.fida.de',
            header_right_bar = {
                "Kontakt": "mailto:covid-19-simulator@fida.de",
                "Impressum": "https://www.fida.de/impressum",
                "Datenschutz": "https://www.fida.de/datenschutz"
            
                },
            header_left_bar = { 'Finanz Data GmbH': 'https://www.fida.de',
                                 'Zu Uns' : 'https://www.google.com/maps/place/Finanz-DATA+GmbH,+Beratungs-+und+Softwarehaus/@50.9511865,10.7069452,16z/data=!4m5!3m4!1s0x0:0x16d6affed6c84597!8m2!3d50.9462478!4d10.7116551'
            }
            ):
        
        super().__init__(id=id + '-header', title=title)
        self.logo_link = logo_link
        self.header_right_bar = header_right_bar
        self.header_left_bar = header_left_bar

    def get_second_row_elments(self):
        return html.Div(className= 'header-second row', children = [
                        html.Div(className='row header-left-bar',
                            children=[
                                html.Div(className='header-second-left-bar row',
                                    children=[html.A(display, href=link, className='header-second-left-text') for display, link in self.header_left_bar.items()]
                                )
                            ])  
                        ,
        
                    html.Div(className='row header-right-bar',
                            children=[
                                html.Div(className='header-second-right-bar row',
                                    children=[html.A(display, href=link, className='header-second-right-text') for display, link in self.header_right_bar.items()]
                                )
                            ])
            ]
            )   


    def get_layout(self):
        

        search_bar = dbc.Row(
            [
            dbc.Col(dbc.Input(type="search", placeholder="Bitte geben Sie etwas ein")),
            dbc.Col(
                dbc.Button("Suche", className="ml-2"),
                width="auto",
                ),
        ],
        no_gutters=True, className="ml-auto flex-nowrap mt-3 mt-md-0", align='center',
        )
        return html.Div(className='report-header', children= [
                html.Div(children=[
                    html.Div(html.A(id=self.id + '_banner-logo', className="banner-logo", href=self.logo_link)),
                    html.Div(children=[search_bar], className='search-box')
                ], className='banner row'),
                html.Div(className='second-row', children=[self.get_second_row_elments()])
        ])

