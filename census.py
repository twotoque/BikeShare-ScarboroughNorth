from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas 

censusData = px.data.tips()

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Restaurant tips by day of week'),
    dcc.Dropdown(
        id="dropdown",
        options=["Fri", "Sat", "Sun"],
        value="Fri",
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))

def update_bar_chart(day):
    mask = censusData["day"] == day
    fig = px.bar(censusData[mask], x="sex", y="total_bill", 
                 color="smoker", barmode="group")
    return fig

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