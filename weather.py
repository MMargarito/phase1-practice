import httpx
import copy
import json
from pathlib import Path

url = "https://api.open-meteo.com/v1/forecast"
params = {"latitude": 40.70,
          "longitude": 13.41,
          "current": ["temperature_2m", "wind_speed_10m"]}

sites_path = f"{Path(__file__).resolve().parent}/sites.json"

def load_sites(sites_path):
    try:
        with open(sites_path) as sites:
            s_load = json.load(sites)
    except FileNotFoundError:
        print(f"Could not find sites file: {sites_path}")
        return {}
    else:
        return s_load

def fetch(url, params):
    response = httpx.get(url, params=params, timeout=10) 
    response.raise_for_status()
    data = response.json()
    return data  


def transform(data, site):
    return {"site": site["name"],
            "temp_c": data["current"]["temperature_2m"],
            "wind_kmh": data["current"]["wind_speed_10m"]}

def caller(site_json, url):
    weather_dict = []
    site_dict = load_sites(sites_path)

    for site in site_dict.values():
        try:
            data = fetch(url, params={"latitude": site["latitude"],
                                    "longitude": site["longitude"],
                                    "current": ["temperature_2m", "wind_speed_10m"]})
        
        except(json.JSONDecodeError) as {e}:
            print(f"Data returned another Data form: {e}")
        
        except(httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"Bad request: {e}")
        
        try:
            weather_dict.append(transform(data, site))
        except KeyError as e:
            print(f"Data missing expected key: {e}")
    
    return weather_dict
    

def main():
    # data = fetch(url, params)
    # site = {"name": "Queens, New York", "lat":data["latitude"], "lon":data["longitude"]}
    # weather_dict = transform(data, site)
    # print(load_sites(sites_path))
    print(caller(sites_path, url))
    


if __name__ == "__main__":
    main()