import plotly.graph_objects as go
import geopandas as gpd 
import pandas
import json

#Opens up geoData, reads and converts it to a JSON (feature), then converts it to a FeatureCollection readable by plotly
geoData = gpd.read_file("data/Neighbourhoods.geojson")
geoDataJSON = geoData.to_json()
geoDataDict = json.loads(geoDataJSON)
geoDataDict = {
    "type": "FeatureCollection",
    "features": geoDataDict['features']
}

#Imports Census Data
censusData = pandas.read_csv("data/CityCensusData.csv")

#Row to compare
rowCompare = 2582

#Subtracts two for header and zero indexing
rowCompare -= 2

#Traverses censusData, appends the rowCompare value as an int relative to Neighbourhood array
rowArray = []
rowArray.append(censusData.iloc[rowCompare])
carValues = list(map(int, rowArray[0].iloc[1:].values))
print(rowArray)


fig = go.Figure(go.Choroplethmapbox(
    geojson=geoDataDict,
    locations=geoData["AREA_ID"],  
    z=carValues,  
    marker_opacity=0.5,
    marker_line_width=1,
    featureidkey="properties.AREA_ID",  
    text = geoData["AREA_NAME"]
))

fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=10, mapbox_center={"lat": 43.702, "lon": -79.395})

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


fig.update_layout(
    title={"text":  "Amount of Census 2021 respondents who listed Biking as a method of transportation", "x": 0.5, "xanchor": "center", "yanchor": "top", "font": {"size": 25}}
)


fig.show()