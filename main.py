"""
    Name: main.py
    Author: Guild Two
    Created: 27 October 2024
    Purpose: Demo of the main application that will utilize
    the FuelManagementAppGUI from gui.py
"""

""" Main program application to demonstrate the utilization of the proposed
    GUI framework.  Commit to week 10 branch."""

# Import tkinter
# Import messagebox from tkinter
# Import GUI class
# Import data handling from writer_module
import tkinter as tk
from tkinter import messagebox
from gui import FuelManagementAppGUI  
from writer_module import WriterPackage, Customer  

# TODO: Initialize main application to set up the writer and GUI
# Create an instance of the writer package (WriterPackage) to handle data
# Initialize tkinter window
# Create GUI with the callback functions to add a customer and check fuel status
# Start the tkinter main loop
class FuelManagementApp:
    def __init__(self):
        self.writer = WriterPackage()  
        self.root = tk.Tk()  
        self.gui = FuelManagementAppGUI(self.root, self.add_customer, self.check_fuel_status)
        self.root.mainloop()  

    # TODO: Create method to fetch fuel data and display tanks with lowest fuel levels
    # Fetch fuel data from API
    # Get lowest ten fuel tanks
    # Display the results
    def check_fuel_status(self):
        fuel_data = self.fetch_fuel_data()  
        lowest_tanks = self.find_lowest_ten_fuel_tanks(fuel_data)  
        self.display_lowest_fuel_tanks(lowest_tanks)  

    # TODO: Create method to simulate data from a database or API
    # Placeholder for a database or API
    def fetch_fuel_data(self):
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

    # TODO: Create method to find ten lowest fuel tanks
    # Sort tanks by fuel levels and return ten lowest tanks
    def find_lowest_ten_fuel_tanks(self, fuel_data):
        sorted_tanks = sorted(fuel_data.items(), key=lambda x: x[1])  
        return sorted_tanks[:10]  

    # TODO: Create method to display the lowest tanks using message box
    # Format tank info for the display
    # Show info in message box
    # messagebox.showinfo()
    def display_lowest_fuel_tanks(self, lowest_tanks):
        tank_info = "\n".join(f"Tank ID: {tank[0]}, Fuel Level: {tank[1]}%" for tank in lowest_tanks)
        messagebox.showinfo("Low Fuel Tanks", tank_info)  

    # TODO: Create method to add a new customer
    # Using Arguments: name, address, phone, email
    def add_customer(self, name, address, phone, email):
        # try-except block to handle any invalid user input
        try:
            # Create a new customer object and save it to the database
            new_customer = Customer(name, address, phone, email, 1000)  
            self.writer.save_customer_to_db(new_customer) 
            return True  
        except Exception as e:
            print(f"Error: {e}") 
            return False  

# Entry point for the program
# Create and run main application
if __name__ == "__main__":
    FuelManagementApp()  