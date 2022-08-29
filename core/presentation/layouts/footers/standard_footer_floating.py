# -*- coding: utf-8 -*-

from ...components.daisie_component import DaisieComponent
from dash import html, dcc
import dash_bootstrap_components as dbc

class StandardFooterFloating(DaisieComponent):
    """Default footer for Daisie (using FIDA logo/links/information)"""
    
    def __init__(self, id,      
            title = 'Finanz-Data GmbH', 
            contact_bar = {
                "contact": "mailto:covid-19-simulator@fida.de",
                "impressum": "https://www.fida.de/impressum",
                "data-protection": "https://www.fida.de/datenschutz"
            }
    ):
        super().__init__(id=id + '-footer')
        
        self.contact_bar = contact_bar
        self.name = title
        self.className = 'standard-footer-body-floating'
   

    def get_layout(self):
        footer = html.Div(children=[
                html.Div(
                    className=self.className,
                    id = self.id + "-standard-footer-body",
                    children=[
                        dbc.Row(
                            [
                            dbc.Col(html.Div(self.name, 
                                ),
                                width= {"size": 9}
                            ),
                            dbc.Col(
                                html.Div(
                                    children=[
                                        dcc.Link('Kontakt', href=self.contact_bar.get('contact'), style = {"margin-left": "1rem"}, className="footer-link"),
                                        dcc.Link('Impressum', href=self.contact_bar.get('impressum'),style = {"margin-left": "1rem"}, className="footer-link"),
                                        dcc.Link('Datenschutz', href=self.contact_bar.get('data-protection'), style = {"margin-left": "1rem"}, className="footer-link"),
                                    ],
                                    className= "row",
                                    style= {
                                        "margin-left": "auto",
                                        "margin-right": 0
                                    }
                                ),
                                width="auto"
                            )
                            # dbc.Col(dcc.Link('Kontakt', href=self.contact_bar.get('contact')), width=1),
                            # dbc.Col(dcc.Link('Impressum', href=self.contact_bar.get('impressum')), width=1),
                            # dbc.Col(dcc.Link('Datenschutz', href=self.contact_bar.get('data-protection')), width=1),
                            ],
                            justify="between"
                        )
                    ]
                )],
                className=self.className+"-padding"
            )

        return footer
        