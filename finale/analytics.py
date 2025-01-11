import pandas as pd
import plotly.express as px

# Load data from the provided sample
data = pd.read_csv("../data/full.wiglecsv")

# Clean data if necessary (e.g., drop rows with missing 'AuthMode' or 'RSSI')
data = data.dropna(subset=['AuthMode', 'RSSI'])

# 1. Authentication Mode (WPA Security) Distribution
auth_mode_usage = data['AuthMode'].value_counts().reset_index()
auth_mode_usage.columns = ['Auth Mode', 'Count']

# 2. Signal Strength (RSSI) by Channel
rssi_by_channel = data.groupby('Channel')['RSSI'].describe()


# 4. Top SSIDs by Network Count
ssid_count = data['SSID'].value_counts().reset_index()
ssid_count.columns = ['SSID', 'Count']

# Plotting the Authentication Mode Usage
fig_auth_mode = px.bar(auth_mode_usage, x='Auth Mode', y='Count', title="Authentication Mode Distribution",
                       labels={"Auth Mode": "Authentication Mode", "Count": "Number of Networks"},
                       template="plotly_white")
fig_auth_mode.update_layout(bargap=0.2)

# Plotting Signal Strength (RSSI) by Channel
fig_rssi_channel = px.box(data, x="Channel", y="RSSI", title="Signal Strength (RSSI) by Channel",
                          labels={"Channel": "Channel", "RSSI": "Signal Strength (RSSI)"},
                          template="plotly_white")
fig_rssi_channel.update_layout(bargap=0.2)

# Plotting the Top 20 SSIDs by Count
fig_ssid_count = px.bar(ssid_count.head(20), x='SSID', y='Count', title="Top 20 SSIDs by Count",
                        labels={"SSID": "Network SSID", "Count": "Frequency of Occurrence"},
                        template="plotly_white")
fig_ssid_count.update_layout(bargap=0.2)

# Generate HTML content for the analysis page
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wi-Fi Network Analysis</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Wi-Fi Network Analysis</h1>
    
    <h2>Authentication Mode Distribution</h2>
    {fig_auth_mode.to_html(full_html=False, include_plotlyjs=False)}
    
    <h2>Signal Strength (RSSI) by Channel</h2>
    {fig_rssi_channel.to_html(full_html=False, include_plotlyjs=False)}
    
    <h2>Top 20 SSIDs by Count</h2>
    {fig_ssid_count.to_html(full_html=False, include_plotlyjs=False)}

</body>
</html>
"""

# Write HTML content to a file
with open("./templates/analytics.html", "w") as f:
    f.write(html_content)

print("Wi-Fi Network Analysis HTML page generated: wi_fi_analysis.html")