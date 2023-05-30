import csv

'''
 Develop a hash table, that has an insertion function that takes the following 
 components as input and inserts the components into the hash table
•   package ID number - check
•   delivery address - check
•   delivery deadline - check
•   delivery city - check
•   delivery zip code - check
•   package weight - check
•   delivery status (e.g., delivered, en route)
'''

class HashTable:
    def __init__(self, capacity=16):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    #inserts new item into the hashtable
    def insert(self, key, item):
        typeKey = type(key)
        useKey = key
        if typeKey is int:
            useKey = str(key)
        #gets list to place in bucket

        #converting key to a string to not run into hash differences because of different types
        bucket = hash(useKey) % len(self.table)
        bucketList = self.table[bucket]

        #will check if key is already in the bucket. if yes, will update it
        for keyValue in bucketList:
            if keyValue[0] == key:
                keyValue[1] = item
                return True

        #if key is unique
        keyValuePair = [key, item]
        bucketList.append(keyValuePair)
        return True

    #will search for item in hash table
    #This is our lookup function requirement from Section F.
    def find(self, key):
        typeKey = type(key)
        useKey = key
        if typeKey is int:
            useKey = str(key)

        '''
        THIS IS 1st ATTEMPT CODE
        #needed to convert keyFind to str(keyFind) or else it would return packageID instead of hashed(packageID)
        bucket = hash(str(key)) % len(self.table) #tried using self.capacity first, did not work
        '''
        bucket = hash(useKey) % len(self.table)
        bucketList = self.table[bucket]

        for kvP in bucketList:
            #[0] index in kvP is the key
            #hopefully this handles collision?
            if useKey == kvP[0]:
                return kvP[1] #index 1 of kvP is the value in the 'key-Value' pair

        #will only get here is key is never found
        return None

    #will remove item from Hash table
    def remove(self, key):
        index = hash(key) % len(self.capacity)
        node = self.table[index]

        if key in node:
            node.remove(key)
