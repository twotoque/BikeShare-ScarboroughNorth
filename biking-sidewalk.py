from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas
import plotly.io as pio
pio.kaleido.scope.mathjax = None
from utils import export_html

def transportationBar (filePath, title, xaxis_title, fileName = None, htmlName = None):  
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

    if htmlName:
        export_html(fig_bar, htmlName) 

def transportationSunburstPie (filePath, title,fileName = None, htmlName = None):  
    ''' 
    Generates a sunburst pie graph assuming neighbourhood name is in the x rows and the category labels are in the y columns. 
    ---
    Parameters:
        filePath - path of the data, in a csv form (str). Should have an
            ID = The name of the outer circle (i.e. the parent and label in one line)
            Answer = Parent of the subcategories (neighbourhood)
            Neighbourhood - Neighbourhoods 
            Value = Specific value
        title - the title of the graph (str)
        xaxis_title - title of the x-axis label (str)
        fileName - the path where you want to export the file in a PDF form. If left blank, the graph will not be exported. (str)
    '''

    #Load csv data
    fileData = pandas.read_csv(filePath)

    colours = {
        "Yes": "green",
        "No": "red"
    }
    fileData["colours"] = fileData["neighbourhood"].map(colours)

    fig_sun =go.Figure(go.Sunburst(
        ids=fileData["id"],
        labels=fileData["neighbourhood"],
        parents=fileData["answer"],
        values=fileData["values"],
        branchvalues="total",
        marker=dict(colors=fileData["colours"]),
        text= fileData["values"],
        textinfo="label+text",     
    ))
    fig_sun.update_layout (margin = dict(t=0, l=0, r=0,  b=0), title= title)
    fig_sun.show()
    if fileName is not None:
       fig_sun.write_image(fileName, format="pdf", engine="kaleido")


    if htmlName:
        export_html(fig_sun, htmlName) 



transportationBar("./data/BikingInfrastructure-MajWithBL.csv", "Ward 23 survey regarding biking on major roads with bike lanes","Rating (1 is highest)", "./pdf/BikingInfrastructure-MajWithBL.pdf", "infra_major_bikelane")
transportationBar("./data/BikingInfrastructure-MajWOBL.csv", "Ward 23 survey regarding biking on major roads without bike lanes","Rating (1 is highest)", "./pdf/BikingInfrastructure-MajWOBL.pdf", "infra_major_wobl")
transportationBar("./data/BikingInfrastructure-Parks.csv", "Ward 23 survey regarding biking on parks","Rating (1 is highest)", "./pdf/BikingInfrastructure-Parks.pdf", "infra_parks")
transportationBar("./data/BikingInfrastructure-Residental.csv", "Ward 23 survey regarding biking on residental areas","Rating (1 is highest)", "./pdf/BikingInfrastructure-Residental.pdf", "infra_residental")
transportationBar("./data/BikingInfrastructure-Sidewalks.csv", "Ward 23 survey regarding biking on sidewalks","Rating (1 is highest)", "./pdf/BikingInfrastructure-Sidewalks.pdf", "infra_sidewalks")
'''



transportationBar("./data/BikingDemand-Spring.csv", "Ward 23 survey respondents regarding biking usage in Spring", "Number of times biked per week", "./pdf/SpringBikingUsage.pdf")
transportationBar("./data/BikingDemand-Fall.csv", "Ward 23 survey respondents regarding biking usage in Fall","Number of times biked per week", "./pdf/FallBikingUsage.pdf")
transportationBar("./data/BikingDemand-Winter.csv", "Ward 23 survey respondents regarding biking usage in Winter", "Number of times biked per week","./pdf/WinterBikingUsage.pdf") 
transportationBar("./data/BikingDemand-Summer.csv", "Ward 23 survey respondents regarding biking usage in Summer","Number of times biked per week", "./pdf/SummerBikingUsage.pdf")
transportationBar("./data/BikingUseCases.csv", "Ward 23 survey respondents regarding general biking desintations","General biking destinations", "./pdf/BikingUseCases.pdf")
transportationBar("./data/BikingJustification.csv", "Ward 23 survey respondents regarding reasons to bike as opposed to other transportation methods","Reasons given", "./pdf/BikingJustification.pdf")
transportationBar("./data/PublicTransportationDestinations (r_=3).csv", "Ward 23 survey respondents regarding public transportation destinations (r>=3)","Destinations", "./pdf/PublicTransportationDestinations.pdf")
transportationBar("./data/PublicTransportationUseCases.csv", "Ward 23 survey respondents regarding general public transportation destinations","Reasons given", "./pdf/PublicTransportationUseCases.pdf")
transportationBar("./data/PublicTransportationInsteadBike.csv", "Ward 23 survey respondents justifying public transportation instead of biking","Reasons given", "./pdf/PublicTransportationInsteadBike.pdf")
transportationBar("./data/PublicTransportationBike.csv", "Ward 23 survey respondents regarding bringing bikes within public transportation methods","Responces", "./pdf/PublicTransportationBike.pdf")
transportationSunburstPie("./data/BikeShareAwarenessSunburst.csv", "Ward 23 survey respondents regarding prior knowledge of the Bike Share Toronto program", "./pdf/BikeShareAwareness.pdf")

transportationSunburstPie("./data/PublicTransportationBikeSunburst.csv", "Ward 23 survey respondents regarding bringing bikes within public transportation methods", "./pdf/PublicTransportationBikeSunburstPie.pdf")
transportationBar("./data/BikingInfrastructure-HydroCorridors.csv", "Ward 23 survey respondents rating biking infrastructure, hydro corridors","Rating (1 is highest)", "./pdf/BikingInfrastructure-HydroCorridors.pdf")
transportationBar("./data/DrivingInsteadBike.csv", "Ward 23 survey respondents justifying driving instead of biking","Rating (1 is highest)", "./pdf/DrivingInsteadBike.pdf")


'''

