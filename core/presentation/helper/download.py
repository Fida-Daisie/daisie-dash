import pandas as pd
import base64
import io
import xlsxwriter


def create_download_link(dff, type="xslx", sheet_name="Business-Report"):
    if type == "xslx":
        xlsx_io = io.BytesIO()
        writer = pd.ExcelWriter(xlsx_io, engine="xlsxwriter")
        dff.to_excel(writer, sheet_name=sheet_name)
        writer.save()
        xlsx_io.seek(0)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        data = base64.b64encode(xlsx_io.read()).decode("utf-8")
        href_data_downloadable = f"data:{media_type};base64,{data}"
        return href_data_downloadable
    else:
        print("Error in 'create_download_link'. Unknown type: "+ str(type))
        return None