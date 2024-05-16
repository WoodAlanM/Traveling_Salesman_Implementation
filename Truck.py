
class Truck:
    def __init__(self):
        self.miles_driven = 0
        self.package_list = []

    def add_package(self, package):
        self.package_list.append(package)

    def add_miles(self, miles):
        self.miles_driven = self.miles_driven + miles
