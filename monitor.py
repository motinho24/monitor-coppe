import requests
import re
import csv
import os
from datetime import datetime

URL = "https://brawlify.com/club/80R90R0UL"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_trophies():
    response = requests.get(URL, headers=HEADERS)
    html = response.text
    
    # Cerca numero grande tipo 1,692,388
    match = re.search(r'\d{1,3}(?:,\d{3})+', html)
    
    if match:
        return int(match.group().replace(",", ""))
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
    if last_value:
        variation = current - last_value
    
    with open("storico_coppe.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp_UTC", "Coppe", "Variazione"])
        writer.writerow([now, current, variation])

def main():
    trophies = get_trophies()
    if trophies:
        save_data(trophies)

if __name__ == "__main__":
    main()
