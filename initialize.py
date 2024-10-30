# csv is used to read from the excel sheets and extract data this
# will be used to add the rows to package objects then each package object
# will be stored in the package hash table. 
import csv
import package
import packageHash
import addressHash

# For each row in the package file sheet provided, create a Package object
# and insert into the hash table and return. 
def initPackageHash():
    packageFile = open('package_file.csv', 'r')
    reader = csv.reader(packageFile)
    hash = packageHash.Hash
    
    for row in reader:
        
        # The excel sheet isn't all package data. For any row that doesn't have an id
        # that will convert to an integer in the first column catch the 
        # ValueError thrown and don't try to 
        # create a package object. These include the WGU header of the table etc. 
        try:
            if int(row[0]):
                
                # If the package note has delayed on flight or wrong address
                # initialize it with a status of delayed. All other packages
                # are initialzed with a status of at hub. The rest of the initialization
                # is just taking the cells of the row from the excel spreadsheet and initializing
                # the appropriate package object variables with these values. 
                if 'Delayed on flight' in row[7] or 'Wrong address' in row[7]:
                    hash.insert(hash, package.Package(row[0], row[1], row[2], row[4], row[5], row[6], 'Delayed'))
                    continue
                hash.insert(hash, package.Package(row[0], row[1], row[2], row[4], row[5], row[6]))


        except ValueError as ve:
            continue
            
    packageFile.close()

    return hash

# Gets distance data from the excel sheet
def getDistanceData():
    distanceFile = open('distance_table.csv')
    reader = csv.reader(distanceFile)
    distanceArray = []
    addressMap = addressHash.AddressHash

    # Loop through earch row in the distance file spreadsheet. 
    # All the headers were removed and so the first row indicating
    # the hub starts at index 1. so index 0 continues. if the first
    # cell of a row is an empy string that means that all actual
    # data in the table has been retrieved and the loop breaks.
    for index, row in enumerate(reader):
        if index == 0:
            continue
        if row[0] == '':
            break

        # remove cell 0 from the row. This has a more detailed discription
        # of the location. I.E contonwood regional softball complex. Only
        # The address is needed as the addresses in the package table only
        # have the actual addresses and not the names of the buildings
        row.pop(0)

        # This checks to see if the address has a zip code. All zip codes
        # in the table are in parenthesis and the rest of the address
        # isn't. The addresses in the package file don't have zip codes.
        # so to make them match I remove the zip code off of the address
        # here. If there's no zip code then this isn't neccesary. I.E.
        # The first entry which is just HUB. 
        try:
            address = row[0][0:row[0].index('(')]
        except ValueError as ve:
            address = row[0]
        
        # This is the array that represents the array key and it's corrosonding
        # index value which represents its index in the distanceArray. 
        addressArr = [address, index - 1]

        # Inserts the addressArr in the addressMap. The address map takes an
        # address and returns it's corresponding row/column index for the distance
        # array
        addressMap.insert(addressMap, addressArr)

        # removes the new 0 cell from the row as the address is no longer needed
        # and only distance data is required for the distance array.
        row.pop(0)

        # Appends remaining distance data to the distance array.
        distanceArray.append(row)

    distanceFile.close()

    # Returns the distanceArray and address map. These two values will
    # be unpacked by the caller. 
    return [distanceArray, addressMap]

