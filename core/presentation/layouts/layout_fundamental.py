# -*- coding: utf-8 -*-



# from . import DaisieComponent
from ... import DaisieMain

class LayoutFundamental(object): # no daisie component anymore
    """*DEPRECIATED* will not be registered anymore!
    Abstract class for DaisieHeader's"""

    def __init__(self, id, title=None):
        """Constructor. Set internal variables"""

        ## Holds the title text that should be displayed in the header
        self.title = title
        ## Holds the DaisieMain.app instance
        self.main_app = DaisieMain.app
        ## Id of Component. Should be unique in complete DaisieMain instance
        self.id = id


    def get_layout(self):
        pass


    def register_callbacks(self):
        pass