import requests
from util import to_celcius, to_fahrenheit


class WeatherAPIHandler(object):
    def __init__(self, api_key):
        self.api_key = api_key

    # Get the coordinates for a city using the OpenWeatherMap Geocoding API
    def get_coordinates(self, city):
        url = "http://api.openweathermap.org/geo/1.0/direct?q={}&appid={}"
        response = requests.get(url.format(city, self.api_key))

        # if the response is not OK or the response is empty, return None
        if response.status_code != 200 or len(response.json()) == 0:
            return None

        # get the first result and return its lat and lon
        data = response.json()[0]
        if data['lat'] and data['lon']:
            return data['lat'], data['lon']
        else:
            return None

    # Get the forecast for the given coordinates using the OpenWeatherMap Forecast API
    def get_forecast(self, coordinates):
        lat, lon = coordinates
        url = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"
        response = requests.get(url.format(lat, lon, self.api_key))

        # if the response is not OK or the response is empty, return None
        if response.status_code != 200 or len(response.json()) == 0:
            return None

        data = response.json()

        # create a list of forecast objects and return it
        result = []
        for entry in data['list']:
            forecast = self.extract_entry(entry)
            result.append(forecast)
        return result

    # Extract the forecast data from the entry.
    # This is a helper function for get_forecast that only extracts
    # the data we need from the entry
    def extract_entry(self, entry):
        return {
            'date': entry['dt_txt'].split(' ')[0],
            'time': entry['dt_txt'].split(' ')[1],
            'temp-c': to_celcius(entry['main']['temp']),
            'temp-f': to_fahrenheit(entry['main']['feels_like']),
            'description': entry['weather'][0]['description']
        }

    # Get the forecast for a city
    def get_forecast_by_city(self, city):
        coordinates = self.get_coordinates(city)
        if coordinates is None:
            return None
        return self.get_forecast(coordinates)

    # Aggregate the forecast data into a list of objects
    def aggregate_forecast(self, forecast):
        if forecast is None:
            return None

        # create a dictionary of dates and their corresponding forecasts
        dailyForcast = {}
        prevDate = None
        entries = 0

        for entry in forecast:
            date = entry['date']
            if date not in dailyForcast:
                # add to the dictionary
                dailyForcast[date] = {
                    'avg-temp-c': 0,
                    'avg-temp-f': 0,
                }
                # if the previous date has entries, calculate its average
                if entries > 0:
                    dailyForcast[prevDate]['avg-temp-c'] /= entries
                    dailyForcast[prevDate]['avg-temp-f'] /= entries
                    entries = 0
                # finally, update prevDate
                prevDate = date

            # update the average temperature and increment the number of entries
            dailyForcast[date]['avg-temp-c'] += entry['temp-c']
            dailyForcast[date]['avg-temp-f'] += entry['temp-f']
            entries += 1

        # now calculate the average for the last date
        dailyForcast[prevDate]['avg-temp-c'] /= entries
        dailyForcast[prevDate]['avg-temp-f'] /= entries
        return dailyForcast
