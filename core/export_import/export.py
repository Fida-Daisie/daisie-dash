import os
import io
import base64
import markdown
import magic
import uuid
import pandas as pd


from openpyxl.drawing.image import Image



class Downloader():
    
### csv Downloader



### pdf Downloaderp


    # method to write mimetype href for download link
    @staticmethod
    def _create_downloader_href(io_file, mimetype=None):
        if mimetype is None:
            io_file.seek(0)
            mime = magic.Magic(mime=True)
            mimetype = mime.from_buffer(io_file.read())
        
        if mimetype == 'Microsoft OOXML':
            mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        io_file.seek(0)
            
        data = base64.b64encode(io_file.read()).decode('utf-8')

        file_string = f"data:{mimetype};base64,{data}"
        return file_string


    
        

    
