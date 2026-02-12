import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

URL = "https://brawlify.com/club/80R90R0UL"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_trophies():
    response = requests.get(URL, headers=HEADERS, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    # Cerca il <p> con classe corretta
    trophy_tag = soup.find("p", class_="text-brawl-gold font-bold")

    if trophy_tag:
        trophies = trophy_tag.text.strip().replace(",", "")
        return int(trophies)

    return None

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
        print("Errore: coppe non trovate")

if __name__ == "__main__":
    main()


