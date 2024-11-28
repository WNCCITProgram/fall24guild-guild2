
"""
    Name: gui_V2.py
    Authors: Guild Two (consolidated)
    Created: 03 November 2024
    First Revision: 10 November 2024
    Second Revision: 28 November 2024
    Purpose: GUI implementation using tkinter
"""
""" Revised with added error handling and weather API addition."""

# RD - Claude.ai inquired to regarding EIA api structure, the returns from EIA are
# complicated, even with good documentation the desired returns are difficult to parse
# for exactly what you want, can be a fire hose of data


# Week 15 - Import webbrowser module to open Google maps link
import webbrowser
import tkinter as tk
from tkinter import messagebox
from models import Customer, FuelTank
from database import DatabaseManager
import asyncio
import python_weather  # RD - import the weather_V2 function, not the python_weather
# from weather_V2 import WeatherApp  # RD - Disable this, the class is repeated below
import re
from fuel_price import fetch_fuel_price # Import fuel price API fetch fuel price function

# NOTE: had to manually install python weather to get it to work
# is there a way to integrate the install so local machines dont have to pip it?

#~~~~ Claude Code
from tkinter import messagebox, ttk  # Add ttk import for better looking table
#~~~~

# Abbigail - Might add a weather API into the GUI eventually (currently looking into it)
class FuelManagementApp:
    def __init__(self):
        self.root = tk.Tk()
        self.db = DatabaseManager()
        self.setup_gui()


    def setup_gui(self):
        self.root.title("Customer Fuel Management System")

        # Set the window icon with ICO file
        self.root.iconbitmap("gas.ico")  

        # Customer Information Fields
        labels = ['Customer Name', 'Address', 'Phone', 'Email', 
                 'Account Number', 'Optional Address', 'City', 'Zipcode']
        self.entries = {}
        
        for i, label in enumerate(labels):
            tk.Label(self.root, text=label).grid(row=i+1, column=0, sticky=tk.W, padx=5, pady=2)
            self.entries[label] = tk.Entry(self.root)
            self.entries[label].grid(row=i+1, column=1, padx=5, pady=2)

        # Set button style format with black background and white text
        button_style = {"bg": "black", "fg": "white", "relief": "flat", "padx": 10, "pady": 5}

        # Set second button style format with green background and white text
        button_style_2 = {"bg": "green", "fg": "white", "relief": "flat", "padx": 10, "pady": 5}

        #Abbigail - Maybe make the window size slightly bigger and space out buttons?
        # Buttons
        tk.Button(self.root, text="Add Customer", 
                command=self.add_customer, **button_style).grid(row=(len(labels)+1), column=0, pady=10)
        tk.Button(self.root, text="Check Fuel Status", 
                command=self.check_fuel_status, **button_style).grid(row=(len(labels)+1), column=1, pady=10)
        # Weather section - This integrates the WeatherApp class from weather_V2.py
        self.weather_app = WeatherApp(self.root)  # Instantiate the WeatherApp class here
        #~~~~ Claude
        tk.Button(self.root, text="View Customers", 
                command=self.show_customer_list, **button_style).grid(
                     row=(len(labels)+1), column=2, pady=10)
        tk.Button(self.root, text="View All Tanks", 
                command=self.show_all_tanks, **button_style).grid(
                     row=(len(labels)+1), column=3, pady=10)
        #~~~~
        # Week 13 Additional button to check fuel prices
        tk.Button(self.root, text="Check Fuel Price", 
                command=self.check_fuel_price, **button_style_2).grid(row=0, column=3, pady=10)
        # Week 15 - Additional button to open Google Maps
        tk.Button(self.root, text="Google Maps", 
                  command=self.open_google_maps, **button_style).grid(row=(len(labels)+2), column=0, pady=10)
    def open_google_maps(self):
        # Get address from the customer entry field
        address = self.entries['Address'].get()
        
        if address:
            # Create a URL that links to Google Maps with the customer's address
            maps_url = f"https://www.google.com/maps?q={address.replace(' ', '+')}"
            webbrowser.open(maps_url)
        else:
            messagebox.showerror("Error", "Please enter a valid address") # Display error message for invalid address

    # Week 13 additional function, Check fuel price function
    def check_fuel_price(self):
        # Fetch fuel prices using the API
        prices = fetch_fuel_price()

        # Display results to user
        # If-else statement to handle error for retrieval failure
        """ if prices is not None:
            message = "Fuel Prices for the last 8 months:\n\n"
            for i, price in enumerate(prices, start=1):
                message += f"Month {i}: ${price}\n"
            messagebox.showinfo("Fuel Prices", message)
        else:
            messagebox.showerror("Error", "Failed to retrieve fuel price data.")   
            """
        if prices['success']:
            message = f"Base Price: ${prices['base_price']:.3f}/gal\nCustomer Price: ${prices['customer_price']:.3f}/gal"
            messagebox.showinfo("Current Propane Prices", message)
        else:
            messagebox.showerror("Error", f"Failed to retrieve price data\n{prices.get('error', '')}")
            
            
            
    def add_customer(self):
        # Get values from entry fields
        values = {label: entry.get().strip() 
                 for label, entry in self.entries.items()}
        
        # Validate required fields
        if not all([values['Customer Name'], values['Address'], 
                   values['Phone'], values['Email']]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        # Validation for phone and email
        if not self.is_valid_phone(values['Phone']):
            messagebox.showerror("Error", "Invalid phone number format")
            return

        if not self.is_valid_email(values['Email']):
            messagebox.showerror("Error", "Invalid email format")
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

    def is_valid_phone(self, phone):
        """ Validate phone number format (e.g., 555-1234 or (555) 123-4567) """
        phone_regex = re.compile(r"^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$")
        return bool(phone_regex.match(phone))

    def is_valid_email(self, email):
        """ Validate email format """
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return bool(email_regex.match(email))

    # Abbigail - Maybe we can change the fuel data from tank1, tank2, tank3 to 1,2,3 so it reads better in the program
    # RD - Absolutely, this should be a priority hit for Week 13, its a main feature promotion
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
    #~~~ Claude
    def show_customer_list(self):
        CustomerListWindow(self.root, self.db)
    def show_all_tanks(self):
        ViewTanksWindow(self.root, self.db)
    #~~~
    def run(self):
        self.root.mainloop()
        
# The WeatherApp class handles weather fetching functionality
# RD - This is a copy-import of the weather_V2
class WeatherApp:
    def __init__(self, root):
        """ Initialize the WeatherApp instance."""
        self.root = root
        self.weather_label = tk.Label(root, text="Local Weather: ")
        # RD - We would rather the info go into the available text box
        self.weather_label.grid(row=0, column=0, sticky=tk.E, padx=5, pady=2)
        # needed adjustment, was over lapping
        
        # add a manual weather display so that it does not get auto generated from
        # main gui 
        self.weather_display = tk.Entry(root,width=10, state='readonly')
        self.weather_display.grid(row=0, column=1,columnspan=2,sticky=tk.W, pady=2, padx=5)

        # Set button style formatting with blue background and white text
        button_style = {"bg": "blue", "fg": "white", "relief": "flat", "padx": 10, "pady": 5}

        # Add a button to fetch weather data
        self.get_weather_button = tk.Button(root, text="Get Weather", command=self.get_weather, **button_style)
        self.get_weather_button.grid(row=0, column=2, sticky=tk.W, padx=5,pady=2)
        
        # RD - async issue correction attempts
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    async def fetch_weather(self):
        """ Fetch weather data asynchronously using python-weather API."""
        # RD - Exception catch
        try:
            async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
                weather = await client.get('Akron')  # Example city (can be replaced with user input)
                return weather.temperature
        except:
            print(f"Fetch Error: Weather") # could/should have more specific error calls
            return None

    def get_weather(self):
        """ Method to fetch weather and update the label asynchronously when the button is clicked."""
        def update_weather():
        # Use the Tkinter event loop to schedule the task.
            self.weather_display.config(state='normal')
            self.weather_display.delete(0, tk.END)
            temp = asyncio.run(self.fetch_weather())  # Run the async function synchronously
            if temp is not None:
                self.weather_display.insert(0, f"{temp}°F")
            else:
                self.weather_display.insert(0, "No Weather Here Boss")
            self.weather_display.config(state='readonly')
    
    # Update weather on the event loop
        self.root.after(0, update_weather)


#~~~~ Claude
class CustomerListWindow:
    def __init__(self, parent, db):
        self.window = tk.Toplevel(parent)
        self.window.title("Customer List")
        self.window.geometry("800x600")
        self.db = db
        self.setup_gui()

    def setup_gui(self):
        # Create frame for the table
        frame = ttk.Frame(self.window)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Create treeview with defined columns
        self.columns = ('ID', 'Name', 'Address', 'Phone', 'Email', 'Account #', 
                       'City', 'Zipcode', 'Status', 'Credit Limit')
        self.tree = ttk.Treeview(frame, columns=self.columns, show='headings')

        # Set column headings and initial widths
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Set default width

        # Add scrollbars
        y_scroll = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        x_scroll = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        x_scroll.grid(row=1, column=0, sticky='ew')

        # Configure grid weights
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Add refresh and test data buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="Refresh", 
                  command=self.refresh_customer_list).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Add Test Data", 
                  command=self.add_test_data).pack(side='left', padx=5)

        # Bind right-click menu
        self.tree.bind("<Button-3>", self.show_context_menu)

        # Load customer data
        self.refresh_customer_list()

    def show_context_menu(self, event):
        # Get the item under the cursor
        item = self.tree.identify_row(event.y)
        if item:
            # Select the item
            self.tree.selection_set(item)
            customer_id = self.tree.item(item)['values'][0]
            customer_name = self.tree.item(item)['values'][1]

            # Create context menu
            menu = tk.Menu(self.window, tearoff=0)
            menu.add_command(label="Add Tank", 
                           command=lambda: self.add_tank(customer_id, customer_name))
            menu.add_command(label="View Tanks", 
                           command=lambda: self.view_customer_tanks(customer_id, customer_name))
            menu.post(event.x_root, event.y_root)

    def add_tank(self, customer_id, customer_name):
        AddTankWindow(self.window, self.db, customer_id, customer_name, 
                     self.refresh_customer_list)

    def view_customer_tanks(self, customer_id, customer_name):
        ViewTanksWindow(self.window, self.db, customer_id, customer_name)

    def refresh_customer_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch and insert customer data
        customers = self.db.fetch_all_customers()
        print(f"Refreshing list with {len(customers)} customers")  # Debug print
        
        if not customers:
            no_data_label = ttk.Label(self.window, 
                                    text="No customers found in database")
            no_data_label.pack(pady=20)
            return

        for customer in customers:
            # Ensure all values are strings
            values = [str(value) if value is not None else "" for value in customer]
            self.tree.insert('', 'end', values=values)

    def add_test_data(self):
        """Add some test data to the database"""
        test_customers = [
            Customer(
                name="John Doe",
                address="123 Main St",
                phone="555-0101",
                email="john@example.com",
                account_number="A001",
                city_addy="Springfield",
                zipcode="12345",
                billable_status="Credit",
                credit_limit=1000
            ),
            Customer(
                name="Jane Smith",
                address="456 Oak Ave",
                phone="555-0102",
                email="jane@example.com",
                account_number="A002",
                city_addy="Shelbyville",
                zipcode="12346",
                billable_status="Cash",
                credit_limit=0
            )
        ]
        
        for customer in test_customers:
            self.db.save_customer(customer)
        
        self.refresh_customer_list()
        messagebox.showinfo("Success", "Test data added successfully!")

