import httpx
import copy
import json
from pathlib import Path
import csv

url = "https://api.open-meteo.com/v1/forecast"
params = {"latitude": 40.70,
          "longitude": 13.41,
          "current": ["temperature_2m", "wind_speed_10m"]}

sites_path = f"{Path(__file__).resolve().parent}/sites.json"
csv_path = f"{Path(__file__).resolve().parent}/weather.csv"

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
    weather_list = []
    site_dict = load_sites(sites_path)

    for site in site_dict.values():
        try:
            data = fetch(url, params={"latitude": site["latitude"],
                                    "longitude": site["longitude"],
                                    "current": ["temperature_2m", "wind_speed_10m"]})

            weather_list.append(transform(data, site))
        except(json.JSONDecodeError) as e:
            print(f"Data returned another Data form: {e}")
        
        except(httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"Bad request: {e}")
            continue
            
        except KeyError as e:
            print(f"Data missing expected key: {e}")
    
    return weather_list
    
def weather_csv_writer(path, weather_list):
    fieldnames = ["site", "temp_c", "wind_kmh"]
    sorted_weather_list = sorted(weather_list, key= lambda x: x["site"])
    try:
        with open(path, mode="w", newline="") as weather_csv:
            writer = csv.DictWriter(weather_csv, fieldnames=fieldnames)
            writer.writeheader()
            written_row_count = 0
            for weather in sorted_weather_list:
                writer.writerow(weather)
                written_row_count += 1
            print(f"{written_row_count}/{len(sorted_weather_list)} rows completed successfully")

    except FileNotFoundError:
        print(f"Error: The directory path for '{path}' is invalid or could not be found")

    except (ValueError, TypeError) as e:
        print(f"Data structure error (check dictionary keys and row types): {e}")
    
    except OSError as e:
        print(f"Operating System Error: {e}")


def main():
    # data = fetch(url, params)
    # site = {"name": "Queens, New York", "lat":data["latitude"], "lon":data["longitude"]}
    # weather_dict = transform(data, site)
    # print(load_sites(sites_path))
    w_list = caller(sites_path, url)
    weather_csv_writer(csv_path, w_list)




if __name__ == "__main__":
    main()