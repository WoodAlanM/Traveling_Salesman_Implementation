# Alan Wood
# WGU Computer Science
# Data Structures and Algorithms 2
# Student ID: 012051293

from HashTable import HashTable
from Truck import Truck
from CSV import getrows
from AdjacencyMatrix import getAdjacencyMatrix
from collections import Counter
from datetime import datetime

# Constant for hub address
HUB = "4001 South 700 East"

# Constants for package id's for each trucks
TRUCK1_LIST = [6, 7, 8, 13, 14, 15, 16, 19, 20, 25, 29, 30, 31, 34, 37, 40]
# Needed to change Sta to Station and S to South in WGUPS Distance Table (CSV)
TRUCK2_LIST = [1, 3, 10, 12, 18, 21, 22, 23, 24, 26, 27, 36, 38, 39]
TRUCK3_LIST = [5, 9, 11, 2, 4, 17, 28, 32, 33, 35]

def runMainProgram():
    # Uses getrows function from CSV.py to retrieve the data
    # from the csv files.
    package_rows = getrows("WGUPS Package File (CSV).csv")

    # Instantiate each truck
    truck1 = Truck(1, 8, 0)
    truck2 = Truck(2, 9, 5)
    truck3 = Truck(3, 10, 20)

    # Isolates the package data and inserts it into
    # the hash table.
    package_dict = getPackageDict(package_rows)
    for key, data in package_dict.items():
        ht.insert(key, data)

    truck_list = []

    # Load trucks with given package lists
    loadTruck(truck1, package_dict, TRUCK1_LIST)
    loadTruck(truck2, package_dict, TRUCK2_LIST)
    loadTruck(truck3, package_dict, TRUCK3_LIST)

    truck_list.append(truck1)
    truck_list.append(truck2)
    truck_list.append(truck3)

    # Test algorithm
    travelAlgo(truck1)
    travelAlgo(truck2)
    travelAlgo(truck3)

    # Begin user interface
    print("********************************************")
    print("WGUPS Package Delivery Information Interface")
    print("********************************************\n")

    boolean_in_program = True

    while boolean_in_program:
        print("Please choose from the following choices: ")
        print("1. View Package Information")
        print("2. View Delivery Details")
        print("3. View Truck Travel Data")
        print("4. Exit\n")
        selection = int(input("Please make a selection: "))
        if selection == 1:
            # UI for searching for a specific packages information
            # will need to add a time filter
            package_id = int(input("Please enter the package ID number: "))
            package_info = lookupPackage(package_id)
            if package_info:
                print("\nPackage number " + str(package_id) + " information:")
                print(f"Address:       {package_info[1][0]: >30}")
                print(f"Deadline:      {package_info[1][3]: >30}")
                print(f"City:          {package_info[1][1]: >30}")
                print(f"Zipcode:       {package_info[1][2]: >30}")
                print(f"Weight (KILO): {package_info[1][4]: >30}")
                print(f"Status:        {package_info[1][5]: >30}\n")
            else:
                print(f"Package number {package_id} was not found.\n")
        elif selection == 2:
            # Ui for delivery details
            boolean_in_detail = True
            while boolean_in_detail:
                print("Please choose from the following choices:")
                print("1. Package delivery information")
                print("2. Overall delivery information")
                print("3. Exit detail menu\n")
                detail_selection = input("Please make a selection: ")
                if int(detail_selection) == 1:
                    # This will collect a time window to show current delivery statuses
                    time_window_start = input("Enter a start time in hh:mm format: ")
                    time_start_AMPM = input("Enter (A/a) for AM or (P/p) for PM: ")
                    if time_start_AMPM == 'A' or time_start_AMPM == 'a':
                        time_window_start = time_window_start + " AM"
                    elif time_start_AMPM == 'P' or time_start_AMPM == 'p':
                        time_window_start = time_window_start + " PM"
                    time_window_stop = input("Enter a stop time in hh:mm format: ")
                    time_stop_AMPM = input("Enter (A/a) for AM or (P/p) for PM: ")
                    if time_stop_AMPM == 'A' or time_stop_AMPM == 'a':
                        time_window_stop = time_window_stop + " AM"
                    elif time_stop_AMPM == 'P' or time_stop_AMPM == 'p':
                        time_window_stop = time_window_stop + " PM"
                    for truck in truck_list:
                        sort_format = ("%I:%M %p")
                        # Send the time window to time window retrieval to update the list based on viewing time
                        time_window_update_list = timeWindowRetrieveList(truck, time_window_stop)
                        print(f"Truck number {truck.truck_number} detailed update list:")
                        print(f"Showing detail snapshot between {time_window_start} and {time_window_stop}:")
                        # Display delivery details
                        print("\n")
                        print(f"{'Truck: ': <10}{'ID:': <5}{'Delivered Time:': <20}{'Address:': <40}{'City:': <20}"
                              f"{'Zipcode:': <10}{'Deadline:': <12}{'Kg:': <5}{'Status:': <12}")
                        for detail in time_window_update_list:
                            print(
                                f"{truck.truck_number: <10}{detail[0]: <5}{detail[1]: <20}{detail[2][0]: <40}{detail[2][1]: <20}"
                                f"{detail[2][2]: <10}{detail[2][3]: <12}{detail[2][4]: <5}{detail[2][5]: <12}")
                        print("\n")
                elif int(detail_selection) == 2:
                    # Collect all delivery details
                    collected_deliver_detail_list = []
                    for delivery_truck in truck_list:
                        for detail in delivery_truck.update_list:
                            detail.append(delivery_truck.truck_number)
                            collected_deliver_detail_list.append(detail)
                    # Set format for time to filter the collected list by delivery time
                    sort_format = ("%I:%M %p")
                    # Sort the collected list by delivery time
                    sorted_delivery_data = sorted(collected_deliver_detail_list, key=lambda detail_list:
                                                  datetime.strptime(detail_list[1], sort_format))
                    # Display delivery details
                    print("\n")
                    print(f"{'Truck: ': <10}{'ID:': <5}{'Delivered Time:': <20}{'Address:': <40}{'City:': <20}"
                          f"{'Zipcode:': <10}{'Deadline:': <12}{'Kg:': <5}{'Status:': <12}")
                    for detail in sorted_delivery_data:
                        print(f"{detail[-1]: <10}{detail[0]: <5}{detail[1]: <20}{detail[2][0]: <40}{detail[2][1]: <20}"
                              f"{detail[2][2]: <10}{detail[2][3]: <12}{detail[2][4]: <5}{detail[2][5]: <12}")
                    print("\n")
                elif int(detail_selection) == 3:
                    # Exit delivery detail
                    boolean_in_detail = False
            print("\n")
        elif selection == 3:
            # UI For detailed information about truck travel
            boolean_in_delivery_detail = True
            while boolean_in_delivery_detail:
                print("Please choose from the following choices:")
                print("1. Truck travel information")
                print("2. Total mileage for all trucks")
                print("3. Exit detail menu\n")
                delivery_detail_selection = input("Please make a selection: ")
                if int(delivery_detail_selection) == 1:
                    # This will give you a breakdown of the places the truck visited
                    # as well as the miles traveled to get there.
                    # This is helpful for checking my work
                    chosen_truck = input("Please choose truck 1, 2, or 3: ")
                    if int(chosen_truck) == 1:
                        print(f"{'Delivery:': <10}{'Location:': <40}{'Miles Traveled There:': >20}")
                        last_delivery = 0
                        for data_item in truck1.distance_traveled_data:
                            last_delivery = last_delivery + 1
                            if not data_item[0] == -1:
                                print(f"{data_item[0]: <10}{data_item[1]: <40}{data_item[2]: >20}")
                        print(f"{last_delivery - 1: <10}{truck1.distance_traveled_data[1][1]: <40}"
                              f"{truck1.distance_traveled_data[1][2]: >20}\n")
                    elif int(chosen_truck) == 2:
                        print(f"{'Delivery:': <10}{'Location:': <40}{'Miles Traveled There:': >20}")
                        last_delivery = 0
                        for data_item in truck2.distance_traveled_data:
                            last_delivery = last_delivery + 1
                            if not data_item[0] == -1:
                                print(f"{data_item[0]: <10}{data_item[1]: <40}{data_item[2]: >20}")
                        print(f"{last_delivery - 1: <10}{truck2.distance_traveled_data[1][1]: <40}"
                              f"{truck2.distance_traveled_data[1][2]: >20}\n")
                    elif int(chosen_truck) == 3:
                        print(f"{'Delivery:': <10}{'Location:': <40}{'Miles Traveled There:': >20}")
                        last_delivery = 0
                        for data_item in truck3.distance_traveled_data:
                            last_delivery = last_delivery + 1
                            if not data_item[0] == -1:
                                print(f"{data_item[0]: <10}{data_item[1]: <40}{data_item[2]: >20}")
                        print(f"{last_delivery - 1: <10}{truck3.distance_traveled_data[1][1]: <40}"
                              f"{truck3.distance_traveled_data[1][2]: >20}\n")
                elif int(delivery_detail_selection) == 2:
                    # This will display the total miles traveled by all trucks
                    total_mileage = 0.0
                    for delivery_truck in truck_list:
                        total_mileage = total_mileage + delivery_truck.miles_driven
                    total_mileage = round(total_mileage, 2)
                    print(f"Total traveled miles for all trucks: {total_mileage: >30}\n")
                elif int(delivery_detail_selection) == 3:
                    # Exit truck detail
                    boolean_in_delivery_detail = False
        elif selection == 4:
            # Exit program
            boolean_in_program = False


