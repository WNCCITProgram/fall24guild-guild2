# File 1: models.py
"""
    Name: models.py
    Authors: Guild Two, Richard Dobson (consolidated)
    Created: 03 November 2024
    Purpose: Core data models for customers and fuel tanks
"""

class Customer:
    def __init__(self, name="", address="", phone="", email="", 
                 account_number="", optional_addy="", city_addy="", 
                 zipcode="", billable_status="Cash", credit_limit=0):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.account_number = account_number
        self.optional_addy = optional_addy
        self.city_addy = city_addy
        self.zipcode = zipcode
        self.billable_status = billable_status
        self.credit_limit = credit_limit
        self.tanks = []  # List to hold associated fuel tanks

class FuelTank:
    def __init__(self, serial_number="", fuel_type="", capacity=0, 
                 manufacturer="", year="", tied_customer="", rental="", contents=0):
        self.serial_number = serial_number
        self.fuel_type = fuel_type
        self.capacity = capacity
        self.manufacturer = manufacturer
        self.year = year
        self.tied_customer = tied_customer
        self.rental = rental
        self.contents = contents
        self._update_percentage()
    
    def _update_percentage(self):
        self.percentage = (self.contents / self.capacity * 100) if self.capacity else 0
    
    def set_contents(self, amount):
        self.contents = amount
        self._update_percentage()
    
    def set_contents_by_percentage(self, percentage):
        self.contents = self.capacity * (percentage / 100)
        self._update_percentage()

# File 2: database.py
"""
    Name: database.py
    Authors: Guild Two (consolidated)
    Created: 03 November 2024
    Purpose: Database operations and data persistence
"""

import sqlite3
import csv

class DatabaseManager:
    def __init__(self):
        self.customers = {}
        self.setup_database()

    def setup_database(self):
        self.conn = sqlite3.connect('customers.db')
        self.cursor = self.conn.cursor()
        
        # Create Customers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                address TEXT,
                phone TEXT,
                email TEXT,
                account_number TEXT,
                optional_addy TEXT,
                city_addy TEXT,
                zipcode TEXT,
                billable_status TEXT,
                credit_limit REAL
            )
        ''')
        
        # Create FuelTanks table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS FuelTanks (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                serial_number TEXT,
                fuel_type TEXT,
                capacity INTEGER,
                manufacturer TEXT,
                year INTEGER,
                rental TEXT,
                contents REAL,
                FOREIGN KEY (customer_id) REFERENCES Customers (id)
            )
        ''')
        self.conn.commit()

    def save_customer(self, customer):
        try:
            self.cursor.execute('''
                INSERT INTO Customers (
                    name, address, phone, email, account_number,
                    optional_addy, city_addy, zipcode, billable_status, credit_limit
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                customer.name, customer.address, customer.phone, customer.email,
                customer.account_number, customer.optional_addy, customer.city_addy,
                customer.zipcode, customer.billable_status, customer.credit_limit
            ))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def fetch_customer(self, customer_id):
        self.cursor.execute('SELECT * FROM Customers WHERE id = ?', (customer_id,))
        return self.cursor.fetchone()

    def save_to_csv(self, filename, data):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def load_from_csv(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            return list(reader)

    def close(self):
        self.conn.close()

# File 3: gui.py
"""
    Name: gui.py
    Authors: Guild Two (consolidated)
    Created: 03 November 2024
    Purpose: GUI implementation using tkinter
"""

import tkinter as tk
from tkinter import messagebox
from models import Customer, FuelTank
from database import DatabaseManager

class FuelManagementApp:
    def __init__(self):
        self.root = tk.Tk()
        self.db = DatabaseManager()
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Customer Fuel Management System")

        # Customer Information Fields
        labels = ['Customer Name', 'Address', 'Phone', 'Email', 
                 'Account Number', 'Optional Address', 'City', 'Zipcode']
        self.entries = {}
        
        for i, label in enumerate(labels):
            tk.Label(self.root, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            self.entries[label] = tk.Entry(self.root)
            self.entries[label].grid(row=i, column=1, padx=5, pady=2)

        # Buttons
        tk.Button(self.root, text="Add Customer", 
                 command=self.add_customer).grid(row=len(labels), column=0, pady=10)
        tk.Button(self.root, text="Check Fuel Status", 
                 command=self.check_fuel_status).grid(row=len(labels), column=1, pady=10)

    def add_customer(self):
        # Get values from entry fields
        values = {label: entry.get().strip() 
                 for label, entry in self.entries.items()}
        
        # Validate required fields
        if not all([values['Customer Name'], values['Address'], 
                   values['Phone'], values['Email']]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return

        # Create and save customer
        customer = Customer(
            name=values['Customer Name'],
            address=values['Address'],
            phone=values['Phone'],
            email=values['Email'],
            account_number=values['Account Number'],
            optional_addy=values['Optional Address'],
            city_addy=values['City'],
            zipcode=values['Zipcode']
        )

        if self.db.save_customer(customer):
            messagebox.showinfo("Success", "Customer added successfully!")
            self._clear_entries()
        else:
            messagebox.showerror("Error", "Failed to add customer")

    def check_fuel_status(self):
        # Simulate fuel data for demonstration
        fuel_data = {
            "tank1": 30,
            "tank2": 20,
            "tank3": 50,
        }
        
        # Sort tanks by fuel level
        sorted_tanks = sorted(fuel_data.items(), key=lambda x: x[1])
        
        # Display results
        message = "Tanks requiring attention:\n\n"
        for tank_id, level in sorted_tanks:
            if level < 40:  # Alert threshold
                message += f"Tank {tank_id}: {level}%\n"
        
        messagebox.showinfo("Fuel Status", message)

    def _clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FuelManagementApp()
    app.run()
