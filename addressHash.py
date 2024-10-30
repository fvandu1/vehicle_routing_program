# Hash table that takes address as a key and returns it's appropriate
# index value for the distanceArray
class AddressHash:
    # Hash table
    table = [[], [], [], [], [], [], [], [], [], []]


    # Method for inserting new addresses and their corrosponding index
    # The hash part of the actual table is created from the first
    # set of number in the address before street names or anything unless
    # the first part of the address is a word like with the HUB.
    # If this is the case it uses the unicode value of the first
    # character of the address as the hash value. 
    def insert(self, addressArray):
        address = addressArray[0].strip()

        try:
            id = address[0:address.index(' ')]
        except ValueError as ve:
            id = address

        addressArray[0] = address

        try:
            self.table[int(id) % 10].append(addressArray)
        except ValueError as ve:
            self.table[int(ord(id[0:1])) % 10].append(addressArray)

    # Lookup a index for the distance table by address. Uses the same
    # hash rules defined in the insert method. 
    def lookUp(self, address):
        address = address.strip()
       
        try:
            id = address[0:address.index(' ')]
        except ValueError as ve:
            id = address
       
        try:
            for key in self.table[int(id) % 10]:
                if key[0] == address:
                    return key[1] 
            
        except ValueError as ve:
            for key in self.table[int(ord(id[0:1])) % 10]:
                if key[0] == address:
                    return key[1]


