"""
    Name: WIP_fuel_project.py
    Author: Richard Dobson
    Created: 10/18/2024
    Purpose: Week 9 classes/methods for storing customer and tank information
      Group 2 WIP non comittal code
"""
# the following code is Work In Progress, not to be applied directly to main without testing

class Customers:
    def __init__(self, name="", account_number="", street_addy="", optional_addy="", city_addy="", zipcode="", billable_status="Cash"):
        # default non arguments can be used to start a customer file, to prevent conflicts
        # or to enable opening accounts where some information is less than clear until technicians arrive
        # customer name
        self._name = name
        # account number
        self._account_number = account_number
        # street address ex. 123 WNCC Ave
        self._street_addy = street_addy
        # optional ex. Apartment #55
        self._optional_addy = optional_addy
        # city ex. Scottsbluff
        self.city_addy = city_addy
        # zipcode ex. 69361
        self._zipcode = zipcode
        # is the customer cash only or do they have a credit account
        # 'Cash' or 'Credit' with cash only being the default setting
        self._billable_status = billable_status
        # underscores are private attributes
        
    # getter methods
    ####################################################################
    
    def get_name(self):
        return self._name
    
    def get_account_number(self):
        return self._account_number
    
    def get_street_addy(self):
        return self._street_addy
    
    def get_optional_addy(self):
        return self._optional_addy
    
    def get_city_addy(self):
        return self._city_addy
    
    def get_zipcode(self):
        return self._zipcode
    
    def get_billable_status(self):
        return self._billable_status
    
    # setter methods
    #######################################################################
    def set_name(self, x):
        self._name = x
    
    def set_account_number(self, x):
        self._account_number = x
    
    def set_street_addy(self, x):
        self._street_addy = x
    
    def set_optional_addy(self, x):
        self._optional_addy = x
    
    def set_city_addy(self, x):
        self._city_addy = x
    
    def set_zipcode(self, x):
        self._zipcode = x
    
    def set_billable_status(self, x):
        self._billable_status = x
    
    
    
class Tanks:
    def __init__(self, tied_customer, serial, capacity, manufacturer, year, fuel_type, rental):
        # for the purposes of coursework, assume all tanks are filed as single units, just one tank at a time
        
        # the customer number of the customer that owns/has this tank
        self._tied_customer = tied_customer
        # liquid size of the tank, functional capacity is different for propane units
        # tanks serial number
        self._serial = serial
        self._capacity = capacity
        # company that made the tank
        self._manufacturer = manufacturer
        # year the tank was built
        self._year = year
        # propane or liquid fuels ie. 'Propane' or 'Gasoline/Diesel'
        # IRL would break down into Regular, Premium, Diesel, and Dyed Diesel categories at a miniumum
        self._fuel_type = fuel_type
        # customer owned or is it a rental, default to 'no', 'rental' if its a rental unit
        self._rental = rental
        
    # getter methods
    #######################################################################
    
    def get_tied_customer(self):
        return self._tied_customer
    
    def get_serial(self):
        return self._serial
    
    def get_capacity(self):
        return self._capacity
    
    def get_manufacturer(self):
        return self._manufacturer
    
    def get_year(self):
        return self._year
    
    def get_fuel_type(self):
        return self._fuel_type
    
    def get_rental(self):
        return self._rental
        
    # setter methods
    #######################################################################
    
    def set_tied_customer(self, x):
        self._tied_customer = x
        
    def set_serial(self, x):
        self._serial = x
    
    def set_capacity(self, x):
        self._capacity = x
    
    def set_manufacturer(self, x):
        self._manufacturer = x
    
    def set_year(self, x):
        self._year = x
    
    def set_fuel_type(self, x):
        self._fuel_type = x
        
    def set_rental(self, x):
        self._rental = x
        
# notes for future:
# customer objects can be created without tanks, tanks should not be creatable without a customer
# a default "corporate" account can be set to reassign company owned but not deployed tanks
# the customer number will be used as a lookup both for which tanks a customer has on site
# and to check a tanks serial number to see who owns it