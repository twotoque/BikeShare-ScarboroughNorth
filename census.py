from dash import Dash, dcc, html, Input, Output
import plotly.express as px
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
carValues = rowArray[0].iloc[1:].values
transitValues = rowArray[1].iloc[1:].values

x_values = rowArray[0].index[1:]

#Plot data:
plot_censusData = pandas.DataFrame({
    'Neighbourhood': x_values,
    'Car': carValues,
    'Transit': transitValues,
})

# Melt the DataFrame to long format
plotMelt_censusData = plot_censusData.melt(id_vars='Neighbourhood', var_name='Category', value_name='Value')

# Plot the stacked bar chart
fig = px.bar(plotMelt_censusData, x='Neighbourhood', y='Value', color='Category', title='Neighbourhood Values')

fig.show()

print(plotMelt_censusData)
'''
app = Dash(__name__)



y_values_str = row.values[1:]
y_values = pandas.to_numeric(y_values_str)
print("x values:", x_values)
print("y values:", y_values)

plot_censusData = pandas.DataFrame({
    'Neighbourhood': x_values,
    'Value': y_values
})

fig = px.bar(plot_censusData, x='Neighbourhood', y='Value', title='Neighbourhood Values')
fig.update_layout(yaxis=dict(range=[0, max(y_values) + 10]))

fig.show()

def export_pdf(fig):
    fig.write_image("figure.pdf", format="pdf")
    return 

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "exportpdf":
        export_pdf(fig)

app.run_server(debug=True)

    'Transit': rowArray[1].iloc[1:].values,
    'Walk': rowArray[2].iloc[1:].values,  
    'Bike': rowArray[3].iloc[1:].values,  
    'Other': rowArray[4].iloc[1:].values
'''