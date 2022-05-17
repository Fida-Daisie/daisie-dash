from daisie.core.presentation.layouts import DaisieLayout
from .header import SingleHeader

from .standard_footer_floating import StandardFooterFloating
from .nav import NavBarTop


class SimpleLayout(DaisieLayout):
    def __init__(self, id=None, title=None, **kwargs):
            header = SingleHeader(id=id, title=title)
            footer = StandardFooterFloating(id=id)
            nav = NavBarTop(id=id)
            super().__init__(id, title=title, header = header, footer=footer, NavTop=nav)


    

