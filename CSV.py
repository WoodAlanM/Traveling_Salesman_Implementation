import csv

# Pretty simple.  This class handles CSV retrieval
def getrows(path_to_csv):
    rows = []
    file = open(path_to_csv)
    csvreader = csv.reader(file)

    for row in csvreader:
        rows.append(row)

    file.close()

    return rows

