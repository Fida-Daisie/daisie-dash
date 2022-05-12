from dash import dcc, html

from .daisie_component import DaisieComponent

class Breadcrumbs(DaisieComponent):
    
    def __init__(self, id, text_color=None):
        
        
        super().__init__(id=self._createID(id + "-breadcrumbs1"))
        self.text_color = text_color 
        self.display_and_links = self.main_app.tree.get_dict_for_breadcrumbs(id)
        
        
    def get_layout(self):
        breadcrumbs_list = [html.Span(
                                title="Sie sind hier:",
                                children=[
                                    "Sie sind hier: "
                                ],
                            ),]


        for key, display_link in enumerate(self.display_and_links):
            breadcrumbs_list.extend(self.get_elment_layout(key, display_link))


        return html.Div(children=breadcrumbs_list)
                    
        

    def get_elment_layout(self, key, display_link):
        dict_length = len(self.display_and_links)
        display = list(display_link.keys())[0]
        link = list(display_link.values())[0]
        bc_elments = [html.I(
                    className="fa fa-caret-right",
                    children=[],
                )]
        if dict_length - 1 > key:
            bc_elments.append(dcc.Link(
                    title="Link zur Seite:" + display,
                    href=link,
                    children=[
                        display
                    ],
                    className="breadcrumb-entry"
                )) 
        else:   
            bc_elments.append( 
                html.A(
                    title="diese Seite:" + display,
                    style={
                        "cursor": "default",
                        "textDecoration": "none",
                        #"color": self.text_color,
                        },
                        children=[
                            display
                            ],
                        className="breadcrumb-entry"
                ))
        return bc_elments
                                                                                    
    def register_callbacks(self):
        pass