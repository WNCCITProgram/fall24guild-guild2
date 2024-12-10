"""
    Name: database.py
    Authors: Guild Two (consolidated)
    Created: 03 November 2024
    Revised: 10 November 2024
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
    
    #~~~~ Claude ~~~ #
    def fetch_all_customers(self):
        """Fetch all customers from the database"""
        try:
            self.cursor.execute('''
                SELECT id, name, address, phone, email, account_number, 
                    city_addy, zipcode, billable_status, credit_limit 
                FROM Customers
                ORDER BY name
            ''')
            customers = self.cursor.fetchall()
            print(f"Fetched {len(customers)} customers from database")  # Debug print
            # Handle error by ensuring fetch_all_customers returns and empty
            # list and not 'None'
            return customers if customers else []
        except sqlite3.Error as e:
            print(f"Database error: {e}")  # Debug print
            return []
    #~~~~

    def save_to_csv(self, filename, data):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def load_from_csv(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            return list(reader)
        
    #~~~ Claude
    def save_fuel_tank(self, customer_id, tank):
        """Save a new fuel tank and associate it with a customer"""
        try:
            self.cursor.execute('''
                INSERT INTO FuelTanks (
                    customer_id, serial_number, fuel_type, capacity,
                    manufacturer, year, rental, contents
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                customer_id, tank.serial_number, tank.fuel_type,
                tank.capacity, tank.manufacturer, tank.year,
                tank.rental, tank.contents
            ))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving tank: {e}")
            return False

    def fetch_customer_tanks(self, customer_id):
        """Fetch all fuel tanks associated with a customer"""
        try:
            self.cursor.execute('''
                SELECT * FROM FuelTanks
                WHERE customer_id = ?
                ORDER BY serial_number
            ''', (customer_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching tanks: {e}")
            return []

    def fetch_all_tanks(self):
        """Fetch all fuel tanks with customer information"""
        try:
            self.cursor.execute('''
                SELECT FuelTanks.*, Customers.name as customer_name
                FROM FuelTanks
                JOIN Customers ON FuelTanks.customer_id = Customers.id
                ORDER BY Customers.name, FuelTanks.serial_number
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching all tanks: {e}")
            return []
     #~~~~

    def close(self):
        self.conn.close()
