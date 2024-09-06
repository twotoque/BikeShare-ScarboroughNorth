import plotly.graph_objects as go
import geopandas as gpd 
import pandas
import json


def torontoCensusMap (rowCompare, title):
    '''
    A function to convert a single row of census 2021 data to a map relative to Toronto's neighbourhoods. 
    ----
    Parameters:
        rowCompare - the row in file "data/CityCensusData.csv" to measure data from (int)
        title - the title of the graph (str)
    '''
    #Opens up geoData, reads and converts it to a JSON (feature), then converts it to a FeatureCollection readable by plotly
    geoData = gpd.read_file("data/Neighbourhoods.geojson")
    geoDataJSON = geoData.to_json()
    geoDataDict = json.loads(geoDataJSON)
    geoDataDict = {
        "type": "FeatureCollection",
        "features": geoDataDict['features']
    }

    rowArray = []

    #Imports Census Data
    censusData = pandas.read_csv("data/CityCensusData.csv")

    #Subtracts two for header and zero indexing
    rowCompare -= 2

    #Traverses censusData, appends the rowCompare value as an int relative to Neighbourhood array

    df_geo = pandas.DataFrame(geoData.drop(columns="geometry"))
    for _, row in df_geo.iterrows():
        neighbourhood_name = row["AREA_NAME"]
        
        if neighbourhood_name in censusData.columns:
            neighbourhood_data = censusData[neighbourhood_name] 
            rowArray.append(neighbourhood_data[rowCompare])
        else: 
            print(f"Not appended {neighbourhood_name}")

    fig = go.Figure(go.Choroplethmapbox(
        geojson=geoDataDict,
        locations=geoData["AREA_ID"],  
        z=rowArray,  
        marker_opacity=0.5,
        marker_line_width=1,
        featureidkey="properties.AREA_ID",  
        text = geoData["AREA_NAME"]
    ))

    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=10, mapbox_center={"lat": 43.702, "lon": -79.395})

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    #Appends Ward 23 outline

    
    ward23GeoData = gpd.read_file("data/Ward23.geojson")
    ward23GeoDataJSON = ward23GeoData.to_json()
    ward23GeoDataDict = json.loads(ward23GeoDataJSON)
    ward23GeoDataDict = {
        "ward23GeoData": "FeatureCollection",
        "features": ward23GeoDataDict['features']
    }

    Ward23lonArray = []
    Ward23latArray = []

    for feature in ward23GeoDataDict["features"]:
        geometry = feature["geometry"]
        for polygon in geometry["coordinates"]:
            for multiCoordinate in polygon:
                for coordinate in multiCoordinate:
                    Ward23lonArray.append(coordinate[0])
                    Ward23latArray.append(coordinate[1])

    fig.add_trace(go.Scattermapbox(
        mode="lines",
        lon=Ward23lonArray,
        lat=Ward23latArray,
        line=dict(width=5, color="red"),  
        text = "Ward 23 Scarborough North"
    ))


    fig.update_layout(
        title={"text": title, "x": 0.5, "xanchor": "center", "yanchor": "top", "font": {"size": 25}}
    )



    fig.show()
torontoCensusMap(2582, "Amount of Census 2021 respondents who listed Biking as a method of transportation")