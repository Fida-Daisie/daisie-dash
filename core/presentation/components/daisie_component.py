# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from itertools import count

from ... import DaisieMain

class DaisieComponent(ABC):
    """Top abstract class for any daisie specific layout component.
    """
    _id_counter = count(0)

    def _createID(self, id):
        """*DEPRECATED*
        Protected function to return a unique id by adding a global counter to 'id'
        """
        return str(id) + str(next(self._id_counter))

    def __init__(self, id):
        """Constructor to setup 'main_app' and 'id'.
        Registration of component callbacks is done here.
        """

        ## Holds the DaisieMain.app instance
        self.main_app = DaisieMain.app
        ## Id of Component. Should be unique in complete DaisieMain instance
        self.id = id
        ## Callbacks of components get registered in DaisieMain, when thy are created
        self.main_app._components.append(self)

    @abstractmethod
    def get_layout(self):
        """Abstract method to return the component specific layout"""
        pass

    @abstractmethod
    def register_callbacks(self):
        """Abstract method to implement the component specific callbacks"""
        pass