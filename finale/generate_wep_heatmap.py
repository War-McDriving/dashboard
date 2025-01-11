import pandas as pd
import folium
from folium.plugins import HeatMap

# Load data from the provided sample (adjust path if necessary)
data = pd.read_csv("../data/full.wiglecsv")

# Print the column names to verify available columns
print("Available columns:", data.columns)

# Filter data for networks using WEP encryption
wep_networks = data[data['AuthMode'].str.contains('WEP', na=False)]

# Check if there are any WEP networks
if not wep_networks.empty:
    # The first column contains MAC addresses, so use that as the BSSID
    bssid_column = data.columns[0]  # Assumes the first column is the MAC address (BSSID)

    # Create a heatmap of WEP networks
    heatmap_data = wep_networks[['CurrentLatitude', 'CurrentLongitude']].dropna()

    # Create a Folium map centered around the average location of WEP networks
    map_center = [heatmap_data['CurrentLatitude'].mean(), heatmap_data['CurrentLongitude'].mean()]
    wep_map = folium.Map(location=map_center, zoom_start=13)

    # Add heatmap layer
    HeatMap(heatmap_data.values.tolist()).add_to(wep_map)

    # Add pinpoints (markers) for each WEP network
    for _, row in wep_networks.iterrows():
        latitude = row['CurrentLatitude']
        longitude = row['CurrentLongitude']
        mac_address = row[bssid_column]
        
        # Add a marker for each WEP network
        folium.Marker(
            location=[latitude, longitude],
            popup=f"MAC: {mac_address}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(wep_map)

    # Create the SSID and MAC address table, including missing SSID rows
    ssid_table = wep_networks[['SSID', bssid_column, 'CurrentLatitude', 'CurrentLongitude']]

    # Check if the SSID is empty or NaN, then append the MAC address
    ssid_table['SSID'] = ssid_table.apply(lambda row: row['SSID'] if pd.notnull(row['SSID']) and row['SSID'] != '' 
                                          else f"NaN", axis=1)

    # Remove duplicates based on SSID and BSSID (MAC address)
    ssid_table = ssid_table.drop_duplicates(subset=['SSID', bssid_column])

    # Generate the HTML table
    table_html = ssid_table.to_html(classes='table table-striped table-hover', index=False)

    # Combine the map and table into a single HTML file
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WEP Networks Map and SSID Table</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
            }}
            h1 {{
                text-align: center;
                color: #0056b3;
                margin-top: 20px;
            }}
            h2 {{
                text-align: center;
                color: #0056b3;
                margin-top: 20px;
            }}
            .container {{
                display: grid;
                grid-template-columns: 70% 30%;  /* Adjusted for wider table */
                gap: 20px;
                width: 100%;
            }}
            #map {{
                width: 100%;
                height: 500px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .table-container {{
                width: 100%;
                height: 85vh;
                overflow-y: auto;
            }}
            .table {{
                width: 100%;
                border-collapse: collapse;
                border-radius: 8px;
                overflow: hidden;
                background-color: #fff;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                font-size: 10px
            }}
            .table th, .table td {{
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            .table th {{
                background-color: #0056b3;
                color: #fff;
            }}
            .table tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .table tr:hover {{
                background-color: #ddd;
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
            <a href="/wep" class="navButton">WEP</a>
            <a href="/contact" class="navButton">Contact</a>
        </nav>
        <h1>WEP Networks Map and SSID Table</h1>
        <div class="container">
            <div id="map">
                {wep_map._repr_html_()}  <!-- Embed the Folium map with heatmap -->
            </div>
            <div class="table-container">
                {table_html}
            </div>
        </div>
    </body>
    </html>
    """

    # Save the combined HTML page
    with open('./templates/wep.html', 'w') as f:
        f.write(html_content)

    print("WEP Network Map with heatmap and SSID table generated: wep.html")
else:
    print("No WEP networks found.")
