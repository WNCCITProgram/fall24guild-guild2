"""
    Name: writer_package.py
    Author: Guild Two
    Created: 19 October 2024
    Purpose: Python program to utilize WriterPackage class from 
    writer_module.py for main functionality.
"""

""" writer_package.py will contain the FuelManagementApp class to handle 
GUI and user interaction.  And will utilize WriterPackage class to 
manage customer data."""

""" Use both writer_module.py and writer_package.py in the same
directory in order to run. """

# Imports for writer package
# Import tkinter for GUI interface
# Import messagebox from tkinter for alerts
# Import requests for making API calls
# Import WriterPackage and Customer classes from the writer_module
import tkinter as tk 
from tkinter import messagebox 
import requests 
from writer_module import WriterPackage, Customer  

# TODO: Create main class (FuelManagementApp) to create the GUI and handle any user interactions
class FuelManagementApp:
    # Initialize FeulManagementApp object
    # Create instance of WriterPackage class that will handle
    # data management for customers and fuel tanks.
    # Create the start of the main GUI loop
    def __init__(self):
        self.writer = WriterPackage()  
        self.main()  

    # TODO: Main function to create the GUI using tkinter
    """ Example GUI for user interaction that allows user to add a customer and check the fuel status of their tanks. """
    def main(self):
        self.root = tk.Tk()  # Create main window
        self.root.title("Customer Fuel Management System")  # Set window title
        
        # Input field for the customer's name
        tk.Label(self.root, text="Customer Name").grid(row=0)
        self.customer_name = tk.Entry(self.root)  # Entry widget for customer name
        self.customer_name.grid(row=0, column=1)  # Place entry in grid

        """ Any additional input fields that we want to use can be added here..."""

        # Create button to add customer
        tk.Button(self.root, text="Add Customer", command=self.add_customer).grid(row=1, column=0, sticky=tk.W)
        # Create button to check fuel status
        tk.Button(self.root, text="Check Fuel Status", command=self.check_fuel_status).grid(row=2, column=0, sticky=tk.W)

        self.root.mainloop()  # Start the GUI event loop

    # TODO: Create method to check the fuel status of tanks
    # Calls fetch_feul_data to retrieve fuel data (or API call)
    # Calls find_lowest_ten_fuel_tanks to figure out which fuel tanks are the lowest
    # Calls display_lowest_fuel_tanks to display result to user through messagebox
    def check_fuel_status(self):
        fuel_data = self.fetch_fuel_data()  # Fetch fuel data
        """ This is a placeholder for an API call function we can create. """
        lowest_tanks = self.find_lowest_ten_fuel_tanks(fuel_data)  # Find tanks with the lowest levels of fuel
        self.display_lowest_fuel_tanks(lowest_tanks)  # Display results of the tanks

    # TODO: Create method to fetch fuel data (placeholder for actual API call)
    def fetch_fuel_data(self):
        # Uncomment and use actual API call
        # response = requests.get("API_URL")
        # return response.json()

        # Here's a simulated response for demonstration purposes of what an API call could return
        # Returns a dictionary of tank ID numbers and their corresponding fuel levels.
        return {
            "tank1": 30,
            "tank2": 20,
            "tank3": 50,
            "tank4": 15,
            "tank5": 90,
            "tank6": 5,
            "tank7": 70,
            "tank8": 10,
            "tank9": 80,
            "tank10": 40,
            "tank11": 25,
        }

    # TODO: Create method to find the ten lowest fuel tanks 
    # This will sort the fuel data by the tank's fuel levels and
    # then return the ten tanks with the lowest levels
    def find_lowest_ten_fuel_tanks(self, fuel_data):
        sorted_tanks = sorted(fuel_data.items(), key=lambda x: x[1])  # Sort tanks by fuel level
        return sorted_tanks[:10]  # Return lowest ten tanks

    # TODO: Create method to display the lowest fuel tanks to the user
    # Use messagebox to display info to user
    # messagebox.showinfo()
    def display_lowest_fuel_tanks(self, lowest_tanks):
        for tank in lowest_tanks:
            messagebox.showinfo("Low Fuel Tank", f"Tank ID: {tank[0]}, Fuel Level: {tank[1]}%") 

    # TODO: Create method to add a new customer
    # Get customer information from input fields
    # Creates new customer object with input data
    # Calls save_customer_to_db to save customer data to the database
    # Displays a message to the user to show if an error occurred or
    # if save was successful.
    def add_customer(self):
        name = self.customer_name.get()  # Get the customer name from the input field
        """ Any additional necessary data such as address, phone, etc. can be added here. """
        
        new_customer = Customer(name, "Sample Address", "1234567890", "email@example.com", 1000)  # Create new customer object
        # Try-except block to handle error for saving a new customer
        try:
            self.writer.save_customer_to_db(new_customer)  # Save the new customer to the database
            messagebox.showinfo("Success", "Customer added successfully!")  # Message to display if save was a success 
        except Exception as e:
            messagebox.showerror("Database Error", str(e))  # Message to display if save was an error 

# Entry point for the program
# if __name__ == "__main__"
if __name__ == "__main__":
    FuelManagementApp()  # Create and run FuelManagementApp
