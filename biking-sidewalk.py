from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas
import plotly.io as pio
pio.kaleido.scope.mathjax = None

def transportationBar (filePath, title, xaxis_title, fileName = None):  
    ''' 
    Generates a bar graph assuming neighbourhood name is in the x rows and the category labels are in the y columns. 
    ---
    Parameters:
        filePath - path of the data, in a csv form (str)
        title - the title of the graph (str)
        xaxis_title - title of the x-axis label (str)
        fileName - the path where you want to export the file in a PDF form. If left blank, the graph will not be exported. (str)
    '''
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
    fig_bar.update_layout(barmode= "stack", xaxis_title= xaxis_title, yaxis_title="Number of respondents", title= title)
    fig_bar.show()

    if fileName is not None:
        fig_bar.write_image(fileName, format="pdf", engine="kaleido", width = "1300")


transportationBar("./data/BikingDemand-Spring.csv", "Ward 23 survey respondents regarding biking usage in Spring", "Number of times biked per week", "./pdf/SpringBikingUsage.pdf")
transportationBar("./data/BikingDemand-Fall.csv", "Ward 23 survey respondents regarding biking usage in Fall","Number of times biked per week", "./pdf/FallBikingUsage.pdf")
transportationBar("./data/BikingDemand-Winter.csv", "Ward 23 survey respondents regarding biking usage in Winter", "Number of times biked per week","./pdf/WinterBikingUsage.pdf")
transportationBar("./data/BikingDemand-Summer.csv", "Ward 23 survey respondents regarding biking usage in Summer","Number of times biked per week", "./pdf/SummerBikingUsage.pdf")



