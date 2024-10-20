# just a testing frame
import WIP_fuel_project

customer1 = WIP_fuel_project.Customers(name="Todd Howard", account_number="007", street_addy="Barbosa Dr", optional_addy="", city_addy="Hilichuck", zipcode="23320", billable_status="Cash")
print(customer1.get_name())
print(customer1.get_account_number())
customer1.set_name("Nigel Hambone")
print(customer1.get_name())

tank1 = WIP_fuel_project.Tanks(tied_customer="007", serial="M-1234", capacity="1000", manufacturer="Quality", year="2012", fuel_type="Propane", rental="No")
print(tank1.get_all())