import httpx
import json
from pathlib import Path
import csv

url = "https://api.open-meteo.com/v1/forecast"

sites_path = f"{Path(__file__).resolve().parent}/sites.json"
csv_path = f"{Path(__file__).resolve().parent}/site_weather.csv"

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

def caller(sites_path, url):
    weather_list = []
    site_dict = load_sites(sites_path)
    success_count = 0
    for site in site_dict.values():
        try:
            data = fetch(url, params={"latitude": site["latitude"],
                                    "longitude": site["longitude"],
                                    "current": ["temperature_2m", "wind_speed_10m"]})

            weather_list.append(transform(data, site))
            success_count += 1

        except(json.JSONDecodeError) as e:
            print(f"Data returned another Data form {site}: {e}")
        
        except httpx.HTTPStatusError as e:
            print(f"Bad request for site: {site['name']}: {e}")
            
        except httpx.RequestError as e:
            print(f"No response for site: {site['name']}: {e}")
            
        except KeyError as e:
            print(f"Data missing expected key for site {site['name']}: {e}")
    
    print(f"{success_count} succeeded, {len(site_dict) - success_count} failed")
    return weather_list
    
def site_weather_csv_writer(path, weather_list):
    fieldnames = ["site", "temp_c", "wind_kmh"]
    sorted_weather_list = sorted(weather_list, key= lambda x: x["site"])

    try:
        with open(path, mode="w", newline="") as site_weather_csv:
            writer = csv.DictWriter(site_weather_csv, fieldnames=fieldnames)
            writer.writeheader()
    
            for weather in sorted_weather_list:
                writer.writerow(weather)
            
    except FileNotFoundError:
        print(f"Error: The directory path for '{path}' is invalid or could not be found")

    except (ValueError, TypeError) as e:
        print(f"Data structure error (check dictionary keys and row types): {e}")
    
    except OSError as e:
        print(f"Operating System Error: {e}")


def main():

    w_list = caller(sites_path, url)
    site_weather_csv_writer(csv_path, w_list)




if __name__ == "__main__":
    main()