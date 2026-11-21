import pytest
from weather import transform
import copy

parsed_data = {
  "latitude": 40.703716,
  "longitude": -73.880554,
  "generationtime_ms": 0.036,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 18.0,
  "current_units": {
    "time": "iso8601",
    "interval": "900",
    "temperature_2m": "°C",
    "wind_speed_10m": "km/h"
  },
  "current": {
    "time": "2026-11-21T21:15",
    "interval": 900,
    "temperature_2m": 8.4,
    "wind_speed_10m": 14.2
  }
}

site = {"name": "Queens, New York", "lat":parsed_data["latitude"], "lon":parsed_data["longitude"]}

def test_weather_transform_normal():
    assert transform(parsed_data, site) == {"site": site["name"],
                                            "temp_c": 8.4,
                                            "wind_kmh": 14.2}

def test_weather_transform_missing_current():
    parsed_data_no_current = copy.deepcopy(parsed_data)
    parsed_data_no_current.pop("current")
    site_copy = site.copy()
    
    with pytest.raises(KeyError):
        transform(parsed_data_no_current, site_copy)

def test_weather_transform_missing_o_key():
    parsed_data_no_o_key = copy.deepcopy(parsed_data)
    parsed_data_no_o_key["current"].pop("temperature_2m")
    site_copy_2 = {"name": "Queens, New York", "lat":parsed_data["latitude"], "lon":parsed_data["longitude"]}

    with pytest.raises(KeyError):   
        transform(parsed_data_no_o_key, site_copy_2)