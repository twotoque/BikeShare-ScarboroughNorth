import plotly.graph_objects as go
import geopandas as gpd 
import pandas
import json
import plotly.io as pio
pio.kaleido.scope.mathjax = None


def censusMap (geoDataFilePath, dataSource, rowCompare, title, rowArrayBar, mapZoomSettings, fileName=None):
    '''
    A function to convert a single row of census 2021 data to a map relative to Toronto's neighbourhoods. 
    ----
    Parameters:
        geoDataFilePath - the path for the geoData (str to .geojson file path)
            "data/Neighbourhoods.geojson" for city-wide neighbourhood map
            "data/Ward23Neighbourhoods.geojson" for Ward 23  neighbourhood map
        dataSource - the path for the data (str to .json file path)
            "data/CityCensusData.csv" for city-wide Census 2021 data
            "data/Ward23CensusData.csv" for Ward 23 Census 2021 data
        rowCompare - the row in dataSource  to measure data from (int)
        title - the title of the graph (str)
        rowArrayBar - label for the variable (str)
        mapZoomSettings - specific settings for map zooming (array). Should be set up in form
            [Zoom variable (float), latitude (float), longitude (float), export height (int) [optional], export width (int) [optional]]
            ---
            Use [11, 43.710, -79.380, 2000, 1250] for City of Toronto-wide maps
            Use [12.6, 43.810, -79.245, 2000, 1250] for Ward 23 maps
        fileName - the path where you want to export the file in a PDF form. If left blank, the graph will not be exported. If this parameter is used, ensure mapZoomSettings have export heights and export widths (str)
    '''
    #Opens up geoData, reads and converts it to a JSON (feature), then converts it to a FeatureCollection readable by plotly
    geoData = gpd.read_file(geoDataFilePath)
    geoDataJSON = geoData.to_json()
    geoDataDict = json.loads(geoDataJSON)
    geoDataDict = {
        "type": "FeatureCollection",
        "features": geoDataDict['features']
    }

    rowArray = []

    #Imports Census Data
    censusData = pandas.read_csv(dataSource)

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

    #Creates a figure with its fill being the z value (in this case, rowArray), relative to all the other z values
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geoDataDict,
        locations=geoData["AREA_ID"],  
        z=rowArray,  
        marker_opacity=0.5,
        marker_line_width=1,
        featureidkey="properties.AREA_ID", 
        text = geoData["AREA_NAME"],
        hoverinfo="text+z",
        hovertemplate= f"%{{text}}<br>%{{z}} {rowArrayBar}<extra></extra>",
        colorbar=dict(
            title=rowArrayBar,
        )
    ))

    #Appends Ward 23 outline (opens up data, gets coords, and then adds a Scatter trace with each trace connected with a line)

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
        mode = "lines",
        showlegend=True,
        lon=Ward23lonArray,
        lat=Ward23latArray,
        line=dict(width=5, color="red"),  
        text = "Ward 23 Scarborough North",
        name = "Ward 23 Scarborough North"  
    ))

    #Updates appearance
    fig.update_layout(
        mapbox_style="carto-positron", 
        mapbox_zoom=mapZoomSettings[0], 
        mapbox_center={"lat": mapZoomSettings[1], "lon": mapZoomSettings[2]}, 
        margin={"r":0,"t":60,"l":0,"b":0}, 
        title={"text": title, "x": 0.5, "xanchor": "center", "yanchor": "top", "font": {"size": 25}},
        legend=dict(
            x=0.5,               
            y=0.1,               
            xanchor="center",  
            yanchor="top",
        )
    )

    fig.show()
    if fileName is not None and len(mapZoomSettings) == 5:
       fig.write_image(fileName, format="pdf", engine="kaleido", width= mapZoomSettings[3], height=mapZoomSettings[4])
    elif fileName is not None: 
        print("Error - missing or invaild mapZoomSettings. It should have 5 numbers, with the last 2 indicating the width and height of the export accordingly")
    else: 
        print("Error - missing fileName or other critical error. The last parameter in your function should be a string ending in .pdf to your exported file")

        
def pointMap (geoDataFilePath, colourList, nameList, title, mapZoomSettings, fileName=None):

    n = 0
    fig = go.Figure(go.Scattermapbox(
        mode = "markers",
        showlegend=True,
    ))

    for geoFile in geoDataFilePath: 
        geoData = gpd.read_file(geoFile)
        geoDataJSON = geoData.to_json()
        geoDataDict = json.loads(geoDataJSON)
        geoDataDict = {
            "ward23GeoData": "FeatureCollection",
            "features": geoDataDict['features']
        }

        lonArray = []
        latArray = []
        for feature in geoDataDict["features"]:
            geometry = feature["geometry"]
            lonArray.append(geometry["coordinates"][0])
            latArray.append(geometry["coordinates"][1])

        fig.add_trace(go.Scattermapbox(
            mode = "markers",
            showlegend=True,
            lon=lonArray,
            lat=latArray,
            marker=dict(size=10, color=colourList[n]), 
            name = nameList[n]
        )
        )
        n += 1
        
    fig.update_layout(
        mapbox_style="carto-positron", 
        mapbox_zoom=mapZoomSettings[0], 
        mapbox_center={"lat": mapZoomSettings[1], "lon": mapZoomSettings[2]}, 
        margin={"r":0,"t":60,"l":0,"b":0}, 
        title={"text": title, "x": 0.5, "xanchor": "center", "yanchor": "top", "font": {"size": 25}},
        legend=dict(
            x=0.5,               
            y=0.1,               
            xanchor="center",  
            yanchor="top",
        )
    )


    fig.show()
    if fileName is not None and len(mapZoomSettings) == 5:
        fig.update_layout(mapbox_zoom=mapZoomSettings[0] * 1.1)
        fig.write_image(fileName, format="pdf", engine="kaleido", width= mapZoomSettings[3], height=mapZoomSettings[4])
    elif fileName is not None: 
        print("Error - missing or invaild mapZoomSettings. It should have 5 numbers, with the last 2 indicating the width and height of the export accordingly")
    else: 
        print("Error - missing fileName or other critical error. The last parameter in your function should be a string ending in .pdf to your exported file")


