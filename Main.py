from HashTable import HashTable
from Truck import Truck
from CSV import getrows
from AdjacencyMatrix import getAdjacencyMatrix
from collections import Counter
from datetime import datetime

HUB = "4001 South 700 East"

TRUCK1_LIST = [1, 2, 4, 5, 7, 8, 14, 15, 19, 20, 29, 30, 31, 34, 37, 40]
TRUCK2_LIST = [3, 10, 12, 17, 18, 21, 22, 23, 24, 25, 26, 27, 33, 36, 38, 39]
TRUCK3_LIST = [6, 9, 11, 13, 16, 28, 32, 35]

def runMainProgram():
    # Uses getrows function from CSV.py to retrieve the data
    # from the csv files.
    package_rows = getrows("WGUPS Package File (CSV).csv")

    truck1 = Truck(1, 8, 0)
    truck2 = Truck(2, 8, 0)

    # Isolates the package data and inserts it into
    # the hash table.
    package_dict = getPackageDict(package_rows)
    for key, data in package_dict.items():
        ht.insert(key, data)

    truck_list = []

    # Load trucks with given package lists
    loadTruck(truck1, package_dict, TRUCK1_LIST)
    loadTruck(truck2, package_dict, TRUCK2_LIST)

    truck_list.append(truck1)
    truck_list.append(truck2)

    # Test algorithm
    travelAlgo(truck1)
    travelAlgo(truck2)

    # Begin user interface
    print("********************************************")
    print("WGUPS Package Delivery Information Interface")
    print("********************************************\n")

    boolean_in_program = True

    while boolean_in_program:
        print("Please choose from the following choices: ")
        print("1. View Package Information")
        print("2. View Delivery Details")
        print("3. View Total Truck Mileage")
        print("4. Exit\n")
        selection = int(input("Please make a selection: "))
        if selection == 1:
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
            boolean_in_detail = True
            print("********************************************")
            print("*********** Delivery Detail Menu ***********")
            print("********************************************\n")
            while boolean_in_detail:
                print("Please choose from the following choices:")
                print("1. Truck delivery information")
                print("2. Package delivery information")
                print("3. Overall delivery information")
                print("4. Exit detail menu\n")
                detail_selection = input("Please make a selection: ")
                if int(detail_selection) == 1:
                    filter_truck_info = input("Would you like to filter truck delivery information by time? (y/n): ")
                    if filter_truck_info == 'y' or filter_truck_info == 'Y':
                        time_format = ("%I:%M %p")
                        time_window_start = input("Enter a start time in hh:mm format: ")
                        time_start_AMPM = input("Enter (A/a) for AM or (P/p) for PM:")
                        if time_start_AMPM == 'A' or time_start_AMPM == 'a':
                            time_window_start = time_window_start + " AM"
                        elif time_start_AMPM == 'P' or time_start_AMPM == 'p':
                            time_window_start = time_window_start + " PM"
                        try:
                            formatted_start_time = datetime.strptime(time_window_start, time_format)
                        except ValueError as e:
                            print("Error formatting time input...\n")
                        time_window_stop = input("Enter a stop time in hh:mm format: ")
                        time_stop_AMPM = input("Enter (A/a) for AM or (P/p) for PM: ")
                        if time_stop_AMPM == 'A' or time_stop_AMPM == 'a':
                            time_window_stop = time_window_stop + " AM"
                        elif time_stop_AMPM == 'P' or time_stop_AMPM == 'p':
                            time_window_stop = time_window_stop + " PM"
                        try:
                            formatted_stop_time = datetime.strptime(time_window_start, time_format)
                        except ValueError as e:
                            print("Error formatting time input...\n")
                elif int(detail_selection) == 2:
                    filter_package_info = input("Would you like to package delivery information by time? (y/n): ")
                    continue
                elif int(detail_selection) == 3:
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
                    # Display delivery times
                    print("\n")
                    print(f"{'Truck: ': <10}{'ID:': <5}{'Delivered Time:': <20}{'Address:': <40}{'City:': <20}"
                          f"{'Zipcode:': <10}{'Deadline:': <12}{'Kg:': <5}{'Status:': <12}")
                    for detail in sorted_delivery_data:
                        print(f"{detail[-1]: <10}{detail[0]: <5}{detail[1]: <20}{detail[2][0]: <40}{detail[2][1]: <20}"
                              f"{detail[2][2]: <10}{detail[2][3]: <12}{detail[2][4]: <5}{detail[2][5]: <12}")
                    print("\n")
                elif int(detail_selection) == 4:
                    boolean_in_detail = False
            print("\n")

        elif selection == 4:
            boolean_in_program = False

def loadTruck(truck, package_dict, list_for_truck):

    # Manually load trucks
    for package in list_for_truck:
        truck.add_package(package, package_dict[package])

    # early_package_dict = {}
    # for key, data in package_dict.items():
    #     if data[3] == '10:30 AM' or data[3] == '9:00 AM':
    #         early_package_dict[key] = data[3]
    #
    # # Test to see how long it will take to deliver each of those packages
    #
    # nearest_to_furthest_dict = {}
    #
    # for key in early_package_dict.keys():
    #     package_data = package_dict[key]
    #     for address in adj_matrix:
    #         if not address[0] == '':
    #             if address[0] == package_data[0]:
    #                 nearest_to_furthest_dict[key] = address[1]
    #
    # count = 0
    # for data in nearest_to_furthest_dict.values():
    #     count = count + float(data)
    #
    # print(count)


def travelAlgo(truck):
    adjMatrix = getAdjacencyMatrix('WGUPS Distance Table (CSV).csv')

    truck_package_dict = truck.package_dict
    truck_keys = []
    truck_addresses = []
    key_address_dict = {}
    for key, value in truck_package_dict.items():
        truck_keys.append(key)
        truck_addresses.append(value[0])
        key_address_dict[key] = value[0]

    addressCounter = Counter(truck_addresses)

    location_count_dict = {}
    for address in truck_addresses:
        location_count_dict[address] = addressCounter[address]

    # Set starting conditions
    start_location = HUB
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

    for address in ordered_route_list:
        if not int(address[0]) == 0:
            cleaned_ordered_route_list.append(address)

    truck.send_ordered_list(cleaned_ordered_route_list)

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


def lookupPackage(packageID):
    return ht.search(packageID)


if __name__ == "__main__":
    ht = HashTable()
    runMainProgram()