import io, base64
from dash import html



def createImageFromFigure(fig, **kwargs):
    pic_IObytes = io.BytesIO()
    fig.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    pic_hash = base64.b64encode(pic_IObytes.read()).decode('ascii')
    return html.Img(src='data:image/png;base64,{}'.format(pic_hash), **kwargs)