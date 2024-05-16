from CSV import getrows


def getAdjacencyMatrix(file_path):
    distance_rows = getrows(file_path)

    # Gets the rows starting with row 8 and removes the first
    # entry because it is not necessary
    needed_rows = distance_rows[7:]
    needed_rows[0][0] = ''

    horizontal_address_list = []
    vertical_address_list = []

    # Cleans up the data in the first row and enters it into
    # the horizontal address list
    for item in needed_rows[0]:
        if not item == '':
            temp_list = item.splitlines()
            address = temp_list[1].split(',')[0].lstrip()
            horizontal_address_list.append(address)

    # Adds a blank entry to the beginning of the horizontal address list
    horizontal_address_list.insert(0, '')

    # Cleans up the data in the first column of the distance rows
    # and adds it to the vertical address list
    for item in needed_rows:
        if not item[1] == '':
            temp_list = item[1].splitlines()
            address = temp_list[0].lstrip()
            vertical_address_list.append(address)

    # Changes the first vertical entry from HUB to the address
    # of the first entry in the horizontal address list
    vertical_address_list[0] = horizontal_address_list[1]

    # Retrieves just the rows where the distances are entered
    distance_needed_rows = distance_rows[8:]

    distance_matrix = []

    # Places only the distances from each row into a distance matrix list
    for row in distance_needed_rows:
        distance_matrix.append(row[2:])

    distance_matrix.insert(0, horizontal_address_list)

    count = 0

    for item in distance_matrix:
        if not item[0] == '':
            item.insert(0, vertical_address_list[count])
            count = count + 1

    return distance_matrix
