

import uuid
import pandas as pd


from dash import dash, html, dcc, Input, Output, State, ALL
import dash_bootstrap_components as dbc

from .daisie_component import DaisieComponent

class DataFrameEntryForm(DaisieComponent):
    
    def __init__(self, id, df, name_column = None, index_column = None, unique_list = [], displayed_input = [], inputfield=[], output_memory_id=None, input_memory_id=None, data_id = None, db_engine=None):
        
        self.unique_list = unique_list
        self.data_id = data_id 
        self.id = id + '-table-entry-form'
        self.db_engine = db_engine
        if output_memory_id is None:
            self.output_memory_id = id=self.id + 'output_local_memory'
        else:
            self.output_memory_id = output_memory_id
        if input_memory_id is None:
            self.input_memory_id = id=self.id + 'input_local_memory'
        else:
            self.input_memory_id = input_memory_id
        if displayed_input == []:
            self.displayed_input = df.columns.to_list()
        else:
            self.displayed_input = displayed_input
        
        self.df = df
        # TODO Datentypen mitgeben (zB als dcc.Store in der übergeordneten App)
        self.types = df[displayed_input].dtypes
        self.inputfield = inputfield
        if name_column:
            self.name_column = name_column
        else:
            self.name_column = self.df.columns.to_list()[0]
        if index_column:
            self.index_column = index_column
        else:
            self.index_column = self.df.columns.to_list()[0]
        self.index = self.df.at[0, self.index_column]
        self.attributes = self.get_attributes()
        super().__init__(id=self.id)
        
        


    def get_attributes(self):
        return self

    def get_layout(self):
        dropdown = html.Div([
        dcc.Dropdown(
            id=self.id+'-line-selection',
            options=[{'label': items[0], 'value':items[1]} for items in self.df[[self.name_column, self.index_column]].values.tolist()], 
            value=self.df.at[0,self.index_column]
            ),
            ])

        newline= dbc.Button(children="neue Zeile anlegen", id=self.id+'-add-newline', n_clicks=0)
        delete_line= dcc.ConfirmDialogProvider(
            children=html.Button(children="diese Zeile löschen", className="btn"),
            id=self.id+'-delete-line',
            message= "Möchten sie die ausgewählte Zeile löschen?"
        )
        
        
        
        status_save = html.Div(children=[
            dbc.Button(children="speichern", id= self.id+"-save-button"),
            ])

        modal = html.Div(dbc.Modal(
                [
                dbc.ModalHeader("Ihre Eingabe wurde gespeichert"),
                dbc.ModalBody("Bitte klicken Sie irgendwo hin")
                ],
                id=self.id+"-save-message",
                centered=True,
                is_open=False))
        return html.Div(children=[modal, html.Label(children=[self.name_column]), html.Div(children=[html.Div(children = [dropdown, newline, delete_line])], style={'columnCount': 3}),
                html.Div(id=self.id+"text-entry-area"), html.Br(), status_save,  html.Br(), html.Br(), html.Br(), html.Br(),html.Br(),dcc.Store(id=self.output_memory_id),
            dcc.Store(id=self.id + 'input_local_memory')])
    
    def is_input(self, col):
        if self.inputfield == []:
            return True
        if self.types[col]=='object':
            return False
        else: return True
        

    def create_text_area(self, index=None, df=None): 
        
        if not index:
            index == self.index
        content=[]
        subset_df = df[self.df[self.index_column] == index].reset_index(drop=True)
        
        for col_name in self.displayed_input:
            
            if not self.is_input(col_name):
                content.append(
                    html.Div([
                    html.Label(col_name), html.Div(id={'type': self.id + 'type-warning', 'index': col_name}),
                    dcc.Textarea(
                        id={'type': self.id + 'text-area', 'index': col_name},
                        
                        value=str(subset_df.loc[0, col_name]),
                        style={'width': '100%', 'height': 100}
                    ),        
                ])
                )
            else:
                content.append(
                    html.Div([
                    html.Label(col_name), html.Div(id={'type': self.id + 'type-warning', 'index': col_name}),
                    dcc.Input(
                        id={'type': self.id + 'text-area', 'index': col_name},
                        value=str(subset_df.loc[0, col_name]),
                        style={'width': '100%'}
                    ),        
                ])
                )
        return html.Div(content)

    def check_type(self, index, i, item, df):
        try:
            df_copy = df[self.displayed_input].copy().astype({col : self.types[i] for i, col in enumerate(self.displayed_input)})
            
            df_copy.iloc[index, i] = item
            df_copy[df_copy.columns.to_list()[i]] = df_copy[self.displayed_input[i]].astype(self.types[i])
            return True
        except Exception as k:
            print('Exception Daisie: ' + str(k))
            return False
    
    def save_to_db(self, index, values, df):
        return index, df
    
    def delete_from_db(self, index):
        pass
        

    def get_default_value(self, i):
        dtype = self.types[i]
        default_values = {
            'object':   "Bitte geben sie Ihrern gewünschten text ein.",
            'int64': 99,
            'float64': 99.9,
            'bool': False,
            'np.datetime64': '2021-01-01',
            'timedelta[ns]': 0,
            'catergory': None
        }
        return default_values.get(str(dtype))

    def check_unique(self, item=None, index = None, column_index = None, df=None, no_errors = True):
        values_list = df[self.displayed_input[column_index]].values.tolist()
        values_list.pop(index)
        values_list = [str(x) for x in values_list]
        if item in values_list:
            return False , self.displayed_input[column_index]
        else:
            return no_errors, None


    def register_callbacks(self):
        @self.main_app.callback(
            [
            Output(self.output_memory_id, 'data'),
            Output(self.id+'-line-selection', "options"),
            Output(self.id+'-line-selection', "value"),
            Output(self.id+"-save-message", "is_open"),
            Output(self.id+"-save-message", 'children')
            ],
            [
            Input(self.id+'-add-newline', 'n_clicks'), 
            Input(self.id+"-delete-line", 'submit_n_clicks'),
            Input(self.id+"-save-button", 'n_clicks')
            ],
            [
            State({'type': self.id + 'text-area', 'index': ALL}, 'value'),
            State(self.id+'-line-selection', "value"),
            State(self.id+"-save-message", "is_open"),
            State(self.input_memory_id, 'data')
            ])
        def save_and_add_new_line(new_line_click, delete_click, save_click, values, index, is_open, local_memory):
            if local_memory:
                if self.data_id:
                    dict_of_df = local_memory.get(self.data_id)
                else:
                    dict_of_df = local_memory
                df=pd.DataFrame(dict_of_df)
            else:
                df = self.df
            
            if df.shape[0] >= 1:
                self.types = df[self.displayed_input].dtypes
            else:
                df = df.astype({col : self.types[i] for i, col in enumerate(self.displayed_input)})
            
            i_index = df[df['id']== index].index[0]
            
            self.index = self.df.at[0, self.index_column]
            # when the save-button is clicked
            saved_successfully = [
                dbc.ModalHeader("Ihre Eingabe wurde gespeichert."),
                dbc.ModalBody("Bitte klicken Sie irgendwo hin")
                ]
            wrong_entry_list=[]
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]  
            if self.id+"-save-button" in changed_id:
                # the dataframe gets updated
                # and a pop-up/modal opens
                is_open = True
                no_errors = True
               
                
                for i, item in enumerate(values):
    
                    if self.displayed_input[i] in self.unique_list:    
                        no_errors, wrong_entry = self.check_unique( item=item, index = i_index, column_index = i, df=df, no_errors=no_errors)
                        wrong_entry_list.append(wrong_entry)
                    if self.check_type(i_index, i, item, df):
                        df.at[i_index, self.displayed_input[i]] = item
                        df[self.displayed_input[i]] = df[self.displayed_input[i]].astype(self.types[i])
                    else:
                        no_errors = False
                        wrong_entry_list.append(self.displayed_input[i])
                wrong_entry_list = list(set(wrong_entry_list))
                if no_errors:
                    pop_up = saved_successfully
                    index, df = self.save_to_db(index, values, df)
                else:
                    message =["Bitte tragen sie andere Werte in folgende Felder: "]
                    message.extend(html.Div(children=[html.Br(), item]) for item in wrong_entry_list)
                    pop_up = [
                        dbc.ModalHeader("Ihre Eingabe wurde nicht gespeichert."),
                        dbc.ModalBody(children=[html.P(message)]) 
                        ]
                self.df = df
                return [df.to_dict('series'), [{'label': items[0], 'value':items[1]} for items in self.df[[self.name_column, self.index_column]].values.tolist()], index, is_open, pop_up]
            # when the new-line-button is clicked
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            if self.id+'-add-newline' in changed_id:
                # a new row gets added to the bottom of the dataframe
                
                if df.shape[0] > 0:
                    j = df.iloc[-1].name + 1
                else:
                    j = 0
                new_line = {'id':int(str(uuid.uuid1().int)[:16])}
                for i, col in enumerate(self.displayed_input):
                    new_line.update({col:  self.get_default_value(i)})
                    
                df = df.append(pd.Series(new_line), ignore_index=True)
                # df = df.astype({col : self.types[i] for i, col in enumerate(df.columns)})
                # the value of the dropdown is also changed, which will trigger the other callback
                self.df = df
                return [df.to_dict('series'),
                        [{'label': items[0], 'value':items[1]} for items in self.df[[self.name_column, self.index_column]].values.tolist()], 
                        new_line.get('id'),
                        is_open,
                        saved_successfully
                    ]
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]  
            if self.id+"-delete-line" in changed_id:
                df = df.drop(index=i_index)
                print('start')
                self.delete_from_db(index)
                df = df.reset_index(drop=True)
                
                index=df.loc[0,'id']
            self.df = df
            return [df.to_dict('series'), [{'label': items[0], 'value':items[1]} for items in self.df[[self.name_column, self.index_column]].values.tolist()], index, is_open, saved_successfully]
        
        @self.main_app.callback(
            Output(self.id+"text-entry-area", "children"),
            [Input(self.id+'-line-selection', "value"), 
            Input(self.input_memory_id, 'data')   
            ]
            )
        def call_text_area(index, local_memory):
            if local_memory:
                if self.data_id:
                    dict_of_df = local_memory.get(self.data_id)
                else:
                    dict_of_df = local_memory
                df=pd.DataFrame(dict_of_df)
            else:
                df = self.df
            if df.shape[0] == 0:
                return [html.Div("Keine Einträge")]
            # the text-area gets updated, when another value is selected in the dropdown 
            else:
                return [self.create_text_area(index, df)]

       