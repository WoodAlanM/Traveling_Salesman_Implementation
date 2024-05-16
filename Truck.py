import datetime
import math

class Truck:
    def __init__(self, departure_hour, departure_minute):
        self.miles_driven = 0
        self.package_dict = {}
        self.route_ordered_dict = {}
        self.update_list = []

        today = datetime.date.today()
        self.departure_time = datetime.datetime(today.year,today.month,today.day, departure_hour, departure_minute, 0)

    def add_package(self, package_id, package_data):
        self.package_dict[package_id] = package_data

    def add_miles(self, miles):
        self.miles_driven = self.miles_driven + miles

    def complete_delivery(self, package_id, distance_traveled):
        package_data = self.package_dict[package_id]
        delivered_address = package_data[0]
        del self.package_dict[package_id]
        self.add_miles(distance_traveled)
        self.delivery_update(delivered_address)

    def delivery_update(self, delivered_address):
        time_change_numeric = math.ceil(self.miles_driven * 0.3)
        delivery_time = self.departure_time + datetime.timedelta(minutes=time_change_numeric)
        update = []
        update.append(delivery_time)
        update.append(delivered_address)
        update.append(self.package_dict)




