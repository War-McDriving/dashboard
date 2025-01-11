import pandas as pd
import plotly.express as px

# Load data from a file
data = pd.read_csv("../data/full.wiglecsv")

# Generate RSSI distribution plot
fig_rssi = px.histogram(data, x="RSSI", nbins=10, title="RSSI Distribution",
                        labels={"RSSI": "Signal Strength (RSSI)"}, template="plotly_white")
fig_rssi.update_layout(bargap=0.2)

# Generate channel usage plot
fig_channel = px.histogram(data, x="Channel", title="Channel Usage",
                           labels={"Channel": "Wi-Fi Channel"}, template="plotly_white")
fig_channel.update_layout(bargap=0.2)

# Generate map of Wi-Fi locations
fig_map = px.scatter_geo(data, lat="CurrentLatitude", lon="CurrentLongitude", hover_name="SSID",
                         size_max=10, title="Wi-Fi Locations", template="plotly_white")

# Save plots as HTML
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wi-Fi Analytics</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Wi-Fi Analytics</h1>
    <h2>RSSI Distribution</h2>
    {fig_rssi.to_html(full_html=False, include_plotlyjs=False)}

    <h2>Channel Usage</h2>
    {fig_channel.to_html(full_html=False, include_plotlyjs=False)}

    <h2>Wi-Fi Locations</h2>
    {fig_map.to_html(full_html=False, include_plotlyjs=False)}
</body>
</html>
"""

# Write HTML content to a file
with open("./templates/analytics.html", "w") as f:
    f.write(html_content)

print("Analytics HTML page generated: wifi_analytics.html")
