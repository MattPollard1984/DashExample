# -*- coding: utf-8 -*-
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
import plotly.express as px
import numpy as np
import base64
import geopandas as gpd
from shapely.geometry import MultiPolygon
from shapely.geometry import Point


"""FUNCTIONS"""


def import_image(filename):
    """
    Parameters
    ----------
    filename : STRING
        full path including file name to the image of interest.

    Function
    -------
    encode an image to base64

    Returns
    -------
    encoded_image : BYTES
        encoded image in base64.
    """
    # set image file name to the input argument of the file name
    image_filename = filename  # replace with your own image
    # encode image
    encoded_image = base64.b64encode(open(image_filename, "rb").read())

    return encoded_image


def load_map(dataframe, zoom_level=7.5):
    """
    Parameters
    ----------
    dataframe : pandas dataframe
        dataframe of the selected scores to show, either all input data
        or filtered by the user
    zoom_level=7.5
        map zoom level set to default of 7.5

    Function
    -------
    load the main map with the locations scores

    Returns
    -------
    fig : plotly mapbox figure
        mapbox figure of the locations scores
    """
    # create a scatter mapbox using lcoations of lon/lat in the dataframe and
    # color using the total score. Zoom level is set the argument zoom level
    # the range of the scale is set based on the total score minimum and
    # maximum scores in the dataframe
    fig = px.scatter_mapbox(
        dataframe,
        lat="Latitude",
        lon="Longitude",
        color="Band",
        size="Band",
        zoom=zoom_level,
        range_color=[dataframe["Band"].min(), dataframe["Band"].max()],
        hover_data=["ToZoneID", "Distance", "Band"],
    )

    # update the figure layout by adding a 'carto-positron' background map
    # and setting the background color and adjusting the map's margings
    fig.update_layout(
        mapbox_style="carto-positron",
        showlegend=False,
        paper_bgcolor="#868B9A",
        margin=dict(t=0, l=1, b=0, r=1),
    )

    # add a color axes to the map to show the colorscale key
    fig.update_coloraxes(
        colorbar_title_text="Distance (km)",
        cmin=0,
        cmax=dataframe["Band"].max(),
        colorscale=px.colors.sequential.tempo,
        colorbar_title_font=dict(color="white", family="Tahoma", size=20),
        colorbar_tickfont=dict(color="white", family="Tahoma", size=14),
    )

    return fig


def load_choropleth_map(dataframe, geojson, zoom_level=7.5):
    """
    Parameters
    ----------
    dataframe : pandas dataframe
        dataframe of the selected scores to show, either all input data
        or filtered by the user
    zoom_level=7.5
        map zoom level set to default of 7.5

    Function
    -------
    load the main map with the locations scores

    Returns
    -------
    fig : plotly mapbox figure
        mapbox figure of the locations scores
    """
    # create a scatter mapbox using lcoations of lon/lat in the dataframe and
    # color using the total score. Zoom level is set the argument zoom level
    # the range of the scale is set based on the total score minimum and
    # maximum scores in the dataframe
    fig = px.choropleth_mapbox(
        dataframe,
        geojson=geojson,
        locations="ZoneID",
        color="Band",
        zoom=zoom_level,
        range_color=[dataframe["Band"].min(), dataframe["Band"].max()],
        hover_data=["ToZoneID", "Distance", "Band"],
    )

    # update the figure layout by adding a 'carto-positron' background map
    # and setting the background color and adjusting the map's margings
    fig.update_layout(
        mapbox_style="carto-positron",
        showlegend=False,
        paper_bgcolor="#868B9A",
        margin=dict(t=0, l=1, b=0, r=1),
    )

    # add a color axes to the map to show the colorscale key
    fig.update_coloraxes(
        colorbar_title_text="Distance (km)",
        cmin=0,
        cmax=dataframe["Band"].max(),
        colorscale=px.colors.sequential.tempo,
        colorbar_title_font=dict(color="white", family="Tahoma", size=20),
        colorbar_tickfont=dict(color="white", family="Tahoma", size=14),
    )

    return fig


def set_zoom_level(dropdown_value):
    """
    Parameters
    ----------
    dropdown_value : string
        districts dropdown value selected by the user

    Function
    -------
    update the zoom level based on the selection
    if it's all districts then the zoom level will be set to 10, else the default
    will be retained of 7.5

    Returns
    -------
    updated zoom level
    """
    return 5


def set_map(dataframe, geojson, options_list, dropdown_value, map_type):
    """
    Parameters
    ----------
    dataframe : pandas dataframe
        dataframe of the selected scores to show, either all input data
        or filtered by the user
    capacity_data : pandas dataframe
        substation capacity data
    chargePoints : pandas dataframe
        EV charge points locations in MC area
    geojson: geopandas dataframe (shapefile)
        LADs shapefile
    options_list: list
        list of user's selected options of layers to show on the map
    dropdown_value: string
        districts drop down value selected by the user

    Function
    -------
    The function will update the map according to the different options selected
    by the user, mainly around the layers the user decides to show/hide

    Returns
    -------
    fig : plotly mapbox figure
        updated mapbox figure with the selected layers
    """
    # update zoom level based on the district dropdown
    zoom_level = set_zoom_level(dropdown_value)
    # load the base map
    if map_type == "scatter":
        fig = load_map(dataframe, zoom_level)
    elif map_type == "choropleth":
        fig = load_choropleth_map(dataframe, geojson, zoom_level)

    # check options to update the map accordingly
    if options_list is not None:
        # if user decides to show the LAD boundaries
        if "Zone Boundaries" in options_list:
            # update figure by adding the LADs boundaries layer
            fig.update_layout(
                mapbox={
                    "style": "carto-positron",
                    "layers": [
                        {
                            "source": geojson["geometry"].__geo_interface__,
                            "type": "line",
                            "color": "black",
                        }
                    ],
                },
            )

    return fig
