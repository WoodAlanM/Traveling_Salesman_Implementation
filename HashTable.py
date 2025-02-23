# Alan Wood
# HashTable class

class HashTable:

    # Upon hashtable initialization a default capacity is set
    # and a table(list) is created and populated with lists
    def __init__(self, capacity=10):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    # Method for inserting a value into the hash table
    def insert(self, package_id, data):
        bucket = hash(package_id) % len(self.table)
        bucket_list = self.table[bucket]

        for container in bucket_list:
            if container[0] == package_id:
                container[1] = data
                return True

        key_value = [package_id, data]
        bucket_list.append(key_value)
        return True

    def search(self, package_id):
        bucket = hash(package_id) % len(self.table)
        bucket_list = self.table[bucket]
        # If the bucket list contains more than one item
        # search through the items one by one to find a matching
        # package id else check the one item.  If the one item
        # does not match then return None.
        if len(bucket_list) > 1:
            for package in bucket_list:
                if package[0] == package_id:
                    return package
        else:
            if bucket_list[0][0] == package_id:
                return bucket_list[0]
            else:
                return None

    def remove(self, package_id):
        bucket = hash(package_id) % len(self.table)
        bucket_list = self.table[bucket]

        for container in bucket_list:
            if container[0] == package_id:
                bucket_list.remove([container[0], container[1]])
