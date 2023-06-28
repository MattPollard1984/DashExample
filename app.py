"""
@author: Matthew (MC)

@Updates:
    
    21042022 - Mahmoud Ishtaiwi
        
"""

import dash
from dash import html
import base64
from c01_app import app
import os
import c00_AppsFunctions as pFunc

# get working directory
mainPath = os.getcwd() + "\\"

# import and encode images
mc_logo_image = pFunc.import_image(mainPath + "iData\\14_Images\\Engine_for_growth.png")
ev_image = pFunc.import_image("iData\\14_Images\\HS2_train.jpeg")

# set layout
layout = html.Div(
    children=[
        html.Img(
            src=f"data:image/png;base64,{mc_logo_image.decode()}", className="center"
        ),
        html.Img(
            src=f"data:image/png;base64,{ev_image.decode()}", className="ev-image"
        ),
    ],
    className="background",
)
