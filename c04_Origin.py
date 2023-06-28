"""
@author: Matthew (MC)

@Updates:
    
    21042022 - Mahmoud Ishtaiwi
        
"""

# High-level python libraries
import os

# Third party libraries
import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
import geopandas as gpd

# Internal Scripts
import c00_AppsFunctions as pFunc
from c01_app import app


pd.options.mode.chained_assignment = None

# get working directory'''
mainPath = os.getcwd() + "\\"

"""READ INPUT DATA"""
# import and encode mage
image_filename = mainPath + "iData\\14_Images\\Menu Icon.png"
encoded_image = base64.b64encode(open(image_filename, "rb").read())

# Default scores data
df = pd.read_csv(mainPath + "iData\\12_Data\\Distance_To_Zones.csv")
# districts bounderies
geodf = mainPath + "iData\\11_SHPs\\PLDZones_GOR.shp"
geodf = gpd.read_file(geodf)
# change projections of the shapefile
geodf = geodf.to_crs("WGS84")


# get unique list of District names
la_district_list = df["ZoneID"].unique()
# default zoom level for districts
default_zoom_list = [{name: 3} for name in la_district_list]

# set options list for dropdown
district_options = [
    {"label": "Zone " + str(value), "value": value} for value in df["ZoneID"].unique()
]
# scenario options
scenario_options = [
    {"label": "Banded Distances", "value": "Banded Distances"},
    {"label": "Full Zonal Distances", "value": "Full Zonal Distances"},
]
# Set Layer options
map_layer_options = [
    {"label": " - Zone Boundaries", "value": "Zone Boundaries"},
    {"label": " - HS2 Network", "value": "HS2 Network"},
]

# main application and layout
layout = html.Div(
    className="row",
    children=[
        html.Div(
            children=[
                html.Div(
                    id="menu-control",
                    children=[
                        html.H3("Layer Controls", className="layer-title"),
                        dcc.Checklist(
                            id="layer-control",
                            options=map_layer_options,
                            value=["Zone Boundaries"],  # LAD layer is active by default
                            className="layer-checklist",
                        ),
                        html.H3("Filters", className="layer-title"),
                        dcc.Dropdown(
                            id="local-authority-dropdown",
                            options=district_options,
                            value="5",  # Districs dropdown
                            className="dropdown",
                        ),
                        dcc.Dropdown(
                            id="scenario-dropdown",
                            options=scenario_options,
                            value=scenario_options[0]["label"],  # Scenario dropdown
                            className="dropdown",
                        ),
                        html.H3("Map Controls", className="layer-title"),
                        html.Button(
                            id="submit-button",
                            n_clicks=0,  # Sumbit Button
                            children=["Update Map"],
                            className="button",
                        ),
                        html.Button(
                            id="reset-button",
                            n_clicks=0,  # map reset Button
                            children=["Reset Map"],
                            className="button",
                        ),
                        html.Button(
                            "Download CSV", id="btn_csv", className="button"
                        ),  # download csv Button
                        dcc.Download(id="export_csv"),
                    ],
                    className="menu-grid",
                )
            ],
            className="menu-container",
        ),
        dcc.Graph(id="origin-map", className="map-style"),
    ],
)


# Output and State lists for app
state_list = [State("local-authority-dropdown", "value")]
state_list.extend(
    [
        State("scenario-dropdown", "value"),
        State("layer-control", "value"),
    ]
)


### Callback functions
# First callback: update the map based on users' selection/filters
@app.callback(
    [
        Output("origin-map", "figure"),
        Output("local-authority-dropdown", "value"),
        Output("scenario-dropdown", "value"),
    ],
    [Input("submit-button", "n_clicks"), Input("reset-button", "n_clicks")],
    state_list,
)

# map update based on users' interaction
def origin_map_update(
    submit_button,
    reset_button,
    dropdown_value,
    scenario_value,
    layer_value,
):
    button_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    # submit - update map
    if button_id == "submit-button" and submit_button:
        # filter data o only show district records
        df_new = df.loc[df["ZoneID"] == dropdown_value]
        # create figure/,ap
        if scenario_value == "Banded Distances":
            col = "Band"
        else:
            col = "Distance"

        fig = pFunc.set_map(df_new, geodf, layer_value, dropdown_value, col)

    # if nothing is triggered, i.e. initial call back!
    else:
        # keep dataframe as it is
        df_new = df.loc[df["ZoneID"] == 5]
        # create figure/,ap
        fig = pFunc.set_map(df_new, geodf, layer_value, dropdown_value, "Band")

    # return map and the various components values
    return (
        fig,
        dropdown_value,
        scenario_value,
    )
