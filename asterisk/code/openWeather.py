#!/usr/bin/env python3
import requests
import sys

# ⚠️ Mets ta clé API OpenWeatherMap ici
API_KEY = "aecb5d1e853db9fb89ef6d2df8f73869"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Ville par défaut si aucun argument
ville = sys.argv[1] if len(sys.argv) > 1 else "Antananarivo"

try:
    params = {"q": ville, "appid": API_KEY, "units": "metric", "lang": "fr"}
    r = requests.get(BASE_URL, params=params)
    data = r.json()

    if r.status_code == 200:
        temp = round(data["main"]["temp"])
        print("SET VARIABLE TEMP %s" % temp)  # format : température,risque pluie %
    else:
        print("SET VARIABLE TEMP %s" % temp)  # erreur API

except Exception:
    print("SET VARIABLE TEMP %s" % temp)
