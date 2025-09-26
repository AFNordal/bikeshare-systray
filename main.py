import time
import requests
import pystray
from datetime import datetime
from PIL import Image
from config import station_names, client_id, endpoint


def get_available_bikes(station_id: int) -> int:
    url = f"{endpoint}/station_status.json"
    headers = {"Client-Identifier": client_id}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    for station in data["data"]["stations"]:
        if int(station["station_id"]) == station_id:
            return station["num_bikes_available"]
    
    return -1

def get_station_id(station_name: str) -> int:
    url = f"{endpoint}/station_information.json"
    headers = {"Client-Identifier": client_id}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    for station in data["data"]["stations"]:
        if station["name"] == station_name:
            return int(station["station_id"])
    
    raise ValueError(f"Station '{station_name}' not found")


def launch_icon():
    icon = pystray.Icon("Bysykkel")
    icon.icon = Image.open("logo.png")

    # Wait until endpoint is available
    print("Attempting to connect to endpoint...")
    for _ in range(24):
        try:
            requests.get(f"{endpoint}/system_information.json", 
                         headers={"Client-Identifier": client_id}, timeout=5)
            break
        except requests.exceptions.Timeout:
            print("Endpoint unavailable, retrying.")
        except requests.exceptions.ConnectionError:
            print("Connection error, retrying.")
            time.sleep(5)
    else:
        raise RuntimeError("Could not connect to endpoint")    

    # Pre-fetch station IDs
    stations = [(name, get_station_id(name)) for name in station_names]
    print("Fetched station IDs:", stations)

    def stop(icon, item):
        print("Stopping...")
        icon.stop()
    
    def refresh(icon, item=None):
        print("Fetching available bikes...")
        bike_counts = {}
        for name, id in stations:
            bike_count = get_available_bikes(id)
            bike_counts[name] = bike_count if bike_count != -1 else "error"
            print(f"{name}: {bike_counts[name]}")

        menu_items = [pystray.MenuItem(f"{station}: {count}", None) for station, count in bike_counts.items()]
        icon.menu = pystray.Menu(
            pystray.MenuItem("Refresh", refresh),
            *menu_items,
            pystray.MenuItem("Quit", stop)
        )
        title = datetime.now().strftime("%H:%M:%S\n") + \
                "\n".join([f"{station}: {count}" for station, count in bike_counts.items()])
        icon.title = title
        icon.update_menu()
        print("Icon updated.")
    
    icon.menu = pystray.Menu(
        pystray.MenuItem("Refresh", refresh),
        pystray.MenuItem("Quit", stop)
    )
    print("Launching...")
    refresh(icon)
    icon.run()

if __name__ == "__main__":
    launch_icon()