'''


censusMap("data/Neighbourhoods.geojson", "data/CityCensusData.csv", 2577, "Amount of Census 2021 respondents who listed driving as a method of transportation", "Respondents", [11, 43.710, -79.380, 2000, 1250],  "./pdf/CensusDrivingDataTorontoWide.pdf")
censusMap("data/Neighbourhoods.geojson", "data/CityCensusData.csv", 2580, "Amount of Census 2021 respondents who listed public transportation as a method of transportation", "Respondents", [11, 43.710, -79.380, 2000, 1250],  "./pdf/CensusPublicTransportDataTorontoWide.pdf")
censusMap("data/Neighbourhoods.geojson", "data/CityCensusData.csv", 2581, "Amount of Census 2021 respondents who listed walking as a method of transportation", "Respondents", [11, 43.710, -79.380, 2000, 1250],  "./pdf/CensusWalkingDataTorontoWide.pdf")
censusMap("data/Neighbourhoods.geojson", "data/CityCensusData.csv", 2582, "Amount of Census 2021 respondents who listed biking as a method of transportation", "Respondents", [11, 43.710, -79.380, 2000, 1250],  "./pdf/CensusBikingDataTorontoWide.pdf")
censusMap("data/Ward23Neighbourhoods.geojson", "data/Ward23CensusData.csv", 2577, "Amount of Census 2021 respondents who listed driving as a method of transportation", "Respondents", [12.6, 43.810, -79.245, 2000, 1250],  "./pdf/CensusDrivingDataWard23.pdf")
censusMap("data/Ward23Neighbourhoods.geojson", "data/Ward23CensusData.csv", 2580, "Amount of Census 2021 respondents who listed public transportation as a method of transportation", "Respondents", [12.6, 43.810, -79.245, 2000, 1250],  "./pdf/CensusPublicTransportDataWard23.pdf")
censusMap("data/Ward23Neighbourhoods.geojson", "data/Ward23CensusData.csv", 2581, "Amount of Census 2021 respondents who listed walking as a method of transportation", "Respondents", [12.6, 43.810, -79.245, 2000, 1250],  "./pdf/CensusWalkingDataWard23.pdf")
censusMap("data/Ward23Neighbourhoods.geojson", "data/Ward23CensusData.csv", 2582, "Amount of Census 2021 respondents who listed biking as a method of transportation", "Respondents", [12.6, 43.810, -79.245, 2000, 1250],  "./pdf/CensusBikingDataWard23.pdf")
pointMap(["data/DrivingDestinations-AgincourtNorth.geojson", "data/DrivingDestinations-MalvernEast.geojson", "data/DrivingDestinations-MalvernWest.geojson", "data/DrivingDestinations-Milliken.geojson", "data/DrivingDestinations-Morningside.geojson"], ["red", "blue", "purple", "green", "black"],  ["Agincourt North", "Malvern East", "Malvern West", "Milliken", "Morningside Heights"] ,"Ward 23 survey respondents regarding driving destinations", [9.5, 43.650, -79.400, 2000, 1250],  "./pdf/Ward23DrivingDestinations.pdf")
pointMap(["data/PublicTransportDestinations-AgincourtNorth.geojson", "data/PublicTransportDestinations-MalvernEast.geojson", "data/PublicTransportDestinations-MalvernWest.geojson", "data/PublicTransportDestinations-Milliken.geojson", "data/PublicTransportDestinations-Morningside.geojson"], ["red", "blue", "purple", "green", "black"],  ["Agincourt North", "Malvern East", "Malvern West", "Milliken", "Morningside Heights"] ,"Ward 23 survey respondents regarding public transit destinations", [11, 43.650, -79.400, 2000, 1250],  "./pdf/Ward23PublicTransportDestinations.pdf")
pointMap(["data/BikingDestinations-AgincourtNorth.geojson", "data/BikingDestinations-MalvernEast.geojson", "data/BikingDestinations-MalvernWest.geojson", "data/BikingDestinations-Milliken.geojson", "data/BikingDestinations-Morningside.geojson"], ["red", "blue", "purple", "green", "black"],  ["Agincourt North", "Malvern East", "Malvern West", "Milliken", "Morningside Heights"] ,"Ward 23 survey respondents regarding biking destinations", [11, 43.700, -79.300, 2000, 1250],  "./pdf/Ward23BikingDestinations.pdf")
'''

pointMap(["data/BikeShare-AgincourtNorth.geojson", "data/BikeShare-AgincourtSouthMalvernWest.geojson", "data/BikeShare-MalvernEast.geojson", "data/BikeShare-MalvernWest.geojson", "data/BikeShare-Milliken.geojson", "data/BikeShare-Morningside.geojson"], ["red", "gray", "blue", "purple", "green", "black"],  ["Agincourt North", "Agincourt South-Malvern West","Malvern East", "Malvern West", "Milliken", "Morningside Heights"] ,"Ward 23 survey respondents regarding future Bike Share Toronto stations", [11, 43.650, -79.400, 2000, 1250],  "./pdf/Ward23BikeShare.pdf")