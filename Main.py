from HashTable import HashTable
from Truck import Truck
from CSV import getrows
from AdjacencyMatrix import getAdjacencyMatrix

HUB = "4001 South 700 East"

TRUCK1_LIST = [1, 2, 4, 5, 7, 8, 14, 15, 19, 20, 29, 30, 31, 34, 37, 40]
TRUCK2_LIST = [3, 10, 12, 17, 18, 21, 22, 23, 24, 25, 26, 27, 33, 36, 38, 39]
TRUCK3_LIST = [6, 9, 11, 13, 16, 28, 32, 35]

def runMainProgram():
    # Uses getrows function from CSV.py to retrieve the data
    # from the csv files.
    distance_rows = getrows("WGUPS Distance Table (CSV).csv")
    package_rows = getrows("WGUPS Package File (CSV).csv")
    adjMatrix = getAdjacencyMatrix("WGUPS Distance Table (CSV).csv")

    truck1 = Truck(8, 0)
    truck2 = Truck(8, 0)

    # Isolates the package data and inserts it into
    # the hash table.
    package_dict = getPackageDict(package_rows)
    for key, data in package_dict.items():
        ht.insert(key, data)

    loadTruck(truck1, package_dict, TRUCK1_LIST)

    # Test algorithm
    travelAlgo(truck1)

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
            package_id = int(input("\nPlease enter the package ID number: "))
            package_info = lookupPackage(package_id)

            if package_info:
                print("Package number " + str(package_id) + " information:")
                print(f"Address:       {package_info[1][0]}")
                print(f"Deadline:      {package_info[1][3]}")
                print(f"City:          {package_info[1][1]}")
                print(f"Zipcode:       {package_info[1][2]}")
                print(f"Weight (KILO): {package_info[1][4]}")
                print(f"Status:        {package_info[1][5]}\n")
            else:
                print(f"Package number {package_id} was not found.\n")
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

    # Set starting conditions
    start_location = HUB
    shortest_distance_destination = [0, 0.0, '']
    ordered_addresses = []
    ordered_route_list = []


    print(adjMatrix)
    for delivery in range(0, 16):
        # Maybe move this number thing
        row_number = 0
        for item in adjMatrix[0]:
            if str(item) == start_location:
                for row in adjMatrix:
                    if str(row[0]) in key_address_dict.values():
                        if str(row[0]) not in ordered_addresses:
                            print('got here')
                            index_of_address = truck_addresses.index(str(row[0]))
                            associated_truck_key = truck_keys[index_of_address]
                            if shortest_distance_destination[1] == 0.0:
                                shortest_distance_destination[1] = row[row_number]
                                shortest_distance_destination[0] = associated_truck_key
                                shortest_distance_destination[2] = row[0]
                            elif shortest_distance_destination[1] > row[row_number]:
                                shortest_distance_destination[1] = row[row_number]
                                shortest_distance_destination[0] = associated_truck_key
                                shortest_distance_destination[2] = row[0]
                if shortest_distance_destination not in ordered_route_list:
                    ordered_route_list.append(shortest_distance_destination)
                if shortest_distance_destination[2] not in ordered_addresses:
                    ordered_addresses.append(shortest_distance_destination[2])
                    start_location = shortest_distance_destination[2]
                    shortest_distance_destination = [0, 0.0, '']
                    print(ordered_route_list)
                    print(str(start_location))
                break
            else:
                row_number = row_number + 1
        continue

    print(len(ordered_route_list))

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
            needed_data.append("NOT_SET")
            package_dict[int(row[0])] = needed_data
        else:
            count = count + 1

    return package_dict


def lookupPackage(packageID):
    return ht.search(packageID)


if __name__ == "__main__":
    ht = HashTable()
    runMainProgram()