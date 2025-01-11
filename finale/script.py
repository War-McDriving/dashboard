import pandas as pd
from flask import Flask, render_template
import folium
from folium.plugins import HeatMap

app = Flask(__name__)

def create_heatmap(file_path):
    # Lees en filter relevante kolommen in één stap
    try:
        data = pd.read_csv(
            file_path,
            usecols=[
                "MAC",
                "SSID",
                "AuthMode",
                "FirstSeen",
                "Channel",
                "RSSI",
                "CurrentLatitude",
                "CurrentLongitude",
                "AltitudeMeters",
                "AccuracyMeters",
                "Type",
            ],
            low_memory=False,
        ).dropna()
    except KeyError:
        raise ValueError("De vereiste kolommen ontbreken in het bestand.")

    # Filter alleen numerieke waarden met een enkele selectie
    data = data[
        (data["CurrentLatitude"].apply(pd.api.types.is_number))
        & (data["CurrentLongitude"].apply(pd.api.types.is_number))
        & (data["RSSI"].apply(pd.api.types.is_number))
    ]

    # Groepeer op SSID en selecteer de coördinaat met de hoogste RSSI
    grouped_data = data.loc[data.groupby("SSID")["RSSI"].idxmax()].reset_index(
        drop=True
    )

    # Maak een Folium-kaart met gemiddelde coördinaten als middelpunt
    if not grouped_data.empty:
        map_center = [data["CurrentLatitude"].mean(), data["CurrentLongitude"].mean()]
        wifi_map = folium.Map(
            location=map_center, zoom_start=15, width="100%", height="400px"
        )

        # Voeg HeatMap toe
        heat_data = grouped_data[
            ["CurrentLatitude", "CurrentLongitude", "RSSI"]
        ].values.tolist()
        HeatMap(heat_data, min_opacity=0.5, radius=10, blur=15).add_to(wifi_map)

        # Opslaan als HTML
        map_file = "templates/heatmap.html"
        wifi_map.save(map_file)
    else:
        raise ValueError("Geen gegevens beschikbaar om een heatmap te genereren.")

    return grouped_data  # Retourneer gegroepeerde data voor weergave


@app.route("/")
def index():
    # CSV-bestandspad
    csv_file = "../data/full.wiglecsv"  # Pas aan naar het juiste bestandspad

    try:
        # Creëer heatmap en verkrijg gegroepeerde data
        data = create_heatmap(csv_file)
    except Exception as e:
        return f"Fout bij het verwerken van het bestand: {e}"

    # Render de hoofdtemplate met data
    return render_template("index.html", data=data.to_dict(orient="records"))


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/marker")
def marker():
    return render_template("myMap.html")


if __name__ == "__main__":
    app.run(debug=True)
