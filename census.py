from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas
i = 0 
n = 0
rowArray = []
selectArray = []

#What row to see? 
carRowSelect = 2577
transitRowSelect = 2580
walkRowSelect = 2581
bikeRowSelect = 2582
otherRowSelect = 2583

#Number of neighbourhoods
neighbourhoods = 5

#Due to the way the census csv is formatted, it counts the header as a row, plus zero indexing. 
selectArray = [carRowSelect - 2, transitRowSelect - 2, walkRowSelect - 2, bikeRowSelect - 2, otherRowSelect - 2]

#Load census csv data
censusData = pandas.read_csv('data/Ward23CensusData.csv')

for i in range(neighbourhoods):
    rowArray.append(censusData.iloc[selectArray[i]])
    i += 1

#Values 
carValues = list(map(int, rowArray[0].iloc[1:].values))
transitValues = list(map(int, rowArray[1].iloc[1:].values))
walkValues = list(map(int, rowArray[2].iloc[1:].values))
bikeValues = list(map(int, rowArray[3].iloc[1:].values))
otherValues = list(map(int, rowArray[4].iloc[1:].values))
numberValues = 5

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

fig_bar.write_image("figure.pdf", format="pdf", engine='kaleido')

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "exportpdf":
        export_pdf(fig)

app.run_server(debug=True)
