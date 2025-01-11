import pandas as pd
import folium
from folium.plugins import MarkerCluster
import re

# Define file paths
CSV_FILE = '../data/full.wiglecsv'  # Update with your CSV file path
OUTPUT_HTML = './templates/myMap.html'  # Output HTML file

def sanitize_popup_content(content):
    """
    Sanitize the popup content to avoid JavaScript issues.
    """
    return re.sub(r"[\\`$]", lambda match: f"\\{match.group()}", content)

def read_and_filter_csv(file_path):
    """
    Read the CSV file and filter relevant data.
    """
    # Load only necessary columns and drop rows with missing coordinates
    try:
        df = pd.read_csv(file_path, usecols=[
            "MAC", "SSID", "RSSI", "CurrentLatitude", "CurrentLongitude"
        ])
    except KeyError:
        raise ValueError("CSV file is missing required columns.")
    
    # Drop rows with NaN coordinates or RSSI values
    df = df.dropna(subset=["CurrentLatitude", "CurrentLongitude", "RSSI"])
    
    # Filter high RSSI values (e.g., stronger than -80 dBm)
    df = df[df["RSSI"] > -80]

    # Remove duplicate rows based on unique SSID and MAC
    df = df.drop_duplicates(subset=["MAC", "SSID", "CurrentLatitude", "CurrentLongitude"])

    return df

def create_marker_cluster_map(df, output_path):
    """
    Create and save an interactive map with MarkerCluster.
    """
    if df.empty:
        print("No valid data to plot on the map.")
        return

    # Initialize the map at the average location
    map_center = [df["CurrentLatitude"].mean(), df["CurrentLongitude"].mean()]
    m = folium.Map(location=map_center, zoom_start=13)

    # Add MarkerCluster with optimized options
    marker_cluster = MarkerCluster(
        disableClusteringAtZoom=15,  # Show individual markers at higher zoom levels
        spiderfyOnMaxZoom=True      # Expand clusters into individual markers
    ).add_to(m)

    # Batch precompute sanitized popup content
    df["PopupContent"] = df.apply(
        lambda row: sanitize_popup_content(f"""
            <b>SSID:</b> {row['SSID'] if pd.notna(row['SSID']) else 'No SSID'}<br>
            <b>MAC:</b> {row['MAC']}<br>
            <b>Signal Strength (RSSI):</b> {row['RSSI']} dBm<br>
            <b>Latitude:</b> {row['CurrentLatitude']}<br>
            <b>Longitude:</b> {row['CurrentLongitude']}
        """),
        axis=1,
    )

    # Add all markers in batch
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["CurrentLatitude"], row["CurrentLongitude"]],
            popup=row["PopupContent"]
        ).add_to(marker_cluster)

    # Save the map to an HTML file
    m.save(output_path)
    print(f"MarkerCluster map saved as {output_path}")

def generate_interactive_map(csv_file, output_html):
    """
    Main function to generate the interactive map.
    """
    try:
        print("Reading and processing data...")
        df = read_and_filter_csv(csv_file)
        print(f"Loaded {len(df)} rows of valid data after filtering and removing duplicates.")
        
        print("Generating the interactive map...")
        create_marker_cluster_map(df, output_html)
    except Exception as e:
        print(f"Error: {e}")

# Run the program
if __name__ == "__main__":
    generate_interactive_map(CSV_FILE, OUTPUT_HTML)
