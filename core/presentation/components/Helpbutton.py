from dash import  html

import dash_bootstrap_components as dbc
class Helper():
    @staticmethod
    def help_button(id, popover_header=None, popover_body=None, title=None):
        """Creates a button that shows some information on click.

        Args:
            id (_type_): id-prefix
            popover_header (_type_, optional): Text of the heading. Defaults to None.
            popover_body (_type_, optional): Text of the description. Defaults to None.
            title (_type_, optional): Shown when hovering. Defaults to None.

        Returns:
            list: Button and its content.
        """
        return [
            dbc.Button(
                html.I(className="fa fa-info"),
                id=id+"-popover-button",
                title=title,
                className="btn-help",
                color="secondary"
            ),

            dbc.Popover(
                children=[
                    dbc.PopoverHeader(popover_header),
                    dbc.PopoverBody(popover_body, id=id+"-data-source")
                ],
                id=id+"-popover",
                trigger="legacy",
                target=id+"-popover-button",
                placement="auto"
            )
        ]
