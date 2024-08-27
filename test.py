import plotly.graph_objects as go
import geopandas as gpd 
import pandas
import json

geoData = gpd.read_file("data/Neighbourhoods.geojson")
geoDataJSON = geoData.to_json()
geoDataDict = json.loads(geoDataJSON)
geoDataDict = {
    "type": "FeatureCollection",
    "features": geoDataDict['features']
}


censusData = pandas.read_csv("data/CityCensusData.csv")

rowCompare = 2582
rowCompare -= 2
print(censusData.columns)


df_geo = pandas.DataFrame(geoData.drop(columns='geometry'))
print(df_geo)
for _, row in df_geo.iterrows():
    neighbourhood_name = row['AREA_NAME']
    
    if neighbourhood_name in censusData.columns:
        neighbourhood_data = censusData[neighbourhood_name]
        print(neighbourhood_data)