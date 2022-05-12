'''
needs to be reworked and put into the module componeten because it is not based on pythonic sqlalchemy
from datetime import datetime as dt

from dash import html, dcc, Output, Input


from . import DBConnection
from ..presentation.components import DaisieComponent

class DatabaseComponent(DaisieComponent):
    def __init__(self, id, sql_list=[], refresh_time=14400): 
        """Constructor for the DatabaseComponent. 
        We need a unique id, a list of sql commands as strings and a refresh time in seconds (default: 4 hours).
        Example for sql_list:  ["SELECT * FROM dwh.v_mart_stunden", "SELECT * FROM dwh.v_mart_rechnungen"]
        """
        self.__sql_list = sql_list
        self.__refresh_time = refresh_time
        self._df_list = []
        self.__last_data_refresh = dt.now()
    
        self.refresh_data()
        
        super().__init__(id)

    def get_data(self) -> list:
        """Method to extract the df_list from the component."""
        return self._df_list

    def refresh_data(self):
        """Method to refresh the data via opening the DB connection and overwriting the old data."""
        # open db connection
        with DBConnection() as db_connection:
            # read all dataframes from the sql list and put them into a df list
            df_list = []

            for sql in self.__sql_list:
                df = db_connection.getDataFrameFromSQL(sql)
                df_list.append(df)

            # overwrite old data
            self._df_list = df_list
            
            # once all things are done, set the new refresh-date
            self.__last_data_refresh = dt.now()


    # component stuff, i.e. layout and callbacks
    def get_layout(self):
        """Method to return the component's layout, i.e. an interval timer and a Display for the last refresh time."""
        return html.Div(children=[
            dcc.Interval(id=self.id+"interval", interval=60*1000), # Generate interval every 60 seconds
            html.P(id=self.id+"last-data-update", # Output for the last refresh time
                className='small d-flex flex-wrap flex-grow-1 last-data-update', 
                children=["Datenbasis zuletzt aktualisiert: " + self.__last_data_refresh.strftime("%d.%m.%Y, %H:%M:%S")]
            )
        ])

    def register_callbacks(self):
        @self.main_app.callback(
            Output(self.id+"last-data-update", "children"),
            [Input(self.id+"interval", "n_intervals")],
        )
        def user_action_refresh_data_basis(n_intervals):
            if (dt.now() - self.__last_data_refresh).seconds > self.__refresh_time:
                # Last update greater than 4 hours
                print("DataBasis update! Last update: ", self.__last_data_refresh)
                self.refresh_data()
                print("DataBasis update! Done: ", self.__last_data_refresh)
            return "Datenbasis zuletzt aktualisiert: " + self.__last_data_refresh.strftime("%d.%m.%Y, %H:%M:%S")
'''