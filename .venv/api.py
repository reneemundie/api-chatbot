# This file contains the code for the API request from OpenWeather
# Import statements for modules required for API call
import os
import requests
from dotenv import load_dotenv

# Creating a dictionary of destinations with their name, latitude and longitude
destinations = [
    {"name" : "Lake District National Park", "lat" : "54.4609", "lon" : "-3.0886"},
    {"name" : "Corfe Castle", "lat" : "50.6395", "lon" : "-2.0566"},
    {"name" : "The Cotswolds", "lat" : "51.8330", "lon" : "-1.8433"},
    {"name" : "Cambridge", "lat" : "52.2053", "lon" : "0.1218"},
    {"name" : "Bristol", "lat" : "51.4545", "lon" : "-2.5879"},
    {"name" : "Oxford", "lat" : "51.7520", "lon" : "-1.2577"},
    {"name" : "Norwich", "lat" : "52.6309", "lon" : "-1.2974"},
    {"name" : "Stonehenge", "lat" : "51.1789", "lon" : "-1.8262"},
    {"name" : "Watergate Bay", "lat" : "50.4429", "lon" : "-5.0553"},
    {"name" : "Birmingham", "lat" : "52.4862", "lon" : "-1.8904"}
]

# Creating a list to store JSON weather data
weather_data = []

# Creating variable for exclusions in API call per OpenWeather URL format
part = 'minutely,hourly,daily,alert'

# Function to access API key stored separately for security
load_dotenv(dotenv_path="/Users/reneemundie/PythonProjects/api-chatbot/.venv/key.env")
api_key = os.getenv('API_KEY')

# Function to update API URL & make API request
def get_weather_data():
    for i in range(len(destinations)):
        lat = (destinations[i]["lat"])
        lon = (destinations[i]["lon"])
        api_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}"
        response = requests.get(f"{api_url}")             
        if response.status_code == 200:
            data = response.json()
            weather_data.append({"name": destinations[i]["name"], "weather": data})
        else:
            print(f"Failed to fetch weather data, {response.status_code} error with your request")
    return weather_data

def py_weather_data():
    py_list = []
    for i in range(len(weather_data)):
        py_dict = {}
        location = (weather_data[i]["name"])
        current_data = (weather_data[i]["weather"]["current"])
        weather = current_data["weather"][0]
        temp = current_data["temp"] - 273.15
        feels_like = current_data["feels_like"] - 273.15
        description = weather["description"]

        py_dict = {
            "Location": location,
            "Temperature": "{:.2f}°C".format(temp),
            "Feels Like": "{:.2f}°C".format(feels_like),
            "Description": description,
        }

        py_list.append(py_dict)

    return py_list