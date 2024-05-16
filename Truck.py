import datetime
import math

class Truck:
    def __init__(self, departure_hour, departure_minute):
        self.miles_driven = 0.0
        self.package_dict = {}
        self.route_ordered_dict = []
        self.update_list = []
        today = datetime.date.today()
        self.departure_time = datetime.datetime(today.year,today.month,today.day, departure_hour, departure_minute, 0)

    def add_package(self, package_id, package_data):
        self.package_dict[package_id] = package_data

    def add_miles(self, miles):
        self.miles_driven = self.miles_driven + float(miles)


    def send_ordered_list(self, ordered_list):

        # Fix to make the packages say EN ROUTE

        self.route_ordered_dict = ordered_list
        for delivery in ordered_list:
            # Set all package statuses to "EN ROUTE"
            package_data = self.package_dict[delivery[0]]
            package_data[-1] = "EN ROUTE"
            self.complete_delivery(delivery[0], delivery[1], delivery[2], delivery[3])


    def complete_delivery(self, package_id, distance_traveled, address, packages_at_address):
        package_data = self.package_dict[package_id]
        # Update for multi package drop offs
        if packages_at_address > 1:
            multiple_package_dict = {}
            for key, value in self.package_dict.items():
                if value[0] == address:
                    multiple_package_dict[key] = value
            self.add_miles(distance_traveled)
            time_change_numeric = math.ceil(self.miles_driven * 0.3)
            delivery_time = self.departure_time + datetime.timedelta(minutes=time_change_numeric)
            for key, value in multiple_package_dict.items():
                del self.package_dict[key]
                update = []
                update.append(key)
                update.append(delivery_time.time())
                value[-1] = "DELIVERED"
                update.append(value)
                self.update_list.append(update)
        else:
            # For single package deliveries
            del self.package_dict[package_id]
            self.add_miles(distance_traveled)
            time_change_numeric = math.ceil(self.miles_driven * 0.3)
            delivery_time = self.departure_time + datetime.timedelta(minutes=time_change_numeric)
            update = []
            update.append(package_id)
            update.append(delivery_time.time())
            package_data[-1] = "DELIVERED"
            update.append(package_data)
            self.update_list.append(update)

        print(self.miles_driven)
        print(self.package_dict)