#~~~~

#~~~ Claude
class AddTankWindow:
    def __init__(self, parent, db, customer_id, customer_name, refresh_callback=None):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Add Tank for {customer_name}")
        self.window.geometry("400x500")
        self.db = db
        self.customer_id = customer_id
        self.refresh_callback = refresh_callback
        self.setup_gui()

    def setup_gui(self):
        # Create input fields
        fields = [
            ('Serial Number', 'serial_number'),
            ('Fuel Type', 'fuel_type'),
            ('Capacity (gallons)', 'capacity'),
            ('Manufacturer', 'manufacturer'),
            ('Year', 'year'),
            ('Rental (yes/no)', 'rental'),
            ('Current Contents (gallons)', 'contents')
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields):
            tk.Label(self.window, text=label).grid(row=i, column=0, padx=5, pady=5)
            self.entries[field] = tk.Entry(self.window)
            self.entries[field].grid(row=i, column=1, padx=5, pady=5)

        # Add Save button
        tk.Button(self.window, text="Save Tank", 
                 command=self.save_tank).grid(row=len(fields), column=0, 
                                            columnspan=2, pady=20)

    def save_tank(self):
        try:
            # Validate input to catch invalid input and display error message
            capacity = int(self.entries['capacity'].get())
            contents = float(self.entries['contents'].get())
            rental = self.entries['rental'].get().lower() in ['yes', 'y', '1']  # Normalize rental field
            # Create new tank object
            tank = FuelTank(
                serial_number=self.entries['serial_number'].get(),
                fuel_type=self.entries['fuel_type'].get(),
                capacity=int(self.entries['capacity'].get()),
                manufacturer=self.entries['manufacturer'].get(),
                year=self.entries['year'].get(),
                rental=self.entries['rental'].get(),
                contents=float(self.entries['contents'].get())
            )

            # Save tank to database
            if self.db.save_fuel_tank(self.customer_id, tank):
                messagebox.showinfo("Success", "Tank added successfully!")
                if self.refresh_callback:
                    self.refresh_callback()
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Failed to add tank")
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers for capacity and contents")

