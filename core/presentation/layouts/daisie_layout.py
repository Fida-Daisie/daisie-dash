from .layout_fundamental import LayoutFundamental


from dash import html
import dash_bootstrap_components as dbc

class DaisieLayout(LayoutFundamental):
    """Abstract class for layout's"""
    def __init__(self, id, title,  header=None, footer=None, NavTop=None, NavLeft=None, NavRight=None, **kwargs):
        """Constructor. Initializes variables according to given parameter"""
        super().__init__(id=id, title=title)
        self.header = header 
        self.footer = footer
        self.NavTop = NavTop
        self.NavRight = NavRight
        self.NavLeft = NavLeft
        self.content = kwargs.get('content', [])
        self.backgroundClass = kwargs.get('backgroundClass', 'base-background')
        self.mainContainerClass = kwargs.get('mainContainerClass', 'main-container')
        self.contentContainerClass = kwargs.get('contentContainerClass', 'content-container')
        self.bodyContainerClass = kwargs.get('bodyContainerClass', 'body-container')
        self.navLeftClass = kwargs.get('navLeftClass', 'NavLeft')
        self.navRightClass = kwargs.get('navRightClass','NavRight')


    def header_layout(self):
        if self.header:
            return self.header.get_layout()
        else:
            return None
   
    def footer_layout(self):
        if self.footer:
            return self.footer.get_layout()
        else:
            return None

    def NavTop_layout(self):
        if self.NavTop:
            return self.NavTop.get_layout()
        else:
            return None
    
    def NavRight_layout(self):
        if self.NavRight:
            return dbc.Col(self.NavRight.get_layout(), className =self.navRightClass, width=2.5)
        else:
            return None    
    
    def NavLeft_layout(self):
        if self.NavLeft:
            return dbc.Col(self.NavLeft.get_layout(), className=self.navLeftClass, width=2.5)
        else:
            return None

    def get_layout(self, content):
        # padding = None
        # if self.footer:
        #         padding = html.Div(className=self.footer.get('className', 'daisie-footer') + "-padding")
        return html.Div(className=self.backgroundClass, children=[
                    html.Div(className=self.mainContainerClass, children=[
                        self.header_layout(),
                        self.NavTop_layout(),
                        dbc.Row(
                                [
                                    self.NavLeft_layout(),
                                    dbc.Col(content, className=self.contentContainerClass,
                                        id = self.id + "-content-container"
                                    ),
                                    self.NavRight_layout()
                                ],
                                className=self.bodyContainerClass,
                                id = self.id + "-body-container"
                            ),
                        # padding,
                        self.footer_layout()
                    ],
                    id = self.id + "-main-container"
                    ),
                    html.Div(html.Div("Bitte im Querformat darstellen!"), className="black-screen")
                ],
                id = self.id + "-background"
                )
        
    def collect_callbacks(self):
        callback_list=[]
        if self.header:
            callback_list.append(self.header)
        if self.footer:
            callback_list.append(self.footer)
        if self.NavLeft:
            callback_list.append(self.NavLeft)
        if self.NavRight:
            callback_list.append(self.NavRight)
        if self.NavTop:
            callback_list.append(self.NavTop)
        return callback_list

    def register_callbacks(self):
        pass

