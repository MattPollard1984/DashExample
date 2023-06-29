"""
@author: Matthew (MC)

@Updates:
    
    21042022 - Mahmoud Ishtaiwi
        
"""

# High-level python libraries
import os

# Third party libraries
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd


# Internal Scripts
import c00_AppsFunctions as pFunc
from c01_app import app
import c03_Home
import c04_Origin

# import c05_Zones

pd.options.mode.chained_assignment = None

# get working directory
mainPath = os.getcwd() + "\\"

# read and encode logo image
logo = pFunc.import_image(mainPath + "iData\\14_Images\\hs2-placeholder.png")

# import the diffrent app's layout from the module scripts
app.layout = html.Div(
    [
        html.Div(
            children=[
                html.Img(
                    src=f"data:image/png;base64,{logo.decode()}", className="home-image"
                )
            ],
            className="home-image-container",
        ),
        html.Div(
            children=[
                dcc.Link(
                    "Distance Bands Centroids",
                    href="/c04_Origin",
                    className="link-container",
                )
            ],  # Origin Appliation
            className="o-href-container",
        ),
        # html.Div(
        #    children=[
        #        dcc.Link(
        #            "Distance Bands (Zones)",
        #            href="/c05_Zones",
        #            className="link-container",
        #        )
        #    ],  # Origin Appliation
        #    className="o-href-container",
        # ),
        html.Div(
            children=[
                dcc.Link("Home Page", href="c03_Home", className="link-container")
            ],  # Home Page Application
            className="h-href-container",
        ),
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content", children=[]),
    ]
)


# set Callback
# navigate through loaded modules, home, origin, etc.
@app.callback(
    Output(component_id="page-content", component_property="children"),
    [Input(component_id="url", component_property="pathname")],
)
def display_page(pathname):
    if pathname == "/c04_Origin":
        return c04_Origin.layout
    # elif pathname == "/c05_Zones":
    #    return c05_Zones.layout
    else:
        return c03_Home.layout


if __name__ == "__main__":
    app.run_server(debug=False)
