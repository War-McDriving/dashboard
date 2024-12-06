import dash
from dash import dcc, html
import pandas as pd
import folium
from folium.plugins import HeatMap

# Load data with only Antwerp coordinates
data = pd.DataFrame({
    'latitude': [
        51.2194, 51.2194, 51.2194, 51.2200, 51.2180, 51.2210, 51.2175, 51.2068527
    ],
    'longitude': [
        4.4025, 4.4025, 4.4025, 4.4030, 4.4010, 4.4040, 4.4005, 4.4298909
    ],
    'signal_strength': [
        -70, -68, -65, -60, -75, -55, -80, 60
    ]
})

# Create a function to generate the heatmap
def generate_heatmap(data):
    m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=13)
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
    html.H1("War McDriving Heatmap Dashboard"),
    html.Iframe(id="map", srcDoc=open(map_path, "r").read(), width="100%", height="600")
])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
