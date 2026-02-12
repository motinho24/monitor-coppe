import requests
import csv
import os
from datetime import datetime

API_URL = "https://api.brawlify.com/v1/club/80R90R0UL"

def get_trophies():
    response = requests.get(API_URL, timeout=30)
    data = response.json()

    # Qui prendiamo direttamente il valore corretto
    return data.get("trophies")

def save_data(current):
    file_exists = os.path.isfile("storico_coppe.csv")
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    last_value = None
    if file_exists:
        with open("storico_coppe.csv", "r") as f:
            rows = list(csv.reader(f))
            if len(rows) > 1:
                last_value = int(rows[-1][1])

    variation = 0
    if last_value is not None:
        variation = current - last_value

    with open("storico_coppe.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp_UTC", "Coppe", "Variazione"])
        writer.writerow([now, current, variation])

    print(f"Ora: {now} | Coppe: {current} | Variazione: {variation}")

def main():
    trophies = get_trophies()

    if trophies is not None:
        save_data(trophies)
    else:
        print("Errore: dati non ricevuti")

if __name__ == "__main__":
    main()




