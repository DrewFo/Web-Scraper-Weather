import requests
from bs4 import BeautifulSoup

def get_coord_request_url(long, lat):
    coord_request = f"https://forecast.weather.gov/MapClick.php?lon={long}&lat={lat}"
    return coord_request

def cur_conditions(soup : BeautifulSoup):
    conds = soup.find(id="current-conditions")
    
    return conds.prettify()

def extended_forecast(soup : BeautifulSoup):
    pass

def main():
    res = requests.get(get_coord_request_url(-94.82, 41.58))
    soup = BeautifulSoup(res.text, 'html.parser')

    print("")
    print(cur_conditions(soup))
    print(res.status_code)

main()