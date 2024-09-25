import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

# Function to get weather data
def get_weather(city):
    api_key = '45583cb9ab81412adcd215e5965e2eda' # Replace with your OpenWeatherMap API key 
    base_url = 'http://api.openweathermap.org/data/2.5/weather?q=Hyderabad&appid=45583cb9ab81412adcd215e5965e2eda&units=metric'
    
    print(f"Request URL: {base_url}")  # Print tpiphe URL for debugging


    try:
        
        response = requests.get(base_url)
        print(f"Status Code: {response.status_code}")  # Check the status code
        print(response.text)  # Print the response body for error details

        data = response.json()
        print (data)
        if data["cod"] != "404":
            main = data['main']
            weather = data['weather'][0]
            wind = data['wind']

            city_info = {
                "city": data["name"],
                "temperature": main['temp'],
                "humidity": main['humidity'],
                "description": weather['description'],
                "icon": weather['icon'],
                "wind_speed": wind['speed']
            }
            return city_info
        else:
            messagebox.showerror("Error", "City not found!")
    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch data!")

# Function to display the weather
def display_weather():
    city = city_entry.get()
    if city:
        weather_data = get_weather(city)
        if weather_data:
            city_label.config(text=f"City: {weather_data['city']}")
            temp_label.config(text=f"Temperature: {weather_data['temperature']}°C")
            description_label.config(text=f"Weather: {weather_data['description'].capitalize()}")
            wind_label.config(text=f"Wind Speed: {weather_data['wind_speed']} m/s")
            humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")

            # Load weather icon from OpenWeatherMap
            icon_url = f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png"
            icon_data = requests.get(icon_url).content
            icon_image = Image.open(io.BytesIO(icon_data))
            icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo
    else:
        messagebox.showerror("Error", "Please enter a city name!")

# Create GUI
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
root.config(bg="lightblue")

# Create GUI elements
city_entry = tk.Entry(root, font=("Helvetica", 14), justify="center")
city_entry.pack(pady=10)

search_button = tk.Button(root, text="Search", font=("Helvetica", 12), command=display_weather)
search_button.pack(pady=5)

city_label = tk.Label(root, text="City: ", font=("Helvetica", 14), bg="lightblue")
city_label.pack(pady=5)

temp_label = tk.Label(root, text="Temperature: ", font=("Helvetica", 14), bg="lightblue")
temp_label.pack(pady=5)

description_label = tk.Label(root, text="Weather: ", font=("Helvetica", 14), bg="lightblue")
description_label.pack(pady=5)

wind_label = tk.Label(root, text="Wind Speed: ", font=("Helvetica", 14), bg="lightblue")
wind_label.pack(pady=5)

humidity_label = tk.Label(root, text="Humidity: ", font=("Helvetica", 14), bg="lightblue")
humidity_label.pack(pady=5)

icon_label = tk.Label(root, bg="lightblue")
icon_label.pack(pady=10)

# Start the Tkinter loop
root.mainloop()
