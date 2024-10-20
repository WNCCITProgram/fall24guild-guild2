"""
    Name: writer_module.py
    Author: Guild Two
    Created: 19 October 2024
    Purpose: Python program that contains WriterPackage, Customer,
    and FeulTank classes.  Sets up customer and feul tank database,
    saves, fetches, and loads customer data to and from a CSV file.
"""
"""writer_module.py handles any database operations such as data
saving and loading.  It will also define the structure for 
customers and fuel tanks."""

""" Use both writer_module.py and writer_package.py in the same
directory in order to run. """

# Imports for writer module
# Import numpy for any potential computations
# Import sqlite3 for database creation and management
# Import csv for any file operations
import numpy as np
import sqlite3 
import csv  

# TODO: Create customer class
""" Below are examples of what information (attributes) to use. """
class Customer:
    # Initialize customer object, set up attributes for new instance of customer
    def __init__(self, name, address, phone, email, credit_limit):
        self.name = name  # Customer name
        self.address = address  # Customer address
        self.phone = phone  # Customer phone number
        self.email = email  # Customer email address
        self.credit_limit = credit_limit  # Customer credit limit
        self.tanks = []  # List that will hold any associated fuel tanks for customer

# TODO: Create FuelTank class to represent a customer's fuel tank
""" Below are examples of what attributes for fuel tanks may be used. """
class FuelTank:
    # Initialize FuelTank object, set up attributes for new instance of fuel tank
    def __init__(self, serial_number, fuel_type, size, make, year):
        self.serial_number = serial_number  # Feul tank serial number
        self.fuel_type = fuel_type  # Type of fuel it contains
        self.size = size  # Size of the tank
        self.make = make  # Make of the tank
        self.year = year  # Year of production
        self.fuel_level = 100  # Assume the tank starts full

# TODO: Create a main class (WriterPackage) to handle the fuel management system
class WriterPackage:
    # Initialize WriterPackage object
    def __init__(self):
        self.customers = {}  # Create Dictionary to hold customer information
        self.setup_database()  # Initialize the setup of the database

    # TODO: Create Method to set up the SQLite database and create tables for
    # customer and fuel tank information
    def setup_database(self):
        self.conn = sqlite3.connect('customers.db')  # Connect to the database
        self.cursor = self.conn.cursor()  # Create a cursor for executing SQL commands
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customers (
                id INTEGER PRIMARY KEY,  # Unique customer ID number
                name TEXT,  # Customer name
                address TEXT,  # Customer address
                phone TEXT,  # Customer phone number
                email TEXT,  # Customer email address
                credit_limit REAL  # Customer credit limit
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS FuelTanks (
                id INTEGER PRIMARY KEY,  # Unique tank ID
                customer_id INTEGER,  # Foreign key linking to Customers table
                serial_number TEXT,  # Tank serial number
                fuel_type TEXT,  # Type of fuel
                size INTEGER,  # Size of the tank
                make TEXT,  # Make of the tank
                year INTEGER,  # Year of production
                fuel_level REAL,  # Current fuel level
                FOREIGN KEY (customer_id) REFERENCES Customers (id)  # Define foreign key relationship
            )
        ''')
        self.conn.commit()  # Commit any changes to the database

    # TODO: Create Method to save customer data to the database
    # Takes a Customer object as a parameter and saves the
    # customer's data to the SQLite database.
    def save_customer_to_db(self, customer):
        # Try-except block that will handle any database errors
        try:
            self.cursor.execute('''
                INSERT INTO Customers (name, address, phone, email, credit_limit)
                VALUES (?, ?, ?, ?, ?)
            ''', (customer.name, customer.address, customer.phone, customer.email, customer.credit_limit))
            self.conn.commit()  # Commit any changes
        # Raise exception for an error
        # except sqlite3.Error as e
        except sqlite3.Error as e:
            raise Exception(f"Error saving customer: {e}")  

    # TODO: Create Method to fetch customer data based on the master key
    # Master key is customer ID for example
    # Queries database for the customer associated for the given ID number
    # Returns customer data as a single record
    def fetch_customer_data(self, master_key):
        self.cursor.execute('SELECT * FROM Customers WHERE id = ?', (master_key,))  # Customer data query
        return self.cursor.fetchone()  # Return single record

    # TODO: Create Method to save data to a CSV file using csv module
    # Accepts a filename and data
    def save_data(self, filename, data):
        with open(filename, 'w', newline='') as file:  # Open file in write 'w' mode
            writer = csv.writer(file)  # Create a CSV writer object
            writer.writerows(data)  # Write the data to the file

    # TODO: Create Method to load data from a CSV file
    # Accepts a filename and reads the data from the csv file
    # and returns as a list
    def load_data(self, filename):
        with open(filename, 'r') as file:  # Open file in read mode
            reader = csv.reader(file)  # Create a CSV reader object
            return list(reader)  # Return the data as a list

    # TODO: Create Method to close the database connection once user is finished
    def close_connection(self):
        self.conn.close()  # Close database connection
