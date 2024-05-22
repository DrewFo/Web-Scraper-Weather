import requests
from bs4 import BeautifulSoup
from colorama import init as colorama_init
from colorama import Fore, Style

colorama_init()

class WeatherConditions():
    basic_data = {}
    detailed_data = {}
    hazards = set()

    def initialize_data(self):
        self.basic_data = {}
        self.detailed_data = {}
        self.hazards = set()
    
    def update_weather(self, long, lat) -> bool:
        self.initialize_data()

        coord_request = f"https://forecast.weather.gov/MapClick.php?lon={long}&lat={lat}"
        res = requests.get(coord_request)
        if(res.status_code != 200):
            print("Error in coordinates or data!")
            return False
        else:
            soup = BeautifulSoup(res.text, "html.parser")
            self.set_basic_conds(soup)
            self.set_detailed_conds(soup)
            self.set_hazards(soup)
        return True

    def set_basic_conds(self, soup : BeautifulSoup):
        conds = soup.find(id="current-conditions")
        self.basic_data["Conditions"] = f"{conds.find(class_='myforecast-current').text}"
        self.basic_data["Temperature"] = f"{conds.find(class_='myforecast-current-lrg').text} ({conds.find(class_='myforecast-current-sm').text})"

    def set_detailed_conds(self, soup : BeautifulSoup):
        if soup.find("b", string="Humidity"):
            self.detailed_data["Humidity"] = soup.find("b", string="Humidity").find_parent("td").find_next_sibling("td").text.strip()
        if soup.find("b", string="Wind Speed"):
            self.detailed_data["Wind Speed"] = soup.find("b", string="Wind Speed").find_parent("td").find_next_sibling("td").text.strip()
        if soup.find("b", string="Barometer"):
            self.detailed_data["Barometer"] = soup.find("b", string="Barometer").find_parent("td").find_next_sibling("td").text.strip()
        if soup.find("b", string="Dewpoint"):
            self.detailed_data["Dewpoint"] = soup.find("b", string="Dewpoint").find_parent("td").find_next_sibling("td").text.strip()
        if soup.find("b", string="Visibility"):    
            self.detailed_data["Visibility"] = soup.find("b", string="Visibility").find_parent("td").find_next_sibling("td").text.strip()
        if soup.find("b", string="Heat Index"):
            self.detailed_data["Heat Index"] = soup.find("b", string="Heat Index").find_parent("td").find_next_sibling("td").text.strip()
        if soup.find("b", string="Last Updated"):
            self.detailed_data["Last Updated"] = soup.find("b", string="Last update").find_parent("td").find_next_sibling("td").text.strip()

    def set_hazards(self, soup : BeautifulSoup):
        hazard_list = soup.findAll(class_="anchor-hazards")
        if hazard_list is None:
            return
        
        for hazard in hazard_list:
            if hazard is not None:
                hazard_link = hazard.get("href")
                hazard_link = hazard_link.replace(" ", "%20")
                self.hazards.add(f"{hazard.text} \nMore Information: {Fore.BLUE}https://forecast.weather.gov/{hazard_link}")

    def toFormattedString(self) -> str:
        result = ""

        for key in self.basic_data.keys():
            result = result + f"{Fore.LIGHTGREEN_EX}{key}: {self.basic_data[key]}{Style.RESET_ALL}\n"
        result = result + "\n"
        for key in self.detailed_data.keys():
            result = result + f"{Fore.LIGHTBLUE_EX}{key}: {self.detailed_data[key]}{Style.RESET_ALL}\n"
        result = result + "\n"
        for hazard in self.hazards:
            result = result + f"{Fore.YELLOW}WARNING: {hazard}{Style.RESET_ALL}\n\n"
    
        return result

def main():
    print("Enter a coordinate in the United states.")
    latitude = input("Enter latitude (for South, use negative latitude): ")
    longitude = input("Enter longitude (for West, use negative longitude): ")

    colorama_init()
    weather = WeatherConditions()
    if(weather.update_weather(lat=latitude, long=longitude)):
        print(weather.toFormattedString())

main()