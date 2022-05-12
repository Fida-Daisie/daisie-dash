# -*- coding: utf-8 -*-

from . import LayoutFundamental

from dash import html

class LargeFooter(LayoutFundamental):
    """Default footer for Daisie (using FIDA logo/links/information)"""
    
    def __init__(self, id,      
            name = 'Finanz-Data GmbH', 
            contact_bar = {
                "Kontakt": "mailto:covid-19-simulator@fida.de",
                "Impressum": "https://www.fida.de/impressum",
                "Datenschutz": "https://www.fida.de/datenschutz"
            }
            ):

        super().__init__(id=id + '-footer')
        self.contact_bar = contact_bar
        self.name = name
    

    def get_columns_layout(self, headline, link, topics):
        return html.Div(className = 'footer-nav-columns', 
                            children=[html.Div(children=[                            
                                html.A(headline, href=link, className = 'footer-nav-headline'), 
                                html.Div(className='footer-nav-topics', children= [
                                    html.Div(html.A(display, href=link)) for display, link in topics.items()])
                            ])])

    def get_navigation(self):
        headlines = self.main_app.tree.get_pages()
        res = []
        for headline, rel_path in headlines.items():
                            topics = self.main_app.tree.get_subpages(rel_path)
                            link = self.main_app.tree.full_url(rel_path)
                            res.append(self.get_columns_layout(headline, link, topics))
        return html.Div(className= 'footer-navigator row', children = res)
        
                

    def get_legal(self):
        return html.Div(className= 'footer-legal row', children = [
                    html.Div(className=' text-left row footer-name',
                        children=[html.A(self.name)]   
                        ),
        
                    html.Div(className='row footer-contact',
                            children=[
                                html.Div(className='legal',
                                    children=[html.A(display, href=link, className='legal-text') for display, link in self.contact_bar.items()]
                                )
                            ])
        ]
        )

    def get_layout(self):
        #self._build_navbar()
        footer = html.Div(
                className='navigator-footer-body',
                children=[ self.get_navigation(),
                            self.get_legal()
                    
                
                        ]
            )

        return footer
