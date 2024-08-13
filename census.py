from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas 

censusData = pandas.read_csv('data/Ward23CensusData.csv')
row = censusData.iloc[2581]



app = Dash(__name__)
import plotly.express as px
import pandas 

censusData = pandas.read_csv('data/Ward23CensusData.csv')
row = censusData.iloc[2581]
print(row)


x_values = row.index[1:] 
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
        fig = update_bar_chart("Fri")  
        export_pdf(fig)
    else:
        print("Error generating pdf output")


app.run_server(debug=True)