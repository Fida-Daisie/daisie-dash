from dash import dash, html, dcc, Input, Output, State, dash_table


import pandas as pd



import dash_bootstrap_components as dbc



import numpy as np



from .daisie_component import DaisieComponent

class TableViewer(DaisieComponent):
    
    def __init__(self, id, df, editable = False, output_memory_id=None, input_memory_id=None, data_id = None):
        self.data_id = data_id 
        self.id = self._createID(id) + 'table-viewer'
        self.df = df
        self.types = df.dtypes
        self.editable = editable
        if output_memory_id is None:
            self.output_memory_id = id=self.id + 'output_local_memory'
        else:
            self.output_memory_id = output_memory_id
        if input_memory_id is None:
            self.input_memory_id = id=self.id + 'input_local_memory'
        else:
            self.input_memory_id = input_memory_id
        super().__init__(id=self.id )
        


    def get_layout(self):
        status_save = html.Div(children=[
            dbc.Button(children="speichern", id= self.id+"-save-button", n_clicks=0, disabled= (not self.editable)),
            ],
            hidden = (not self.editable))
        content = html.Div([
            dcc.Dropdown(
                options=[{'label':entry, 'value':entry} for i, entry in enumerate(self.df.columns)],
                value=self.df.columns,
                multi=True,
                placeholder="Wählen Sie bitte die gewünschten Spalten aus.",
                id= self.id+"-subsetting-selection"
            ),
            dbc.Button(children="Tabelle aktualisieren", id= self.id+"-update-button", n_clicks=0),

            dash_table.DataTable(
                id=self.id + '-table-editing',
                columns=[{"name": i, "id": i} for i in self.df.columns],
                data=self.df.to_dict('records'),
        
                editable=self.editable
            ),
            status_save,
            html.Div(dbc.Modal(
                    children = [],
                    id=self.id+"-save-message",
                    centered=True,
                    is_open=False)),
            dcc.Store(id=self.output_memory_id),
            dcc.Store(id=self.id + 'input_local_memory')
            ])
        return content 


    def is_valid_type(self, df_col_new,  col_name, df_types, df):
        try:
            df_copy = df.copy()
            df_copy[col_name] = df_col_new
            df_copy[col_name] = df_copy[col_name].astype(df_types[col_name])
            return True
        except Exception as k:
            # print('Exception Daisie: ' + str(k))
            return False
        

    def register_callbacks(self):
        @self.main_app.callback(
            [
            Output(self.id+"-save-message", 'children'),
            Output(self.id+"-save-message", "is_open"),
            Output(self.output_memory_id, 'data')
            ],
            [
            Input(self.id+ '-save-button', 'n_clicks')
            ],
            [
            State(self.id + '-table-editing', 'data'),        
            State(self.id + '-table-editing', 'columns'),
            State(self.id+"-save-message", "is_open"),
            State(self.input_memory_id, 'data')
            ]
            )
        def save_changes(n_clicks, rows, columns, is_open, local_memory):
            print('local memory: ' + str(local_memory))
            if local_memory:
                if self.data_id:
                    dict_of_df = local_memory.get(self.data_id)
                else:
                    dict_of_df = local_memory
                df=pd.DataFrame(dict_of_df)
            else:
                df = self.df
            df_new = pd.DataFrame(rows, columns=[c['name'] for c in columns])
            no_errors = True
            wrong_entry_list = []
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]  
            if self.id+"-save-button" in changed_id:
                print(columns)
                for item in columns:
                    col_name = item.get('name')
                    print(col_name)
                    if self.is_valid_type(df_new[col_name], col_name, df.dtypes, df):    
                        df[col_name] = df_new[col_name].astype(df.dtypes[col_name])
                    else:
                        no_errors = False
                        wrong_entry_list.append(col_name)
                if no_errors:
                    pop_up_message =  [
                    dbc.ModalHeader("Ihre Eingabe wurde gespeichert."),
                    dbc.ModalBody("Bitte klicken Sie irgendwo hin")
                    ]
                else:
                    message =["Bitte tragen sie andere Werte in folgende Spalten: "]
                    message.extend(html.Div(children=[html.Br(), item]) for item in wrong_entry_list)
                    pop_up_message = [
                        dbc.ModalHeader("Ihre Eingabe wurde nicht gespeichert."),
                        dbc.ModalBody(children=[html.P(message)])
                        ]
                self.df = df
                


                return [pop_up_message, True, df.to_dict('series')]
            else:
                return [[''], False, local_memory]
        @self.main_app.callback(
            [
            Output(self.id + '-table-editing', 'data'),
            Output(self.id + '-table-editing', 'columns'), 
            ],        
            [
            Input(self.id+"-update-button", 'n_clicks')
            ],
            [
            State(self.id+'-subsetting-selection', "value"),
            State(self.input_memory_id, 'data')
            ])
        def update_table(n_clicks, subset, local_memory):
            if local_memory:
                if self.data_id:
                    dict_of_df = local_memory.get(self.data_id)
                else:
                    dict_of_df = local_memory
                df=pd.DataFrame(dict_of_df)
            else:
                df = self.df
            
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]  
            if self.id+"-update-button" in changed_id:
                
                columns=[{"name": i, "id": i} for i in subset]
                data=df[subset].to_dict('records')
                
                return [data, columns]
            else:
                return [df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]]

            
            

            