
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State

from itertools import count

from . import DaisieComponent

class ComponentWithHelpText(DaisieComponent):
    """Generalized class that supports a help text Modal popup when clicked on a button.
    """
    __gcounter = count(0)

    def __init__(self, id, name, helpText, style={}, subComponent=html.Div([])):
        """Constructor

        @input id: Daisie component specific id
        @input name: Text that needs to be displayed as header of this element (html.P-Element). Help button will be displayed next to it. If 'None', then subComponent is displayed instead.
        @input helpText: Text that is displayed in Modal when help button is clicked.  
        @input style: Style of the html.Div which then holds the single elements.
        @input subComponent: Single child component that is being displayed below header (unless name is 'None')
        """
        self._counter = next(self.__gcounter)
        super().__init__(id)

        self._layoutDiv = self.__initDiv(name, helpText, style, subComponent)

    def __initDiv(self, name, helpText, _style, subComponent):
        return html.Div(
            style=_style,
            children=[
                html.Div(
                        className="daisie-helptext-container",
                        children=[
                            html.P(f"{name}:") if name else subComponent,
                            dbc.Button("?", id=f'open{self._counter}', className="btn btn-primary daisie-help-btn"),
                            dbc.Modal([
                                dbc.ModalHeader(f"{name}:" if name else ""),
                                dbc.ModalBody(dcc.Markdown(f'{helpText}')),
                                dbc.ModalFooter(
                                    dbc.Button("Schließen", id=f'close{self._counter}', className="ml-auto btn btn-primary"),
                                ),
                            ],
                            id = f'div{self._counter}',
                            centered=True,
                            )
                        ],
                    ),

                html.Div(style={"marginLeft": "6px"}, children=subComponent if name else []),
            ],
        )
        
    def get_layout(self):
        return self._layoutDiv

    def register_callbacks(self):
        @self.main_app.callback(
            Output(f"div{self._counter}", "is_open"),
            [Input(f"open{self._counter}", "n_clicks"), Input(f"close{self._counter}", "n_clicks")],
            [State(f"div{self._counter}", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open