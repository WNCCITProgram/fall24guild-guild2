"""
    Name: api_module.py
    Author: Guild Two
    Created: 02 November 2024
    Purpose: API module example for main program use.  
    API shows weekly oil and propane prices. 
"""


# Import requests library to handle HTTP requests
import requests  

# TODO: Create EIA API class
# EIA is the US Energy Information Administration

class EIA_API:
    # URL for the EIA API
    BASE_URL = "https://api.eia.gov/v2/petroleum/pri/wfr/data/"
    
    @staticmethod
    #TODO: Create method to fetch fuel data from EIA API
    # This method will construct needed parameters for an API call.
    # GET request to API and process response.
    # Returns a dictionary with the fuel data if the request was a success.
    # If request fails, raise Exception
    def fetch_fuel_data():    
        # Define the headers for the API request
        # Copy header from EIA API
        headers = {
            "X-Params": {
                "frequency": "weekly",  # Frequency of data retrieval
                "data": ["value"],  # Data to retrieve (fuel value)
                "facets": {
                    "product": ["EPLLPA"]  # Specific product to query (petroleum)
                },
                "start": None,  # Start date (Can modify for specific inquery)
                "end": "2024-10-21",  # End date for the data
                "sort": [
                    {
                        "column": "period",  # Column to sort by
                        "direction": "desc"  # Sort in descending order
                    }
                ],
                "offset": 0,  # Offset for pagination
                "length": 5000  # Maximum number of records to return
            }
        }
        
        # Make GET request to API
        # response = requests.get()
        response = requests.get(EIA_API.BASE_URL, params=headers)
        
        # Check if request was a success
        # Return JSON response as dictionary
        # return response.json()
        if response.status_code == 200:
            return response.json() 
        else:
            # Raise exception if request did not succeed
            raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

# Example usage: Uncomment the lines below to test the API
# if __name__ == "__main__":
#     try:
#         data = EIA_API.fetch_fuel_data()  # Call the method to fetch data
#         print(data)  # Print the fetched data
#     except Exception as e:
#         print(e)  # Print any errors encountered during the API call