def loadTruck(truck, package_dict, list_for_truck):
    # Manually load trucks
    for package in list_for_truck:
        truck.add_package(package, package_dict[package])


def timeWindowRetrieveList(truck, time_end):
    update_list = truck.update_list

    sort_format = ("%I:%M %p")
    # Sort the trucks update list by delivery time
    sorted_update_data = sorted(update_list, key=lambda detail_list:
                                datetime.strptime(detail_list[1], sort_format))

    # If a delivery has not occurred, update status and delivery time
    for update in sorted_update_data:
        if update[1] >= time_end:
            update[2][-1] = "EN ROUTE"
            update[1] = 'EN ROUTE'

    return sorted_update_data


def travelAlgo(truck):
    adjMatrix = getAdjacencyMatrix('WGUPS Distance Table (CSV).csv')

    # I use these values to compare addresses with package id's
    truck_package_dict = truck.package_dict
    truck_keys = []
    truck_addresses = []
    key_address_dict = {}
    for key, value in truck_package_dict.items():
        truck_keys.append(key)
        truck_addresses.append(value[0])
        key_address_dict[key] = value[0]

    address_counter = Counter(truck_addresses)

    # I use this to keep track of whether an address has more than one package
    location_count_dict = {}
    for address in truck_addresses:
        location_count_dict[address] = address_counter[address]

    # Set starting conditions
    start_location = HUB
    # This list will hold package id, distance traveled, address, and number of packages at address
    shortest_distance_destination = [0, 0.0, '', 0]
    ordered_addresses = []
    ordered_route_list = []

    total_packages = len(truck_keys)
    # Goes through each delivery in the truck
    # will have to make an adjustment for a truck with less
    # than 16 packages in it.
    for delivery in range(0, total_packages):
        # This variable keeps track of the row index for
        # cross-referencing start vs next locations
        row_number = 0
        # Enter the first row of the adjacency matrix and traverse horizontally
        # looking for the start location
        for item in adjMatrix[0]:
            if str(item) == start_location:
                # Access every row of the adjacency matrix and traverse the first
                # index to find the next location
                for row in adjMatrix:
                    # If the address is the delivery address of one of the trucks packages
                    if str(row[0]) in key_address_dict.values():
                        # If the delivery address has not already been entered into the list
                        if str(row[0]) not in ordered_addresses:
                            # find the index of the address, to find the key (package id)
                            index_of_address = truck_addresses.index(str(row[0]))
                            associated_truck_key = truck_keys[index_of_address]
                            # If the value for shortest distance variable has not been set
                            # then set it to the corresponding next location distance
                            # and continue until all the addresses have been traversed
                            # this will guarantee the selection of the shortest travel distance
                            if float(shortest_distance_destination[1]) == 0.0:
                                shortest_distance_destination[0] = associated_truck_key
                                shortest_distance_destination[1] = row[row_number]
                                shortest_distance_destination[2] = row[0]
                                shortest_distance_destination[3] = location_count_dict[
                                    str(shortest_distance_destination[2])]
                            elif float(shortest_distance_destination[1]) > float(row[row_number]):
                                shortest_distance_destination[0] = associated_truck_key
                                shortest_distance_destination[1] = row[row_number]
                                shortest_distance_destination[2] = row[0]
                                shortest_distance_destination[3] = location_count_dict[
                                    str(shortest_distance_destination[2])]
                # Precautionary check for the shortest distance
                # location to ensure it is not added twice.  As well
                # as the list of ordered addresses.  These may not be necessary
                if shortest_distance_destination not in ordered_route_list:
                    ordered_route_list.append(shortest_distance_destination)
                if shortest_distance_destination[2] not in ordered_addresses:
                    ordered_addresses.append(shortest_distance_destination[2])
                    start_location = shortest_distance_destination[2]
                    shortest_distance_destination = [0, 0.0, '', 0]
                break
            else:
                row_number = row_number + 1
        continue

    cleaned_ordered_route_list = []

    # Since some of the packages are delivered to the same address
    # this will clean the list and remove any empty package items
    for address in ordered_route_list:
        if not int(address[0]) == 0:
            cleaned_ordered_route_list.append(address)

    # Sends the list to the truck object where it is further handled
    truck.send_ordered_list(cleaned_ordered_route_list)

# This function will take the package ID and return the information associated with it
def retrievePackageData(packageID):
    package_data = []

    return package_data

# Takes rows from the package csv and removes the first 8 rows
# This gets the meaningful data. Then the data is added to a dictionary
# where the package id is the key, and the package information
# is the data.
def getPackageDict(package_rows):
    package_dict = {}
    count = 0
    for row in package_rows:
        if count > 7:
            needed_indices = [1, 2, 4, 5, 6]
            needed_data = [row[i] for i in needed_indices]
            needed_data.append("NOT SET")
            package_dict[int(row[0])] = needed_data
        else:
            count = count + 1

    return package_dict


# This sends the hash table the package id and then returns information
# about it, if it exists.
def lookupPackage(packageID):
    return ht.search(packageID)


if __name__ == "__main__":
    ht = HashTable()
    runMainProgram()