from HashTable import HashTable
from Truck import Truck
from CSV import getrows


def runMainProgram():
    # Uses getrows function from CSV.py to retrieve the data
    # from the csv files.
    distance_rows = getrows("WGUPS Distance Table (CSV).csv")
    package_rows = getrows("WGUPS Package File (CSV).csv")

    # Isolates the package data and inserts it into
    # the hash table.
    package_dict = getPackageDict(package_rows)
    for key, data in package_dict.items():
        ht.insert(key, data)

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


def travelAlgo(distance_rows):
    truck1 = Truck(8, 0)
    truck2 = Truck(8, 0)

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