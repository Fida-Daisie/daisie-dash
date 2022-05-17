# -*- coding: utf-8 -*-

from daisie.core.presentation.layouts.layout_fundamental import LayoutFundamental
from dash import html, dcc
import dash_bootstrap_components as dbc

class StandardFooterFloating(LayoutFundamental):
    """Default footer for Daisie (using FIDA logo/links/information)"""
    
    def __init__(self, id,      
            title = 'Finanz-Data GmbH', 
            contact_bar = {
                "contact": "mailto:daisie@fida.de",
                "impressum": "https://www.fida.de/impressum",
                "data-protection": "https://www.fida.de/datenschutz"
            }
    ):
        super().__init__(id=id + '-footer')
        
        self.contact_bar = contact_bar
        self.name = title
        self.className = 'footer-floating'
   

    def get_layout(self):
        footer = html.Div(
                    className="footer "+self.className,
                    id = self.id + "-standard-footer",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                    dcc.Link(self.name, href="https://www.fida.de", target="_blank", className="footer-link"), 
                                    ),
                                    width= {"size": 8}
                                ),
                                dbc.Col(
                                    html.Div(
                                        children=[
                                            dcc.Link('Datenschutz', href=self.contact_bar.get('data-protection'), target="_blank", className="footer-link footer-link-margin-left"),                                        
                                            dcc.Link('Impressum', href=self.contact_bar.get('impressum'), target="_blank", className="footer-link footer-link-margin-left"),
                                            dcc.Link('Kontakt', href=self.contact_bar.get('contact'), target="_blank", className="footer-link footer-link-margin-left"),
                                        ],
                                    ),
                                    width={"size": 4},
                                    style={"textAlign": "right"}
                                )
                            ],
                            justify="between",
                            align="center"
                        )
                    ]
                )         
            
        return footer
        