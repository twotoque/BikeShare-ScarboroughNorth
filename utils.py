import os

def export_html(fig, name):
    """Generates a responsive HTML iframe for a Plotly figure."""
    if not os.path.exists("./html"):
        os.makedirs("./html")

    html_string = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                padding: 10px;
                box-sizing: border-box;
                overflow: hidden;
            }}
        </style>
    </head>
    <body>
        {fig.to_html(include_plotlyjs=False, full_html=False, div_id='plotly-div')}
    </body>
    </html>
    """
    
    with open(f"./html/{name}.html", 'w', encoding='utf-8') as f:
        f.write(html_string)
    print(f"Exported HTML: ./html/{name}.html")