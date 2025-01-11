import requests
from datetime import datetime

def fetch_weather(city="Vaasa", api_key="1841b4f0e921b501ec47c278a535991f", times=["06:00:00", "12:00:00", "18:00:00"]):
    """
    Hakee sääennusteen OpenWeather API:lta annetulle kaupungille ja kellonajoille.

    Args:
        city (str): Kaupungin nimi. Oletus "Vaasa".
        api_key (str): OpenWeather API -avain.
        times (list): Lista haettavista kellonajoista, esim. ["06:00:00", "12:00:00", "18:00:00"].

    Returns:
        list: Lista tupleja, joissa viikonpäivä, päivämäärä ja lämpötilat haetuilta ajoilta.
    """
    BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

    try:
        response = requests.get(BASE_URL, params={"q": city, "appid": api_key, "units": "metric"})
        response.raise_for_status()
        data = response.json()

        # Haetaan lämpötilat annettujen kellonaikojen perusteella
        weather_data = []
        daily_temps = {}

        for entry in data["list"]:
            dt = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
            time = entry["dt_txt"].split()[1]

            if time in times:
                date = dt.strftime("%d.%m.%Y")
                weekday = dt.strftime("%a")

                if date not in daily_temps:
                    daily_temps[date] = {"weekday": weekday, "temps": {time: entry["main"]["temp"]}}
                else:
                    daily_temps[date]["temps"][time] = entry["main"]["temp"]

        # Muodostetaan lopullinen lista
        for date, info in daily_temps.items():
            temps = [info["temps"].get(time, "Ei tietoa") for time in times]
            weather_data.append((info["weekday"], date, *temps))

        if not weather_data:
            print(f"Virhe: Ei löydetty ennustetietoja kaupungille {city} annetuilla ajoilla.")

        return weather_data
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return []
