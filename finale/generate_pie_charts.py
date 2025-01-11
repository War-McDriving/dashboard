import pandas as pd
import plotly.express as px

# Load data from the provided sample
data = pd.read_csv("../data/full.wiglecsv")

# Clean data if necessary (e.g., drop rows with missing 'AuthMode' or 'RSSI')
data = data.dropna(subset=['AuthMode', 'RSSI'])

# 1. Authentication Mode Distribution
auth_mode_usage = data['AuthMode'].value_counts().reset_index()
auth_mode_usage.columns = ['Auth Mode', 'Count']

# Create a pie chart for Authentication Mode Distribution
fig_auth_mode = px.pie(auth_mode_usage, names='Auth Mode', values='Count', title="Authentication Mode Distribution",
                       template="plotly_white", color='Auth Mode', color_discrete_sequence=px.colors.qualitative.Set2)

# Save the pie chart as an HTML file
fig_auth_mode.write_html('./templates/auth_mode_distribution.html')

# 2. Wi-Fi Generation Distribution
# Define a function to determine Wi-Fi generation
def get_wifi_generation(channel):
    if 36 <= channel <= 165:
        return "Wi-Fi 5 (802.11ac)"
    elif 1 <= channel <= 233:
        if channel <= 64:
            return "Wi-Fi 6 (802.11ax)"
        else:
            return "Wi-Fi 7 (802.11be)"
    else:
        return "Unknown"

# Apply the function to create a new column for Wi-Fi generation
data['Wi-Fi Generation'] = data['Channel'].apply(get_wifi_generation)

wifi_gen_usage = data['Wi-Fi Generation'].value_counts().reset_index()
wifi_gen_usage.columns = ['Wi-Fi Generation', 'Count']

# Create a pie chart for Wi-Fi Generation Distribution
fig_wifi_gen = px.pie(wifi_gen_usage, names='Wi-Fi Generation', values='Count', title="Wi-Fi Generation Distribution",
                      template="plotly_white", color='Wi-Fi Generation', color_discrete_sequence=px.colors.qualitative.Set3)

# Save the pie chart as an HTML file
fig_wifi_gen.write_html('./templates/wifi_generation_distribution.html')

print("Pie charts generated: auth_mode_distribution.html and wifi_generation_distribution.html") 