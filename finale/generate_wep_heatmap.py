import pandas as pd
import folium
from folium.plugins import HeatMap

# Load data from the provided sample
data = pd.read_csv("../data/full.wiglecsv")

# Filter data for networks using WEP encryption
wep_networks = data[data['AuthMode'].str.contains('WEP', na=False)]

# Check if there are any WEP networks
if not wep_networks.empty:
    # Create a heatmap of WEP networks
    heatmap_data = wep_networks[['CurrentLatitude', 'CurrentLongitude']].dropna()

    # Create a Folium map centered around the average location of WEP networks
    map_center = [heatmap_data['CurrentLatitude'].mean(), heatmap_data['CurrentLongitude'].mean()]
    wep_heatmap = folium.Map(location=map_center, zoom_start=13)

    # Add heatmap layer
    HeatMap(heatmap_data.values.tolist()).add_to(wep_heatmap)

    # Save the heatmap to an HTML file
    wep_heatmap.save('./templates/wep_heatmap.html')
    print("WEP Heatmap generated: wep_heatmap.html")
else:
    print("No WEP networks found.") 