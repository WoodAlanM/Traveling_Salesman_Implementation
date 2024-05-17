import datetime
import math
from AdjacencyMatrix import getAdjacencyMatrix

MINUTES_PER_MILE = ((1.0/18.0) * 60.0)

class Truck:
    def __init__(self, truck_number, departure_hour, departure_minute):
        self.truck_number = truck_number
        self.miles_driven = 0.0
        self.package_dict = {}
        self.route_ordered_dict = []
        self.update_list = []
        today = datetime.date.today()
        self.running_time = datetime.datetime(today.year, today.month, today.day, departure_hour, departure_minute, 0)
        # This is used later to test my algorithm
        # The first value is the delivery number, second is address, third is distance traveled to get there
        self.distance_traveled_data = [[0, 'HUB', 0]]
        self.departure_time = datetime.datetime(today.year, today.month, today.day, departure_hour, departure_minute, 0)

    def add_package(self, package_id, package_data):
        self.package_dict[package_id] = package_data

    def add_miles(self, miles):
        self.miles_driven = self.miles_driven + float(miles)

    # This method adds the mileage to get back to the hub to the
    # distance traveled data as well as the miles variable
    def send_to_hub(self, final_delivery_address):
        adjMatrix = getAdjacencyMatrix('WGUPS Distance Table (CSV).csv')
        miles_to_hub = 0.0
        for row in adjMatrix:
            if str(row[0]) == str(final_delivery_address):
                miles_to_hub = row[1]
                self.add_miles(row[1])
        travel_data = [-1, 'HUB', miles_to_hub]
        self.distance_traveled_data.append(travel_data)

    # This method receives the ordered delivery list
    # then it sends it to the complete delivery method
    # after updating the distance traveled data list
    def send_ordered_list(self, ordered_list):
        delivery_counter = 1
        # Fix to make the packages say EN ROUTE
        self.route_ordered_dict = ordered_list
        self.send_to_hub(ordered_list[-1][2])
        running_time = self.departure_time
        for delivery in ordered_list:
            # Collect travel data for checking distances
            travel_data = []
            travel_data.append(delivery_counter)
            delivery_counter = delivery_counter + 1
            travel_data.append(delivery[2])
            travel_data.append(delivery[1])
            self.distance_traveled_data.append(travel_data)
            # Set all package statuses to "EN ROUTE"
            package_data = self.package_dict[delivery[0]]
            # This is probably no longer necessary
            package_data[-1] = "EN ROUTE"
            self.complete_delivery(delivery[0], delivery[1], delivery[2], delivery[3], running_time)


    # This method handles creating the delivery updates.  It uses the distance
    # traveled to determine the delivery time.  And it handles situations where
    # more than one package is delivered to the same address
    def complete_delivery(self, package_id, distance_traveled, address, packages_at_address, running_time):
        package_data = self.package_dict[package_id]
        # Update for multi package drop offs
        if packages_at_address > 1:
            multiple_package_dict = {}
            for key, value in self.package_dict.items():
                if value[0] == address:
                    multiple_package_dict[key] = value
            self.add_miles(distance_traveled)
            # This calculates the time it took to get from one location to another
            # and adds it to departure time, which becomes running time at this point
            time_change_numeric = (float(distance_traveled) * MINUTES_PER_MILE)
            self.running_time = self.running_time + datetime.timedelta(minutes=time_change_numeric)
            formatted_time = self.running_time.strftime("%I:%M %p")
            for key, value in multiple_package_dict.items():
                del self.package_dict[key]
                update = []
                update.append(key)
                update.append(formatted_time)
                value[-1] = "DELIVERED"
                update.append(value)
                self.update_list.append(update)
        else:
            # For single package deliveries
            del self.package_dict[package_id]
            self.add_miles(distance_traveled)
            # This calculates the time it took to get from one location to another
            # and adds it to departure time, which becomes running time at this point
            time_change_numeric = (float(distance_traveled) * MINUTES_PER_MILE)
            self.running_time = self.running_time + datetime.timedelta(minutes=time_change_numeric)
            formatted_time = self.running_time.strftime("%I:%M %p")
            update = []
            update.append(package_id)
            update.append(formatted_time)
            package_data[-1] = "DELIVERED"
            update.append(package_data)
            self.update_list.append(update)
