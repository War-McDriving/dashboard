# Wi-Fi Network Analysis Dashboard

A comprehensive dashboard for analyzing Wi-Fi networks, featuring interactive visualizations, WEP network detection, and detailed analytics.

## Features

- **Interactive Network Map**: Visualize Wi-Fi networks with heatmap and marker clustering
- **Analytics Dashboard**: 
  - Authentication Mode Distribution
  - Wi-Fi Generation Distribution
  - Signal Strength Analysis
  - Channel Distribution
- **WEP Network Detection**: Dedicated view for identifying potentially vulnerable WEP networks
- **Responsive Design**: Mobile-friendly interface with dynamic layouts

## Prerequisites

- Python 3.x
- Required Python packages:
  ```bash
  pip install pandas plotly folium
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/wifi-dashboard.git
   cd wifi-dashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Place your WiGLE CSV file in the `data` directory as `full.wiglecsv`

## Usage

1. Start the Flask server:
   ```bash
   python script.py
   ```

2. Access the dashboard at `http://localhost:5000`

## Project Structure

- `/finale`
  - `analytics.py` - Generates analytics visualizations
  - `generate_wep_heatmap.py` - Creates WEP network heatmap
  - `generate_pie_charts.py` - Generates pie chart visualizations
  - `interactive.py` - Handles interactive map features
  - `script.py` - Main Flask application
- `/templates` - HTML templates
- `/static` - Static assets
- `/data` - Data directory for WiGLE CSV files

## Features in Detail

### Analytics Dashboard
- Authentication mode distribution (WPA, WEP, Open)
- Wi-Fi generation analysis (Wi-Fi 5/6/7)
- Signal strength distribution
- Channel usage analysis

### WEP Network Detection
- Heatmap visualization of WEP networks
- Detailed table with network information
- MAC address and SSID listing

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Flask, Plotly, and Folium
- Inspired by WiGLE's Wi-Fi database

