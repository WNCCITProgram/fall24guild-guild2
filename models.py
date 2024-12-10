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