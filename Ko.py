import tkinter as tk
from APIkutsu import fetch_weather
from paivan_pituus import calculate_day_length
from datetime import datetime
from PIL import Image, ImageTk
from Asetukset import DATA_FONT, HEADER_FONT, TITLE_FONT, SHADOW_OFFSET, COLUMN_STARTS, ROW_START, ROW_SPACING, UI_WIDTH, UI_HEIGHT, LINE_COLOR, LINE_WIDTH, BACKGROUND_IMAGE

def create_ui():
    # Luodaan pääikkuna
    root = tk.Tk()
    root.title("Sääennuste Vaasa")
    root.geometry(f"{UI_WIDTH}x{UI_HEIGHT}")

    # Lataa taustakuva
    background_image = Image.open(BACKGROUND_IMAGE)
    background_photo = ImageTk.PhotoImage(background_image)

    # Aseta taustakuva Canvasille
    canvas = tk.Canvas(root, width=UI_WIDTH, height=UI_HEIGHT, highlightthickness=0)
    canvas.place(relwidth=1, relheight=1)
    canvas.image = background_photo  # Pitää viittauksen taustakuvaan hengissä
    canvas.create_image(0, 0, anchor="nw", image=background_photo)

    # Varjotekstin luontifunktio
    def create_shadowed_text(canvas, text, font, x, y):
        # Varjo
        canvas.create_text(x + SHADOW_OFFSET, y + SHADOW_OFFSET, text=text, font=font, fill="black", anchor="nw")
        # Valkoinen pääteksti
        canvas.create_text(x, y, text=text, font=font, fill="white", anchor="nw")

    # Erottavan viivan luontifunktio
    def create_separator(canvas, x1, y1, x2, y2):
        canvas.create_line(x1, y1, x2, y2, fill=LINE_COLOR, width=LINE_WIDTH)

    # Otsikko
    create_shadowed_text(canvas, "VAASAN SÄÄ", TITLE_FONT, 300, 10)

    # Hae säädata Vaasasta
    weather_data = fetch_weather()

    # Otsikot sarakkeille
    headers = ["Viikonpäivä", "Päivämäärä", "klo 6.00", "klo 12.00", "klo 18.00", "Päivän pituus"]
    for header in headers:
        create_shadowed_text(canvas, header, HEADER_FONT, COLUMN_STARTS[header], 50)

    # Erottavat viivat otsikon ja datan väliin
    create_separator(canvas, 10, 80, UI_WIDTH - 10, 80)

    # Täytetään käyttöliittymä datalla
    y_position = ROW_START
    for row, data in enumerate(weather_data):
        weekday, date, temp_6, temp_12, temp_18 = data

        # Laske päivän pituus
        date_obj = datetime.strptime(date, "%d.%m.%Y")
        day_length = calculate_day_length(63.105870, 21.596817, date_obj)

        # Muutetaan tunteja ja minuutteja varten
        hours = int(day_length)
        minutes = int((day_length - hours) * 60)
        day_length_str = f"{hours} h {minutes} min"

        # Näytetään tiedot varjotekstinä
        data_texts = [weekday, date, f"{temp_6}°C", f"{temp_12}°C", f"{temp_18}°C", day_length_str]
        for i, text in enumerate(data_texts):
            create_shadowed_text(canvas, text, DATA_FONT, COLUMN_STARTS[headers[i]], y_position)

        # Erottava viiva rivin jälkeen
        create_separator(canvas, 10, y_position + 25, UI_WIDTH - 10, y_position + 25)

        y_position += ROW_SPACING

    # Erottavat viivat sarakkeiden väliin
    for start in COLUMN_STARTS.values():
        create_separator(canvas, start - 10, 80, start - 10, y_position - ROW_SPACING + 15)

    # Käynnistetään pääsilmukka
    root.mainloop()

if __name__ == "__main__":
    create_ui()