class ViewTanksWindow:
    def __init__(self, parent, db, customer_id=None, customer_name=None):
        self.window = tk.Toplevel(parent)
        self.window.title("Fuel Tanks" if customer_id is None else f"Fuel Tanks - {customer_name}")
        self.window.geometry("1000x600")
        self.db = db
        self.customer_id = customer_id
        self.setup_gui()

    def setup_gui(self):
        # Create frame for the table
        frame = ttk.Frame(self.window)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Create treeview with customer name at the beginning
        columns = ('Customer', 'ID', 'Serial Number', 'Fuel Type', 'Capacity',
                  'Manufacturer', 'Year', 'Rental', 'Contents', '% Full')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')

        # Set column headings and widths
        column_widths = {
            'Customer': 150,
            'ID': 50,
            'Serial Number': 100,
            'Fuel Type': 100,
            'Capacity': 80,
            'Manufacturer': 120,
            'Year': 60,
            'Rental': 60,
            'Contents': 80,
            '% Full': 70
        }

        for col, width in column_widths.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)

        # Add scrollbars
        y_scroll = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        x_scroll = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        x_scroll.grid(row=1, column=0, sticky='ew')

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Add refresh button
        tk.Button(self.window, text="Refresh", 
                 command=self.refresh_tank_list).pack(pady=10)

        self.refresh_tank_list()

    def refresh_tank_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.customer_id is not None:
            tanks = self.db.fetch_customer_tanks(self.customer_id)
        else:
            tanks = self.db.fetch_all_tanks()

        for tank in tanks:
            try:
                # For single customer view, we need to add the customer name
                if self.customer_id is not None:
                    # Assuming the customer name wasn't in the fetch_customer_tanks result
                    customer_name = tank[1]  # Adjust index if needed
                else:
                    # For all tanks view, customer name should be in the last column
                    customer_name = tank[-1]  # Get customer name from the last column

                # Extract relevant data
                tank_id = str(tank[0])
                serial = str(tank[2]) if tank[2] is not None else ""
                fuel_type = str(tank[3]) if tank[3] is not None else ""
                capacity = float(tank[4]) if tank[4] is not None else 0
                manufacturer = str(tank[5]) if tank[5] is not None else ""
                year = str(tank[6]) if tank[6] is not None else ""
                rental = str(tank[7]) if tank[7] is not None else ""
                contents = float(tank[8]) if tank[8] is not None else 0

                # Calculate percentage full
                percent_full = (contents / capacity * 100) if capacity > 0 else 0

                # Create the values tuple with customer name at the beginning
                values = (
                    customer_name,
                    tank_id,
                    serial,
                    fuel_type,
                    f"{capacity:,.0f}",  # Format with thousands separator
                    manufacturer,
                    year,
                    rental,
                    f"{contents:,.0f}",  # Format with thousands separator
                    f"{percent_full:.1f}%"
                )
                
                self.tree.insert('', 'end', values=values)
                
            except (ValueError, TypeError) as e:
                print(f"Error processing tank data: {e}")
                # Insert row with error indication
                self.tree.insert('', 'end', values=(
                    customer_name, tank_id, "Error processing tank data", "", "", "", "", "", "", "Error"
                ))
#~~~~




# Assign the App to a variable and run it
if __name__ == "__main__":
    app = FuelManagementApp()
    app.run()
