import math
from datetime import datetime

def calculate_day_length(latitude, longitude, date=None):
    """
    Laskee päivän pituuden tunteina annettuna päivämääränä ja koordinaateilla.

    Args:
        latitude (float): Leveysaste (esim. Vaasa: 63.105870).
        longitude (float): Pituusaste (ei vaikuta laskentaan, mutta mukana selkeyden vuoksi).
        date (datetime, optional): Päivämäärä. Oletus: nykyinen päivä.

    Returns:
        float: Päivän pituus tunteina.
    """
    if date is None:
        date = datetime.now()

    # Laske vuodenpäivä (1 = tammikuu 1, 365 = joulukuu 31)
    day_of_year = date.timetuple().tm_yday

    # Deklinaatio (auringon korkeus ekvaattorin yläpuolella)
    declination = -23.44 * math.cos(math.radians((360 / 365) * (day_of_year + 10)))

    # Päiväkaaren kulma (hour angle)
    latitude_rad = math.radians(latitude)
    declination_rad = math.radians(declination)
    
    cos_hour_angle = -math.tan(latitude_rad) * math.tan(declination_rad)

    # Tarkista, onko aurinko aina horisontin ylä- tai alapuolella
    if cos_hour_angle > 1:
        return 0.0  # Aurinko ei nouse
    elif cos_hour_angle < -1:
        return 24.0  # Aurinko ei laske

    # Päivän pituus tunteina
    hour_angle = math.degrees(math.acos(cos_hour_angle))
    day_length = (2 * hour_angle) / 15  # Muutetaan asteet tunneiksi

    return day_length

# Testataan funktiota Vaasan koordinaateilla
latitude = 63.105870
longitude = 21.596817
date = datetime(2025, 1, 12)  # Esimerkki päivämäärä

print(f"Päivän pituus: {calculate_day_length(latitude, longitude, date):.2f} tuntia")
