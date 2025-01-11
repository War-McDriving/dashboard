import pandas as pd
import plotly.express as px

# Load data from the provided sample
data = pd.read_csv("../data/full.wiglecsv")

# Clean data if necessary (e.g., drop rows with missing 'AuthMode' or 'RSSI')
data = data.dropna(subset=['AuthMode', 'RSSI'])

# Add Wi-Fi Generation based on Channel
def get_wifi_generation(channel):
    if 36 <= channel <= 165:
        return "Wi-Fi 5 (802.11ac)"
    elif 1 <= channel <= 233:
        if channel <= 64:
            return "Wi-Fi 6 (802.11ax)"
        else:
            return "Wi-Fi 7 (802.11be)"  # Assuming Wi-Fi 7 uses the higher channels, you could adjust based on more precise details
    else:
        return "Unknown"

# Apply the function to create a new column for Wi-Fi generation
data['Wi-Fi Generation'] = data['Channel'].apply(get_wifi_generation)

# 1. Authentication Mode (WPA Security) Distribution
auth_mode_usage = data['AuthMode'].value_counts().reset_index()
auth_mode_usage.columns = ['Auth Mode', 'Count']

# 2. Wi-Fi Generation Distribution
wifi_gen_usage = data['Wi-Fi Generation'].value_counts().reset_index()
wifi_gen_usage.columns = ['Wi-Fi Generation', 'Count']

# 3. Top SSIDs by Network Count
ssid_count = data['SSID'].value_counts().reset_index()
ssid_count.columns = ['SSID', 'Count']

# Plotting the Authentication Mode Usage as a Pie Chart
fig_auth_mode = px.pie(auth_mode_usage, names='Auth Mode', values='Count', title="Authentication Mode Distribution",
                       template="plotly_white", color='Auth Mode', color_discrete_sequence=px.colors.qualitative.Set2)

# Plotting the Wi-Fi Generation Usage
fig_wifi_gen = px.bar(wifi_gen_usage, x='Wi-Fi Generation', y='Count', title="Wi-Fi Generation Distribution",
                       labels={"Wi-Fi Generation": "Wi-Fi Generation", "Count": "Number of Networks"},
                       template="plotly_white", color='Wi-Fi Generation', color_discrete_sequence=px.colors.qualitative.Set3)
fig_wifi_gen.update_layout(bargap=0.2)

# Plotting the Top 20 SSIDs by Count
fig_ssid_count = px.bar(ssid_count.head(20), x='SSID', y='Count', title="Top 20 SSIDs by Count",
                        labels={"SSID": "Network SSID", "Count": "Frequency of Occurrence"},
                        template="plotly_white", color='SSID', color_discrete_sequence=px.colors.qualitative.Pastel)
fig_ssid_count.update_layout(bargap=0.2)

# Generate HTML content with better styles
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wi-Fi Network Analysis</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        /* General Body Styles */
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
            color: #333;
        }}

        /* Header Styles */
        h1 {{
            text-align: center;
            color: #4a90e2;
            margin-top: 50px;
        }}

        h2 {{
            color: #4a90e2;
            text-align: center;
            margin-top: 30px;
        }}

        /* Chart Container Styles */
        .chart-container {{
            margin: 20px auto;
            width: 90%;
            max-width: 1000px;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}

        .chart-container:hover {{
            transform: translateY(-5px);
        }}

        .chart-container h2 {{
            margin-bottom: 20px;
            color: #333;
        }}

        /* Footer Styles */
        .footer {{
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #aaa;
        }}

        .footer a {{
            color: #4a90e2;
            text-decoration: none;
        }}

        /* Navigation Bar Styles */
        nav {{
            background-color: #333;
            overflow: hidden;
        }}

        nav .logo {{
            float: left;
            padding: 8px 16px;
        }}

        nav .logo img {{
            height: 40px;
            vertical-align: middle;
        }}

        nav .logo:active {{
            opacity: 0.7;
            transform: scale(0.95); /* Slightly shrink the logo on click */
        }}

        nav .logo img:hover {{
            cursor: pointer;
            transform: scale(1.05); /* Slightly enlarge the logo on hover */
        }}

        .navButton {{
            float: left;
            display: block;
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }}

        .navButton:hover {{
            background-color: #4a90e2;
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            body {{
                font-size: 14px;
            }}

            .chart-container {{
                width: 95%;
                padding: 15px;
            }}

            nav .logo {{
                padding: 5px 10px;
            }}

            nav .navButton {{
                padding: 12px 14px;
            }}

            h1, h2 {{
                font-size: 1.5em;
            }}

            .footer {{
                font-size: 12px;
            }}
        }}
    </style>
</head>
<body>
    <nav>
        <a href="/">
            <div class="logo">
                <img src="../static/warmcdriving-logo.png" alt="WiFi Heatmap Logo">
            </div>
        </a>
        <a href="/analytics" class="navButton">Analytics</a>
        <a href="/contact" class="navButton">Contact</a>
    </nav>

    <h1>Wi-Fi Network Analysis</h1>

    <div class="chart-container">
        <h2>Authentication Mode Distribution</h2>
        {fig_auth_mode.to_html(full_html=False, include_plotlyjs=False)}
    </div>

    <div class="chart-container">
        <h2>Wi-Fi Generation Distribution</h2>
        {fig_wifi_gen.to_html(full_html=False, include_plotlyjs=False)}
    </div>

    <div class="chart-container">
        <h2>Top 20 SSIDs by Count</h2>
        {fig_ssid_count.to_html(full_html=False, include_plotlyjs=False)}
    </div>

    <div class="footer">
        <p>Analysis generated by Wi-Fi Network Analytics. For more insights, visit <a href="#">our website</a>.</p>
    </div>
</body>
</html>
"""

# Write the updated HTML content to a file
with open("./templates/analytics.html", "w") as f:
    f.write(html_content)

print("Wi-Fi Network Analysis HTML page updated: wi_fi_analysis.html")
