"""
    Name: fuel_price.py
    Authors: Guild Two 
    Created: 17 November 2024
    Purpose: Python API fuel price module called by main gui program
    that will display the monthly prices for natural gas products.
"""

import requests
import json
from datetime import datetime, timedelta

# Define the API URL
API_URL = "https://api.eia.gov/v2/petroleum/pri/wfr/data/"

# constants
MARKUP = 0.50  # 50 cents markup
MIDWEST_SERIES = "W_EPLLPA_PRS_R40_DPG"  # Midwest residential propane


# Replace this with your actual API key
# Register for free account and copy/paste API KEY from 
# email you provided
API_KEY = "R0tfPSctUPmq6wHsdIlK92EaifGDSIO9THIb377l"

# Create method to fetch the price of fuel
def fetch_fuel_price():
    # Calculate date range for last month
    today = datetime.now()
    end_date = today.strftime("%Y-%m")
    start_date = (today - timedelta(days=30)).strftime("%Y-%m")
    
    """
    Fetches Midwest padd region propane per gallon price and calcs markup

    Returns:
        list: A list of monthly fuel prices for the given start to end parameter.
        None: If there was an error or no data found.
    """
    # Define the parameters for the request 
    # Parameters should be passed as URL params, NOT in the headers
    # API KEY is added here reduntantly in parameters, 
    # because some API's may allow the API Key to pass 
    # only as a parameter query
    params = {
        "api_key": "R0tfPSctUPmq6wHsdIlK92EaifGDSIO9THIb377l", # this is redundant but necessary?
        "frequency": "weekly",
        "data[0]": "value",   # corrected
        "facets[series][]": MIDWEST_SERIES,
        # "start": "2024-07",
        # "end": "2024-08",   # these may need to be adjusted or turned dynamic
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",  # Most recent first
        "start": start_date,
        "end": end_date,
        # "offset": 0,
        # "length": 5000     # might not need 5,000 data point returns
        "length": 4
    }
    
    # currently returning just the gallon price mark
    # maybe a sparkline display of historical prices later?
   
   
    
    try:
        # Add the API key to the request headers
        # Authorization Bearer token authentication (API KEY)
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "X-Api-Key": API_KEY,  # Add additional auth header, correct api call?
            "Content-Type": "application/json"  
        }
        
        # Debug print (remove in production)
        print(f"Requesting URL: {API_URL}")
        print(f"With params: {params}")
        
        # Send GET request to the EIA API with the parameters passed in the params argument
        response = requests.get(API_URL, params=params, headers=headers)
        
        # Debug print (remove in production)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

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
            if "response" in data and "data" in data["response"] and len(data["response"]["data"]) > 0:
                latest_data = data["response"]["data"][0]
                base_price = float(latest_data["value"])
                customer_price = base_price + MARKUP
                
                return {
                    'success': True,
                    'base_price': base_price,
                    'customer_price': customer_price
                }
            else:
                return {'success': False, 'error': "No price data found"}
        else:
           return {'success': False, 'error': f"API error: {response.status_code}"}
       
    except requests.exceptions.RequestException as e:
        print(f"Error: An error occurred while fetching data - {e}")
        return None
