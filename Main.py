from HashTable import HashTable
from Truck import Truck
from CSV import getrows
from AdjacencyMatrix import getAdjacencyMatrix

HUB = "4001 South 700 East"

def runMainProgram():
    # Uses getrows function from CSV.py to retrieve the data
    # from the csv files.
    distance_rows = getrows("WGUPS Distance Table (CSV).csv")
    package_rows = getrows("WGUPS Package File (CSV).csv")
    adjMatrix = getAdjacencyMatrix("WGUPS Distance Table (CSV).csv")

    # Isolates the package data and inserts it into
    # the hash table.
    package_dict = getPackageDict(package_rows)
    for key, data in package_dict.items():
        ht.insert(key, data)

    loadTrucks(package_dict, adjMatrix)

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


def loadTrucks(package_dict):
    truck1 = Truck(8, 0)
    truck2 = Truck(8, 0)

    # Manually load trucks
    truck1_list = [1, 2, 4, 5, 7, 8, 14, 15, 19, 20, 29, 30, 31, 34, 37, 40]
    truck2_list = [3, 10, 12, 17, 18, 21, 22, 23, 24, 25, 26, 27, 33, 36, 38, 39]
    truck3_list = [6, 9, 11, 13, 16, 28, 32, 35]

    for package in truck1_list:
        truck1.add_package(package, package_dict[package])

    for package in truck2_list:
        truck2.add_package(package, package_dict[package])

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

    distance_dict = {}

    truck_package_dict = truck.package_dict

    start_location = HUB
    next_location = ''
    distance_dict = {}

    for key, value in truck_package_dict.items():
        # Get address of package
        next_location = value[0]
        next_location_distance = 0.0
        for row in adjMatrix:
            if not row[0] == '':
                if row[0] == next_location:
                    for x in range(1, len(adjMatrix[0]) - 2):
                        if adjMatrix[0][x] == start_location:
                    #         Matching start location stopped here

                    break
                else:
                    pass
        distance_dict[key] = value



    #STOPPING HERE FOR THE EVENING

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