'''
# Biking Demand and Use Cases
'''
transportationBar("./data/BikingDemand-Spring.csv", "Ward 23 survey respondents regarding biking usage in Spring", "Number of times biked per week", "./pdf/SpringBikingUsage.pdf", "biking_usage_spring")
transportationBar("./data/BikingDemand-Fall.csv", "Ward 23 survey respondents regarding biking usage in Fall","Number of times biked per week", "./pdf/FallBikingUsage.pdf", "biking_usage_fall")
transportationBar("./data/BikingDemand-Winter.csv", "Ward 23 survey respondents regarding biking usage in Winter", "Number of times biked per week","./pdf/WinterBikingUsage.pdf", "biking_usage_winter") 
transportationBar("./data/BikingDemand-Summer.csv", "Ward 23 survey respondents regarding biking usage in Summer","Number of times biked per week", "./pdf/SummerBikingUsage.pdf", "biking_usage_summer")
transportationBar("./data/BikingUseCases.csv", "Ward 23 survey respondents regarding general biking destinations","General biking destinations", "./pdf/BikingUseCases.pdf", "biking_destinations")
transportationBar("./data/BikingJustification.csv", "Ward 23 survey respondents regarding reasons to bike as opposed to other transportation methods","Reasons given", "./pdf/BikingJustification.pdf", "biking_justification")

'''
# Public Transportation
'''
transportationBar("./data/PublicTransportationDestinations (r_=3).csv", "Ward 23 survey respondents regarding public transportation destinations (r>=3)","Destinations", "./pdf/PublicTransportationDestinations.pdf", "pt_destinations_filtered")
transportationBar("./data/PublicTransportationUseCases.csv", "Ward 23 survey respondents regarding general public transportation destinations","Reasons given", "./pdf/PublicTransportationUseCases.pdf", "pt_destinations_general")
transportationBar("./data/PublicTransportationInsteadBike.csv", "Ward 23 survey respondents justifying public transportation instead of biking","Reasons given", "./pdf/PublicTransportationInsteadBike.pdf", "pt_instead_of_bike")
transportationBar("./data/PublicTransportationBike.csv", "Ward 23 survey respondents regarding bringing bikes within public transportation methods","Responces", "./pdf/PublicTransportationBike.pdf", "pt_bikes_on_transit")

'''
# Awareness and Infrastructure
'''
transportationSunburstPie("./data/BikeShareAwarenessSunburst.csv", "Ward 23 survey respondents regarding prior knowledge of the Bike Share Toronto program", "./pdf/BikeShareAwareness.pdf", "bikeshare_awareness")
transportationSunburstPie("./data/PublicTransportationBikeSunburst.csv", "Ward 23 survey respondents regarding bringing bikes within public transportation methods", "./pdf/PublicTransportationBikeSunburstPie.pdf", "pt_bikes_sunburst")
transportationBar("./data/BikingInfrastructure-HydroCorridors.csv", "Ward 23 survey respondents rating biking infrastructure, hydro corridors","Rating (1 is highest)", "./pdf/BikingInfrastructure-HydroCorridors.pdf", "infra_hydro_corridors")

'''
# Driving
'''
transportationBar("./data/DrivingInsteadBike.csv", "Ward 23 survey respondents justifying driving instead of biking","Rating (1 is highest)", "./pdf/DrivingInsteadBike.pdf", "driving_instead_of_bike")
