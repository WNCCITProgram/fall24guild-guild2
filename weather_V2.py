"""
    Name: weather_V2.py
    Authors: Guild Two (consolidated)
    Created: 03 November 2024
    Revised: 10 Nomember 2024
    Purpose: Gather information for weather to be implemented into main program.
"""
""" weather_V2 created as an alternative method to better integrate asyncio
(asynchronous) within the GUI, which uses tkinter that uses a synchronous loop"""

# Import asyncio module for asynchronous programming
# Import python weather to fetch weather data
# pip install python-weather
# Import tkinter to build GUI
import asyncio
import python_weather
import tkinter as tk

class WeatherApp:
    def __init__(self, root):
        # Initialize object with constructor method
        # Set title window
        # Create label widget for weather info
        self.root = root
        self.root.title("Weather Info")
        self.weather_label = tk.Label(root, text="Weather Info will appear here")
        self.weather_label.pack(pady=10)

        # Add a button to fetch weather data
        self.get_weather_button = tk.Button(root, text="Get Weather", command=self.get_weather)
        self.get_weather_button.pack(pady=10)

    async def fetch_weather(self):
        """ This is an asynchronous method to fetch weather data and uses
        the python_weather API."""
        # Create asynchronous context manager that handles weather client connection
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            weather = await client.get('Scottsbluff')  # Example city that can be replaced
            return weather.temperature

    def get_weather(self):
        """Method to fetch weather and update the label asynchronously.
        Triggered by user when they click the 'Get weather' button."""
        # Asynchronous function definition that updates the weather label
        # after the data is fetched
        async def update_weather():
            temp = await self.fetch_weather()
            self.weather_label.config(text=f"Temperature: {temp}°F")
        # Asynchronous task that runs update_weather function
        asyncio.create_task(update_weather())

if __name__ == "__main__":
    root = tk.Tk()          # Create main tkinter window
    app = WeatherApp(root)  # Instantiate WeatherApp class
    root.mainloop()         # Start tkinter event loop
