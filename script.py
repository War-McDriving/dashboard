import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import folium
from folium.plugins import HeatMap
import base64
import os

# Load data (replace this with your wardriving data source)
# Data must have columns: 'latitude', 'longitude', 'signal_strength'
# Data with clear coordinates for Belgium
data = pd.DataFrame({
    'latitude': [
        50.8503, 51.2194, 51.0543, 50.8798, 50.6326,  # Brussels, Antwerp, Ghent, Leuven, Namur
        51.0536, 51.0164, 50.9307, 50.6337, 50.4542   # Bruges, Mechelen, Hasselt, Liège, Mons
    ],
    'longitude': [
        4.3517, 4.4025, 3.7174, 4.7005, 4.8590,       # Brussels, Antwerp, Ghent, Leuven, Namur
        3.7057, 4.4808, 5.3378, 5.5675, 3.9567        # Bruges, Mechelen, Hasselt, Liège, Mons
    ],
    'signal_strength': [
        -60, -70, -50, -55, -65,                     # Example signal strengths
        -50, -58, -62, -70, -68
    ]
})


# Create a function to generate the heatmap
def generate_heatmap(data):
    m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=15)
    heat_data = [[row['latitude'], row['longitude'], row['signal_strength']] for _, row in data.iterrows()]
    HeatMap(heat_data, min_opacity=0.5, max_val=data['signal_strength'].max(), radius=15, blur=10).add_to(m)
    
    # Save map to an HTML file
    file_path = "map.html"
    m.save(file_path)
    return file_path

# Initialize Dash app
app = dash.Dash(__name__)

# Generate the initial heatmap
map_path = generate_heatmap(data)

# Layout
app.layout = html.Div([
    html.H1("Wardriving Heatmap Dashboard"),
    dcc.Upload(
        id="upload-data",
        children=html.Div(["Drag and Drop or ", html.A("Select a CSV File")]),
        style={
            "width": "100%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
        },
        multiple=False,
    ),
    html.Div(id="output-data-upload"),
    html.Iframe(id="map", srcDoc=open(map_path, "r").read(), width="100%", height="600")
])

# Callback to update the heatmap when a file is uploaded
@app.callback(
    Output("map", "srcDoc"),
    [Input("upload-data", "contents")]
)
def update_map(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # Parse the uploaded file as a CSV
            new_data = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            # Regenerate heatmap
            new_map_path = generate_heatmap(new_data)
            return open(new_map_path, "r").read()
        except Exception as e:
            return f"<p>Error processing file: {str(e)}</p>"
    return open(map_path, "r").read()

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
