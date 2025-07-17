import os
import csv
import requests

# Imame API raktą iš GitHub Secrets
API_KEY = os.getenv("VC_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# Vietovės: ABC stovykla ir viršūnė
LOCATIONS = [
    {"name": "Everest ABC Camp", "lat": 28.0024, "lon": 86.8528},
    {"name": "Everest Summit",    "lat": 27.9881, "lon": 86.9250},
]

# Intervalas ISO formatu
START = "2025-05-24T00:00:00"
END   = "2025-05-25T00:00:00"

# CSV antraštė
HEADER = [
    "location",
    "datetime_UTC",
    "temp_C",
    "feelslike_C",
    "humidity_%",
    "wind_speed_kph",
    "wind_dir_deg",
    "pressure_hPa"
]

def fetch_location(loc):
    coords = f"{loc['lat']},{loc['lon']}"
    url = f"{BASE_URL}/{coords}/{START}/{END}"
    params = {
        "unitGroup":   "metric",
        "include":     "hours",
        "key":         API_KEY,
        "contentType": "json",
        "elements":    "datetime,temp,feelslike,humidity,windspeed,winddir,pressure"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    rows = []
    for day in data.get("days", []):
        for h in day.get("hours", []):
            rows.append([
                loc["name"],
                h["datetime"],
                h.get("temp"),
                h.get("feelslike"),
                h.get("humidity"),
                h.get("windspeed"),
                h.get("winddir"),
                h.get("pressure")
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
