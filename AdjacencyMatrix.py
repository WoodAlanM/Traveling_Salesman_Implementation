from CSV import getrows

distance_rows = getrows("WGUPS Distance Table (CSV).csv")

needed_rows = distance_rows[7:]

print(needed_rows)