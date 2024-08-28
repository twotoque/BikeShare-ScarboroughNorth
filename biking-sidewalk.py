from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas

def bikingInfrastructBar(filePath):  
    i = 0 
    n = 0
    rowArray = []
    selectArray = []
    traceList = []

    #Load census csv data
    fileData = pandas.read_csv(filePath)

    fileDataFrame = pandas.DataFrame(fileData)
    

    print(fileDataFrame.iloc[1][1:])
    neighbourhoodList = list(fileDataFrame.columns[1:])

    for i in enumerate(fileDataFrame):
        x_values = ["1 (most safest)", "2", "3", "4", "5", "6 (least safe)"]  
        y_values = fileDataFrame.iloc[i].value_counts()  
        trace = go.Bar(name=neighbourhoodList[i], x=x_values, y=y_values)
        traceList.append(trace)

    fig_bar = go.Figure(data=traceList)


    fig_bar.update_layout(barmode="stack")
    fig_bar.show()

    '''
    fig_bar.update_layout(
        title='Main mode of commuting for the employed labour force aged 15 years and over with a usual place of work or no fixed workplace address - 25% sample data, Census 2021',
        xaxis_title='Neighbourhood',
        yaxis_title='Value',
        barmode='stack'  
    )
    


    x_values = rowArray[0].index[1:]

    #Plot data:
    plot_censusData = pandas.DataFrame({
        'Neighbourhood': x_values,
        'Car': carValues,
        'Transit': transitValues,
        'Walk': walkValues,
        'Bike': bikeValues,
        'Other': otherValues,
    })

    #Melt the DataFrame to long format
    plotMelt_censusData = plot_censusData.melt(id_vars='Neighbourhood', var_name='Category', value_name='Value')

    #Assign bar graph variable
    fig_bar = go.Figure()

    #Plotly tracing
    for category in plotMelt_censusData['Category'].unique():
        category_data = plotMelt_censusData[plotMelt_censusData ['Category'] == category]
        fig_bar.add_trace(go.Bar(
            x=category_data['Neighbourhood'],
            y=category_data['Value'],
            name=category
        ))


    #Render bar graph
    fig_bar.update_layout(
        title='Main mode of commuting for the employed labour force aged 15 years and over with a usual place of work or no fixed workplace address - 25% sample data, Census 2021',
        xaxis_title='Neighbourhood',
        yaxis_title='Value',
        barmode='stack'  
    )

    fig_bar.show()

    def export_pdf(fig):
        fig.write_image("figure.pdf", format="pdf")
        return 

    if __name__ == "__main__":
        import sys
        if len(sys.argv) > 1 and sys.argv[1] == "exportpdf":
            export_pdf(fig)

    app.run_server(debug=True)
    '''

bikingInfrastructBar("./data/BikingInfrastructure-Sidewalks.csv")



