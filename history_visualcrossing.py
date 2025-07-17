import os
import csv
import requests

API_KEY = os.getenv("VC_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

LOCATIONS = [
    {"name": "Everest ABC Camp", "lat": 28.0024, "lon": 86.8528},
    {"name": "Everest Summit",    "lat": 27.9881, "lon": 86.9250},
]

START = "2025-05-24T00:00:00"
END   = "2025-05-25T00:00:00"

# Pridedame naujus elementus: krituliai, sniegas, debesuotumas, matomumas, UV, radiacija, rasos taškas, gūsiai
HEADER = [
    "location","datetime_UTC",
    "temp_C","feelslike_C","dewpoint_C","humidity_%",
    "wind_speed_kph","wind_gust_kph","wind_dir_deg",
    "pressure_hPa","sealevelpressure_hPa",
    "precip_mm","snow_cm","snowdepth_cm",
    "cloudcover_%","visibility_km",
    "uvindex","solarradiation_W/m2"
]

ELEMENTS = ",".join([
    "datetime","temp","feelslike","dew","humidity",
    "windspeed","windgust","winddir",
    "pressure","sealevelpressure",
    "precip","snow","snowdepth",
    "cloudcover","visibility",
    "uvindex","solarradiation"
])

def fetch_location(loc):
    coords = f"{loc['lat']},{loc['lon']}"
    url = f"{BASE_URL}/{coords}/{START}/{END}"
    params = {
        "unitGroup":   "metric",
        "include":     "hours",
        "key":         API_KEY,
        "contentType": "json",
        "elements":    ELEMENTS
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    rows = []
    for day in data.get("days", []):
        for h in day.get("hours", []):
            rows.append([
                loc["name"],
                h.get("datetime"),
                h.get("temp"),
                h.get("feelslike"),
                h.get("dew"),
                h.get("humidity"),
                h.get("windspeed"),
                h.get("windgust"),
                h.get("winddir"),
                h.get("pressure"),
                h.get("sealevelpressure"),
                h.get("precip"),
                h.get("snow"),
                h.get("snowdepth"),
                h.get("cloudcover"),
                h.get("visibility"),
                h.get("uvindex"),
                h.get("solarradiation")
            ])
    return rows

def main():
    all_rows = []
    for loc in LOCATIONS:
        all_rows.extend(fetch_location(loc))

    with open("history_visualcrossing.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(all_rows)

if __name__ == "__main__":
    main()
