# Hash table made for the package objects. It stores package objects
# but does not use any additional classes to implement the functionality
# so shouldn't conflict with the requirements of part A
class Hash:
    table = [[], [], [], [], [], [], [], [], [], []]

    # Stores all required data from part A into the hash table.
    # It does this by storing a package object. Since the
    # Package object has all fields required in part A this should
    # fulfil part A. It uses the package ID as the hash value. 
    def insert(self, package):
        self.table[int(package.id) % 10].append(package)

    # Takes an id and returns a package object. The object has
    # all fields required in part B and so should fulfil part B
    def lookUp(self, id):
        tempArr = self.table[int(id) % 10]
        for package in tempArr:
            if int(package.id) == id:
              
                return package
    
        return None
    
    
        
        