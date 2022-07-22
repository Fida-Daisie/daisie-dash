from multiprocessing.sharedctypes import Value
from operator import index
import pandas as pd
import base64
import io


def create_download_link(dff: pd.DataFrame | list[pd.DataFrame], type: str="xslx", sheet_name: str | list[str]="Business-Report", index_label:str | None=None) -> str:
    if type == "xslx":
        with io.BytesIO() as xlsx_io:
            writer = pd.ExcelWriter(xlsx_io, engine="xlsxwriter")

            if isinstance(dff, pd.DataFrame):
                if index_label is None:
                    index_label = dff.index.name
                dff.to_excel(writer, sheet_name=sheet_name, index_label=index_label)
            elif isinstance(dff, list):
                assert len(dff) == len(sheet_name)
                if index_label is None:
                    index_label = [df.index.name for df in dff]
                for (i, df), index in zip(enumerate(dff), index_label):
                    df.to_excel(writer, sheet_name=f'{sheet_name[i]}', index_label=index)
            else:
                raise ValueError('Only pandas DataFrame and list of pandas DataFrame are allowed.')

            writer.save()
            xlsx_io.seek(0)
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            data = base64.b64encode(xlsx_io.read()).decode("utf-8")
            href_data_downloadable = f"data:{media_type};base64,{data}"
        return href_data_downloadable
    else:
        raise ValueError("Error in 'create_download_link'. Unknown type: "+ str(type))