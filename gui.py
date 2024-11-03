"""
    Name: gui.py
    Author: Guild Two
    Created: 27 October 2024
    Edited: 02 November 2024
    Purpose: GUI module using tkinter to handle user interface.  
    File contains FuelManagementAPPGUI class and add customer 
    and check fuel status methods.
"""

""" Possible GUI framework to use for main program application.  Commit to week 10 branch only."""
import tkinter as tk
from tkinter import messagebox

# Initialize GUI with main window and callback functions.
# add customer and check fuel status callbacks
# Call method to create the GUI components
# self.create_widgets
class FuelManagementAppGUI:
    def __init__(self, master, add_customer_callback, check_fuel_status_callback):
        self.master = master
        self.add_customer_callback = add_customer_callback
        self.check_fuel_status_callback = check_fuel_status_callback
        self.create_widgets()  

    # TODO: Create widgets call method to arrange GUI components

    def create_widgets(self):
        # Set the window title
        self.master.title("Customer Fuel Management System")  

        # TODO: Create input fields for customer details
        # tk.Label(self.master, text=" ").grid(row= )
        # Specify label and grid row and column
        # Entry for the customer name
        tk.Label(self.master, text="Customer Name").grid(row=0)
        self.customer_name = tk.Entry(self.master)  
        self.customer_name.grid(row=0, column=1)

        # Entry for the customer's address
        tk.Label(self.master, text="Address").grid(row=1)
        self.customer_address = tk.Entry(self.master)  
        self.customer_address.grid(row=1, column=1)

        # Entry for the customer's phone number
        tk.Label(self.master, text="Phone").grid(row=2)
        self.customer_phone = tk.Entry(self.master)  
        self.customer_phone.grid(row=2, column=1)

        # Entry for the customer's email address
        tk.Label(self.master, text="Email").grid(row=3)
        self.customer_email = tk.Entry(self.master)  
        self.customer_email.grid(row=3, column=1)

        # TODO: Create buttons that will add a customer and check fuel status
        # tk.Button(self.master, text=" ", command=self."insert method")
        # Specify grid row and column
        tk.Button(self.master, text="Add Customer", command=self.add_customer).grid(row=4, column=0, sticky=tk.W)
        tk.Button(self.master, text="Check Fuel Status", command=self.check_fuel_status).grid(row=5, column=0, sticky=tk.W)

    # TODO: Create method to add new customer via data retrieval from input fields
    # Get customer name
    # Get customer address
    # Get customer phone number
    # Get customer email
    def add_customer(self):
        name = self.customer_name.get().strip()  
        address = self.customer_address.get().strip() 
        phone = self.customer_phone.get().strip()
        email = self.customer_email.get().strip()

        # Handle validation of basic user input
        if not all([name, address, phone, email]):
            messagebox.showerror("Error","You MUST fill out ALL fields.")
            return

        # Use callback function to add the customer
        # If-else statement for message success and failure
        # messagebox.showinfo
        # messagebox.showerror
        if self.add_customer_callback(name, address, phone, email):
            messagebox.showinfo("Success", "Customer added successfully!")
          
        else:
            messagebox.showerror("Error", "Failed to add customer.")  

    # TODO: Create check fuel status callback function
    # Call fuel status check method
    def check_fuel_status(self):
        self.check_fuel_status_callback()  
