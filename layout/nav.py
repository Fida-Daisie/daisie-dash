from dash import html
import dash_bootstrap_components as dbc

from daisie.core.presentation.layouts.layout_fundamental import LayoutFundamental

class NavBarTop(LayoutFundamental):  # Getting from Abstract base class - possibly change this to DaisieHeader? (Since it would be in the right place)
    """Nested dropdown for a top-bound navigation component"""

    def __init__(self, id, title:str=None, logo_link = False, classname = "NavBar"):
        super().__init__(id=id+"navTop", title=title)
        self.navColor = 'secondary'
        self.id = id
        self.logo = None
        self.classname = classname




    def get_layout(self):
        headlines = self.main_app.tree.get_pages()
        bar = [
            dbc.NavItem(
                dbc.NavLink(self.main_app.tree.get_home().get("title"), href=self.main_app.tree.get_home().get("url"), active="exact")
            ),
            
        ]
        i = 1
        for headline, rel_path in headlines.items():
                            topics = self.main_app.tree.get_subpages(rel_path)
                            link = self.main_app.tree.full_url(rel_path)
                            bar.append(self.get_bar_element(i, headline, link, topics))
                            i+=1
        # bar = html.Div(children=[self.get_bar_element(headlines,items) 
        #     for headlines, items in self.navStructure.items()], className="NavBarTop row")

        return html.Div(
            html.Div(
                children=[
                    html.Div(""),
                    self.logo,
                    dbc.Nav(children=bar,pills=True)
                ],
                    className=self.classname),
                className='NavBottom')

    def get_bar_element(self, i, headline, link, topics):
        if topics=={}:
            return dbc.NavItem(
                            dbc.NavLink(headline, href=link, active="exact")
                            )
        else: 
            return self.generateNestedDropdown(title=headline, structure=topics)

            




    def generateTopLevelOptions(self, structure:dict): # This is for generating the nested dropdowns
        items = []
        for key, value in structure.items():
            items.append(dbc.DropdownMenuItem(header=key, children=self.generateNestedDropdown(key, value)))

        return items

    def generateNestedDropdown(self, title: str, structure:dict): # This is for generating dropdownception
        #TODO: Check if our passed structure is dict[str,str] or dict[str, dict[...]] - For the latter case we can call this method recursively for the true dropdownception experience.
        
        nestedDropdownItems = []
        full_url = self.main_app.tree.full_url(self.id)
            
        for key, value in structure.items():
            active = (full_url==value)
            nestedDropdownItems.append(dbc.DropdownMenuItem(key, href=value, active=active, disabled=active)) #header=key, 

        nestedDropdown = dbc.DropdownMenu(
            label=title,
            id=self.id+"-nestedDropdown-"+title, # TODO: Check if this causes Problems when title contains special characters
            children=nestedDropdownItems,
            group=True,
            nav=True,
            in_navbar=True
            #color=self.navColor
        )
        
        return nestedDropdown

