import pandas as pd
import folium
from folium.plugins import MarkerCluster
import re

# Define your CSV file path and output HTML file
csv_file = 'Kismet-20250102-05-16-35-1.wiglecsv'  # Update with your CSV file path
output_html = 'myMap.html'  # Output HTML file

# Function to sanitize the popup content
def sanitize_popup_content(content):
    # Replace any backslashes or special characters to avoid JavaScript errors
    content = re.sub(r'\\', r'\\\\', content)  # Escape backslashes
    content = re.sub(r'`', r'\`', content)  # Escape backticks (if any)
    content = re.sub(r'\$', r'\$', content)  # Escape dollar signs (used in JS templating)
    return content

# Function to read the CSV file using pandas and extract relevant data
def read_csv(file_path):
    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Filter rows where latitude and longitude are not null
    df = df.dropna(subset=['CurrentLatitude', 'CurrentLongitude'])
    
    return df

# Function to create the interactive map
def create_map(df, output_path):
    # Initialize the map at a central location (average lat/long of your data)
    m = folium.Map(location=[df['CurrentLatitude'].mean(), df['CurrentLongitude'].mean()], zoom_start=15)
    
    # Create a marker cluster to group nearby markers
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add markers for each WiFi access point
    for _, row in df.iterrows():
        lat = row['CurrentLatitude']
        lon = row['CurrentLongitude']
        rssi = row['RSSI']
        ssid = row['SSID'] if pd.notna(row['SSID']) else 'No SSID'
        
        # Popup content for each marker
        popup_content = f"""
        <b>SSID:</b> {ssid}<br>
        <b>MAC:</b> {row['MAC']}<br>
        <b>Signal Strength (RSSI):</b> {rssi} dBm<br>
        <b>Latitude:</b> {lat}<br>
        <b>Longitude:</b> {lon}
        """
        
        # Sanitize the popup content to avoid JavaScript issues
        sanitized_content = sanitize_popup_content(popup_content)
        
        # Add a marker to the map with the sanitized popup
        folium.Marker([lat, lon], popup=sanitized_content).add_to(marker_cluster)
    
    # Save the map to an HTML file
    m.save(output_path)
    print(f"Interactive map saved as {output_path}")

# Main function to generate the interactive map
def generate_interactive_map(csv_file, output_html):
    df = read_csv(csv_file)
    create_map(df, output_html)

# Run the program
generate_interactive_map(csv_file, output_html)
