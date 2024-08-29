from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas

def bikingInfrastructBar(filePath, title):  
    i = 0 
    n = 0
    rowArray = []
    selectArray = []
    traceList = []

    #Load csv data
    fileData = pandas.read_csv(filePath)

    fileDataFrame = pandas.DataFrame(fileData)
    ratings = list(fileDataFrame.columns[1:]) 
    neighbourhoods = fileDataFrame["Neighbourhood"]  

    for rating in ratings:
        trace = go.Bar(
            x=neighbourhoods, 
            y=fileDataFrame[rating],  
            name=rating,  
            text=fileDataFrame[rating], 
            textposition="auto"  
        )
        traceList.append(trace)

    fig_bar = go.Figure(data=traceList)
    fig_bar.update_layout(barmode="stack", xaxis_title="Neighbourhood", yaxis_title="Count", title= title)
    fig_bar.show()

bikingInfrastructBar("./data/BikingInfrastructure-Sidewalks.csv", "Sidewalk safety ratings")



