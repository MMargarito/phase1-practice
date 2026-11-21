import httpx
import copy

url = "https://api.open-meteo.com/v1/forecast"
params = {"latitude": 40.70,
          "longitude": 13.41,
          "current": ["temperature_2m", "wind_speed_10m"]}



def fetch(url, params):
    response = httpx.get(url, params=params, timeout=10) 
    response.raise_for_status()
    data = response.json()
    return data


def transform(data, site):
    return {"site": site["name"],
            "temp_c": data["current"]["temperature_2m"],
            "wind_kmh": data["current"]["wind_speed_10m"]}

def main():
    data = fetch(url, params)
    site = {"name": "Queens, New York", "lat":data["latitude"], "lon":data["longitude"]}
    weather_dict = transform(data, site)
    print(weather_dict)


if __name__ == "__main__":
    main()