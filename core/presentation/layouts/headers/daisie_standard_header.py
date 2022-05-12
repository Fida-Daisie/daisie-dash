# -*- coding: utf-8 -*-

from . import LayoutFundamental

from dash import html, dcc


class StandardHeader(LayoutFundamental):
    """Default header for Daisie (using FIDA logo/links/information)"""
    def __init__(self, id, 
        title=None, 
        logo_link='https://www.fida.de',
        contact_bar = {
            "Kontakt": "mailto:covid-19-simulator@fida.de",
            "Impressum": "https://www.fida.de/impressum",
            "Datenschutz": "https://www.fida.de/datenschutz"
        }
    ):
        super().__init__(id=id + '-header', title=title)
        self.logo_link = logo_link
        self.contact_bar = contact_bar
    
    # def _build_navbar(self):
    #     self.__navbar = html.Div(className='collapse navbar-collapse', id=self.id + '_navbarResponsive',
    #     children=[
    #         html.Ul(className='navbar-nav ml-auto', children=[
    #             html.Li(className='nav-item', children=[
    #                 #ToDo: select dedicated Pages from Daisie
    #                 dcc.Link(className='nav-link', href='#', children=['Navigator'])
    #             ])
    #         ])
    #     ])

    def get_layout(self):
        #self._build_navbar()
        banner = html.Div(
                className='banner',
                children=[
                    html.Div(className='scalable',
                    children=[
                        html.Div(className='row',
                        children=[
                            html.Div(className='col-12 text-right',
                            children=[
                                html.Div(className='legal',
                                    children=[html.A(display, href=link) for display, link in self.contact_bar.items()]
                                )
                            ])
                        ]),
                        html.Div(className='pl-4 pr-4 banner-row',
                        children=[
                            html.Div(className='header-right',
                                children=[html.Div(html.A(id=self.id + '_banner-logo', className="banner-logo", href=self.logo_link))]
                            ),
                            html.H2(id=self.id + '_banner-title', className='header-left',
                            children=[
                                dcc.Link(children=self.title, href=self.main_app.GetDefaultApp().url)
                            ]),
                        ])
                    ])
                ]
            )

        return html.Header(className='site-header',
            children=[
                html.Div(
                    id="overlay-landscape",
                    children=[
                        html.Div(
                            className="content",
                            children=["Die App bitte im Querformat verwenden."]
                        )
                    ]
                ),
                banner
            ])

