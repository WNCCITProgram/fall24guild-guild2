"""
    Name: weather.py
    Authors: Guild Two (consolidated)
    Created: 03 November 2024
    Purpose: Gather information for weather to be implemented into main program
"""

# import the module
# pip install python-weather
import python_weather

import asyncio
import os

async def getweather() -> None:
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    # fetch a weather forecast from a city
    weather = await client.get('Scottsbluff')
    
    # returns the current day's forecast temperature (int)
    print(f"{weather.temperature} degrees")
    

if __name__ == '__main__':
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())