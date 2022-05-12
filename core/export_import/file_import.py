# -*- coding: utf-8 -*-
import uuid
import base64
import os

from dash import html, Input, Output


from .. import DaisieMain

class DaisieImport():
   
    def __init__(self, id, type):
        self.id = id + uuid.uuid4() + 'import'
        self.main_app = DaisieMain.app
        self.register_callbacks()


    def save_file(name, content):
        
        
        """Decode and store a file uploaded with Plotly Dash."""
        data = content.encode("utf8").split(b";base64,")[1]
        with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
            fp.write(base64.decodebytes(data))

    def get_layout(self):
        pass
       

    
    def register_callbacks(self):
        @self.main_app.callback(
        Output("file-list", "children"),
        [Input("upload-data", "filename"), 
        Input("upload-data", "contents")],
        )
        def update_output(uploaded_filenames, uploaded_file_contents):
            """Save uploaded files and regenerate the file list."""

            if uploaded_filenames is not None and uploaded_file_contents is not None:
                for name, data in zip(uploaded_filenames, uploaded_file_contents):
                    save_file(name, data)

            files = uploaded_files()
            if len(files) == 0:
                return [html.Li("No files yet!")]
            else:
                return [html.Li(file_download_link(filename)) for filename in files]
