# -*- coding: utf-8 -*-

import dash_bootstrap_components as dbc
from dash import html, dependencies, callback_context

from . import DaisieComponent

class DaisieAccordion(DaisieComponent):
    """Accordion item"""
    def __init__(self, id, content=None, title=None, is_open=False):
        """Constructor. Sets internal variables
        
        @param id: Id of daisie app
        @param content: Content that needs to be displayed (can be either single dash conform element or list of dash conform elements)
        @param title: Text that has to be displayed as accordion title
        @param is_open: Property whether accordion should be open in initial state
        """
        super().__init__(id=self._createID(id + "-accordion-"))
        ## Id of toggle item
        self.__toggle_name = self.id + "-toggle"
        if type(content) is list:
            self._content = content
        else:
            self._content = []
            self._content.append(content)
        self.__title = title
        self._is_open = is_open

    def get_layout(self):
        """Return accordion element including content"""
        layout = html.Div(
            id=self.id,
            className="accordion",
            children=[
                html.Div(
                    className="card",
                    children=[
                        html.Div(
                            className="card-header",
                            children=[
                                html.H5(
                                    id=self.__toggle_name,
                                    className="headline",
                                    children=[
                                        html.Span(self.__title),
                                        html.Span(
                                            "+" if self._is_open else "-",
                                            id=self.id + "-state-icon",
                                            className="accordion-state-icon",
                                        ),
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="card-body",
                            children=[
                                dbc.Collapse(
                                    children=self._content,
                                    id=self.id,
                                    is_open=self._is_open,
                                ),
                            ],
                        ),
                    ],
                )
            ],
        )

        return layout

    def append(self, content):
        """Append dash conform element to accordion content list"""
        self._content.append(content)

    def register_callbacks(self):
        """Register user interaction callbacks (e.g. to open/close accordion)"""
        @self.main_app.callback(
            [
                dependencies.Output(f"{self.id}", "is_open"),
                dependencies.Output(f"{self.id}-state-icon", "children"),
            ],
            [
                dependencies.Input(f"{self.id}-toggle", "n_clicks")
            ],
            [
            dependencies.State(f"{self.id}", "is_open")
            ],
        )
        def toggle_accordion(n_clicks, is_open):
            ctx = callback_context

            if not ctx.triggered:
                button_id = 'No clicks yet'
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if button_id == self.__toggle_name:
                if self._is_open:
                    self._is_open = not(self._is_open)
                    return False, "+"
                else:
                    self._is_open = not(self._is_open)
                    return True, "-"
            else:
                return self._is_open, '-' if self._is_open else '+'
