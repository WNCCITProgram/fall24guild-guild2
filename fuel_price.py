"""
    Name: fuel_price.py
    Authors: Guild Two 
    Created: 17 November 2024
    Purpose: Python API fuel price module called by main gui program
    that will display the monthly prices for natural gas products.
"""

import requests
import json

# Define the API URL
API_URL = "https://api.eia.gov/v2/natural-gas/pri/sum/data/"

# Define the parameters for the request 
# Parameters should be passed as URL params, NOT in the headers
# API KEY is added here reduntantly in parameters, 
# because some API's may allow the API Key to pass 
# only as a parameter query
params = {
    "api_key": "R0tfPSctUPmq6wHsdIlK92EaifGDSIO9THIb377l",
    "frequency": "monthly",
    "data": ["value"],
    "facets": {
        "product": ["EPG0"]
    },
    "start": "2024-07",
    "end": "2024-08",
    "offset": 0,
    "length": 5000
}

# Replace this with your actual API key
# Register for free account and copy/paste API KEY from 
# email you provided
API_KEY = "R0tfPSctUPmq6wHsdIlK92EaifGDSIO9THIb377l"

# Create method to fetch the price of fuel
def fetch_fuel_price():
    """
    Fetches monthly fuel price of natural gas data from the EIA API.

    Returns:
        list: A list of monthly fuel prices for the given start to end parameter.
        None: If there was an error or no data found.
    """
    try:
        # Add the API key to the request headers
        # Authorization Bearer token authentication (API KEY)
        headers = {
            "Authorization": f"Bearer {API_KEY}",  
        }
        
        # Send GET request to the EIA API with the parameters passed in the params argument
        response = requests.get(API_URL, params=params, headers=headers)

        # Check if the request was successful 
        # Status code 200 = success
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Print the raw response for debugging purposes
            # Use this to help us inspect the structure of the response
            print(json.dumps(data, indent=4))  

            # Extract the relevant part of the response we want; prices
            # if-else to handle error if data is not found
            if "data" in data and len(data["data"]) > 0:
                prices = [item["value"] for item in data["data"]] 
                return prices
            else:
                print("Error: No price data found in the response.")
                return None
        else:
            print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: An error occurred while fetching data - {e}")
        return None
