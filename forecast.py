from util import celc_str, fahr_str
from weather_api import WeatherAPIHandler

api_key = "e5e54ec7007bd3befa4dc68d230f7456"


def print_forecast(forecast):
    print("Forecast:")
    for entry in forecast:
        print(
            entry['date'],
            entry['time'],
            celc_str(entry['temp-c']),
            fahr_str(entry['temp-f']),
            entry['description'],
            sep='\t'
        )
    print()


def print_aggregate_forecast(aggregate_forecast):
    print("Daily Averages:")
    for date, entry in aggregate_forecast.items():
        print(
            date,
            celc_str(entry['avg-temp-c']),
            fahr_str(entry['avg-temp-f']),
            sep='\t'
        )


def main():
    # Create a WeatherAPIHandler object with the api_key
    weather_api = WeatherAPIHandler(api_key)

    # Prompt user
    city = input("Enter a city: ")
    city = city.strip().title()

    # Get the forecast for the city
    forecast = weather_api.get_forecast_by_city(city)
    aggregate_forecast = weather_api.aggregate_forecast(forecast)

    # Print the granular forecast
    print_forecast(forecast)

    # Print the aggregated forecast
    print_aggregate_forecast(aggregate_forecast)


if __name__ == "__main__":
    main()
