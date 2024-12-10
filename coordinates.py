"""
    Name: coordinates.py
    Authors: Guild Two
    Created: 28 November 2024
    Purpose: Python module that uses geopy library to give gps
    lat/long coordinates for a given street address location.
"""
# gps_coordinates.py
from geopy.geocoders import Nominatim

# Create a geolocator instance with a user-defined agent name
geolocator = Nominatim(user_agent="Fuel Management System")

def get_coordinates(location_name):
    """
    Accepts a location name as input and returns its coordinates (latitude, longitude).
    """
    try:
        # Get the location details based on the location's name
        location = geolocator.geocode(location_name)
        
        if location:
            # Return the latitude and longitude as a tuple
            return location.latitude, location.longitude
        else:
            print(f"Location '{location_name}' not found.")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
