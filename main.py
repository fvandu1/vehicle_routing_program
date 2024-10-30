# Forrest VanDuren Student ID: 010620769
print('Forrest VanDuren Student ID: 010620769')

# Import a timedelta for keeping track of delivery times.
from datetime import timedelta
# Import initialize. It's a file I made that has functions that creates
# all the packages objects and addsd them to the package hash table. 
# Also has function creating an address map that maps addresses to
# row and column indicies for the distance array as well as the distance
# array itself
import initialize
# Import truck class to initialize truck objects
import truck
# Import math class
import math

# Initialize two trucks with the name truck1 and truck2
truck1 = truck.Truck("Truck1")
truck2 = truck.Truck("Truck2")

# Create the package hash object filled with all the package objects
# from the initPackageHash function in the initialize file. 
packageHash = initialize.initPackageHash()

# Unpack distance array and addressMap from the return value of the
# getDistanceData function. The distance table has the word HUB in the
# cell that all the other locations have their addresses. Because of this
# I created the address map so that the word HUB alone is used to identify
# The hub instead of its address. In a lot of locations throughout the program
# I use package.address with the addressMap to get the corrosponding index
# of that address for the distance array. Becuse of this, and because
# no package object is created with hub as the address, there's several
# location where using package.address would throw an attribute error. 
# Those locations are when the index of the route being read is the hub.
# So either the first location in the route, the last, or during one of 
# the trips back to the hub to get the delayed packages. So there's several
# places where I have try except blocks set up to handle this and pass
# 'HUB' into the addressMap instead of package.address. This represents
# normal operation of the program as it is desinged and isn't an actual error
distanceArray, addressMap = initialize.getDistanceData()

# Function that takes two addresses and returns the distance between
# them using the address map and distance array
def getDistance(address1, address2):
    id1 = addressMap.lookUp(addressMap, address1)
    id2 = addressMap.lookUp(addressMap, address2)

    if id1 > id2:
        return distanceArray[id1][id2]
    
    return distanceArray[id2][id1]

# Add required packages to truck2. When packages are added to a truck
# They're automatically given the 'Loaded' status. This is so I can
# Make sure I don't add the same package twice. 
truck2.addPackage(packageHash.lookUp(packageHash, 3))
truck2.addPackage(packageHash.lookUp(packageHash, 18))
truck2.addPackage(packageHash.lookUp(packageHash, 36))
truck2.addPackage(packageHash.lookUp(packageHash, 38))

# Add other packages that need to go together to truck1
truck1.addPackage(packageHash.lookUp(packageHash, 13))
truck1.addPackage(packageHash.lookUp(packageHash, 14))
truck1.addPackage(packageHash.lookUp(packageHash, 15))
truck1.addPackage(packageHash.lookUp(packageHash, 16))
truck1.addPackage(packageHash.lookUp(packageHash, 19))
truck1.addPackage(packageHash.lookUp(packageHash, 20))

# Load more packages by matching addresses that are already in the truck
# If the package has the loaded or delayed status it isn't loaded. Delayed
# status is given to any truck with a delay given in the package note when
# the package object is initialized. The loaded and delayed statuses are only
# used transiently to help with the assignment and routing of the trucks
# during the actual runtime of the program only At Hub, en route and delivered
# status are used. As defined in the requriments. 
for package in truck1.packages:
    for array in packageHash.table:
        for unloaded in array:
            if unloaded.status != 'Loaded' and unloaded.status != 'Delayed':
                if unloaded.address == package.address:
                    truck1.addPackage(unloaded)

# Same as above but for truck2
for package in truck2.packages:
    for array in packageHash.table:
        for unloaded in array:
            if unloaded.status != 'Loaded' and unloaded.status != 'Delayed':
                if unloaded.address == package.address:
                    truck2.addPackage(unloaded)

# The below loop adds packages that have deadlines to both truck1 and truck2.
# I wanted to make sure the deadline packages get on the first load of
# 16 packages. Like above it doesn't load loaded or delayed packages and
# then also only loads packages that don't have EOD as their deadline. 
# Also stops if the number of packages on the truck goes above 16.
i = 0
while i < 40:
    for array in packageHash.table:
        for index, package in enumerate(array):
            if package.status != 'Loaded' and package.status != 'Delayed':
                if package.deadline != 'EOD':
                    if index % 2 == 0 and len(truck1.packages) < 16:
                        truck1.addPackage(package)


                        for package in truck1.packages:
                            for array in packageHash.table:
                                for unloaded in array:
                                    if unloaded.status != 'Loaded' and unloaded.status != 'Delayed':
                                        if unloaded.address == package.address:
                                            truck1.addPackage(unloaded)


                    if index % 2 == 1 and len(truck1.packages) < 16:
                        truck2.addPackage(package)
                        
                        for package in truck2.packages:
                            for array in packageHash.table:
                                for unloaded in array:
                                    if unloaded.status != 'Loaded' and unloaded.status != 'Delayed':
                                        if unloaded.address == package.address:
                                            truck2.addPackage(unloaded)

    i = i + 1
                    

# Adds any additional packages that aren't loaded and don't have
# delayed status to the trucks until each truck has 16 packages. 
for array in packageHash.table:
    for index, package in enumerate(array):
        if 'At hub' in package.status:
            if len(truck1.packages) < 16:
                truck1.addPackage(package)
                try:
                    i = index + 1
                    while i < len(array):
                        if package == array[i]:
                          truck1.addPackage(array[i])  
                        i = i + 1      
                except IndexError as err:
                    print('index out of range')
                continue
            if len(truck2.packages) < 16:
                truck2.addPackage(package)
                try:
                    i = index + 1
                    while i < len(array):
                        if package == array[i]:
                          truck2.addPackage(array[i]) 
                        i = i + 1
                except IndexError as err:
                    print('index out of range')

i = 0

# This function is for getting a timeDelta from the distance between
# two address. The time delta represents the amount of time it takes
# to travel that distance while going 18 miles an hour.  
def getDelta(distance):
    timeDecimal = float(distance)/18
    hour = math.floor(timeDecimal)
    minute = math.floor((timeDecimal - hour) * 60)
    second = math.floor((((timeDecimal - hour) * 60) - minute)*60)
    return timedelta(hours=hour, minutes=minute, seconds=second)

# This is a function for adjusting the route if any of the packages are
# routed outside of their delivery deadline after the initial route. 
# It happens after each package is inserted into the route in the route
# function. It fist checks if the increase in delivery time would make
# the delivery go outside of its deadline. If not it adds the new delivery
# deadline. If it does go outside the deadlline it starts the nearest insert
# algorithm for that package only and finds an optimal fit for it with the
# contraint that it only choose indicies to insert that put its delivery
# time below its deadline. It then calls itself to make sure adding itself
# to the lower index didn't push any other packages outside their deadlines. 
# It adjusts automatically after each recursion to contrain the end index more
# and more. Forcing the packages with deadlines to insert into lower and lower
# indexes if they keep going outside of their deadlines. 
def adjust(ind, startIndex, truck, delta4, depth, endIndex):
    # Loops from the index of the last insert until the last delivery
    # currently in the route. Minus the last index which is the return
    # to the hub
    while ind < len(truck.route) - 1:

        # Gets the distance between the package at the current index and the package
        # At the last index. It then gets the time it takes to traverse this distance
        # This time is added to the packages current delivery time so that the
        # delivery time is correct after the last insert. It uses this to check
        # if the package will go over its deadline before updating the time and
        # responds accordingly if so. If the location at the route index is the
        # hub there's no package object. So an except block is used to handle
        # the attribute error for package.address and passes hub into getDistance
        # directly. The package object or "HUB" keyword is stored in index 0 of the
        # column array and 1 holds the delivery time. 
        try:
            distance = getDistance(truck.route[ind][0].address, truck.route[ind - 1][0].address)
            delta = getDelta(distance)
        except AttributeError as err:
            distance = getDistance(truck.route[ind][0].address, 'HUB')
            delta = getDelta(distance) 

        try:

            # Checks the updated time after inserting a new object would
            # make the package go over its deadline. 
            if truck.route[ind][1] + delta > truck.route[ind][0].deadline:
                # the below until line 289 is the same as the inner loop of
                # the route function so I won't comment it all. The one difference
                # is that it only loops while the delivery time of the current
                # index it's checking against plus the delta which represents
                # the time it would take to travel from that location to the
                # package address that's trying to be inserted is less then
                # that packages deadline. 
                index = startIndex
                
                cheapest = [-1, None, None, 0]
                
                try:
                    while truck.route[index][1] + delta < truck.route[ind][0].deadline and index < endIndex:

                        if index == startIndex:
                            i = addressMap.lookUp(addressMap, truck.route[index][0])
                        else:
                            i = addressMap.lookUp(addressMap, truck.route[index][0].address)
                        
                        j = addressMap.lookUp(addressMap, truck.route[ind][0].address)

                        if (i == j):
                            if truck.route[ind + 1][1] == truck.route[ind][1]:
                    
                                break
                            cheapest = [0, package, index + 1, 0]
                            
                            cheapest[1].address
                            index = index + 1
                            continue
                        
                        if index+1 == len(truck.route) -1:
                            iP1 = addressMap.lookUp(addressMap, truck.route[index + 1][0])
                        else:
                            iP1 = addressMap.lookUp(addressMap, truck.route[index + 1][0].address)

                        if j == iP1:
                            index = index + 1
                            continue

                        distanceij = 0.0
                        distanceJi1 = 0.0
                        distanceii1 = 0.0

                        if i < j:
                            distanceij = float(distanceArray[j][i])
                            if iP1 < j:
                                distanceJi1 = float(distanceArray[j][iP1])
                            else:    
                                distanceJi1 = float(distanceArray[iP1][j])

                            if iP1 < i:
                                distanceii1 = float(distanceArray[i][iP1])
                            else:
                                distanceii1 = float(distanceArray[iP1][i])
                        else:
                            distanceij = float(distanceArray[i][j])
                            if iP1 < j:
                                distanceJi1 = float(distanceArray[j][iP1])
                            else:    
                                distanceJi1 = float(distanceArray[iP1][j])

                            if iP1 < i:
                                distanceii1 = float(distanceArray[i][iP1])
                            else:
                                distanceii1 = float(distanceArray[iP1][i])

                        deltaij = distanceij + (distanceJi1 - distanceii1)

                        timeDecimal2 = distanceij/18
                        hour2 = math.floor(timeDecimal2)
                        minute2 = math.floor((timeDecimal2 - hour2) * 60)
                        second2 = math.floor((((timeDecimal2 - hour2) * 60) - minute2)*60)

                        if truck.route[index][1] + timedelta(hours=hour2, minutes=minute2, seconds=second2) > truck.route[ind][0].deadline:
                            
                            break
                        
                        if cheapest[0] == - 1 or deltaij < cheapest[0]:
                            
                            cheapest = [deltaij, truck.route[ind][0], index + 1, distanceij]

                        index = index + 1
                except TypeError as err:
                    err
                
                # gets the time delta and then adds it to the previous
                # package in the routes delivery time. This gives the
                # updated delivery time for the package that will be
                # re inserted into the route array. 
                delta = getDelta(cheapest[3])
                time =  delta + truck.route[cheapest[2] - 1][1]
                
                # removes the package from its current index and adds
                # it to the new index
                truck.route.pop(ind)
                truck.route.insert(cheapest[2], [cheapest[1], time])

                # indMove = 1


                checkFromIndex = startIndex + 1
                
                # This checks to see if any of the remaining address past
                # the insert index for the updated package have the same address.
                # if so it inserts them into the index after representing the same
                # delivery time. 
                while checkFromIndex < len(truck.route) - 1:

                    if truck.route[checkFromIndex][0].address == cheapest[1].address:
                        truck.route.insert(cheapest[2] + 1, [truck.route[checkFromIndex][0], truck.route[cheapest[2] - 1][1]])
                        if checkFromIndex > cheapest[2]:
                            truck.route.pop(checkFromIndex + 1)
                        else:
                            truck.route.pop(checkFromIndex)
                        
                    checkFromIndex = checkFromIndex + 1

                updateTimeIndex = cheapest[2]
                
                # This cascades the new delivery time for all packages
                # past the insert index of the package that's being
                # re inserted. It does this using the previous indexes
                # delivery time and then adding the time it takes to
                # travel from that address to the address at the current
                # index.
                while updateTimeIndex < len(truck.route) - 1:

                    try:
                        distance = getDistance(truck.route[updateTimeIndex][0].address, truck.route[updateTimeIndex - 1][0].address)
                        delta = getDelta(distance)
                    except AttributeError as err:
                        distance = getDistance(truck.route[updateTimeIndex][0].address, 'HUB')
                        delta = getDelta(distance)
                    truck.route[updateTimeIndex][1] = truck.route[updateTimeIndex - 1][1] + delta

                    updateTimeIndex = updateTimeIndex + 1

                # A package can't be inserted before the start index. This if block 
                # insure the end index never goes to low. 
                if endIndex == startIndex + 2:
                    adjust(startIndex + 1, startIndex, truck, delta, depth + 1, endIndex)
                    break

                # Recusivly called the adjust function to make sure the new update didn't
                # push any other packages past their deadline. It decreases the end index every
                # recursion. This forces the insert of a package with a deadline to go further
                # and further back in the route if if the adjustments keep pushing new packages
                # out of their deadlines. 
                adjust(startIndex + 1, startIndex, truck, delta, depth + 1, endIndex - 1)
                break
        
        # If the deadline is "EOD" and not a number a type error is thrown.
        # in this case no re adjustment needs to be considered and the program
        # skips to this except block. The except block updates the delivery
        # time of the 'EOD' package in the same way as the other updates on previous
        # lines
        except TypeError as err:
            try:
                distance = getDistance(truck.route[ind][0].address, truck.route[ind - 1][0].address)
                delta = getDelta(distance)
            except AttributeError as err:
                distance = getDistance(truck.route[ind][0].address, 'HUB')
                delta = getDelta(distance) 
            truck.route[ind][1] = truck.route[ind - 1][1] + delta
            ind = ind + 1 
            continue
        
        # This is the delivery time update block for packages that have a deadline
        # but the new delivery time wouldn't be over the deadline. In this case.
        # It's what happens if the if block on line 203 doesn't throw an error and
        # also evaluates to false. 
        try:
            distance = getDistance(truck.route[ind][0].address, truck.route[ind - 1][0].address)
            delta = getDelta(distance)
        except AttributeError as err:
            distance = getDistance(truck.route[ind][0].address, 'HUB')
            delta = getDelta(distance) 
        truck.route[ind][1] = truck.route[ind - 1][1] + delta
        ind = ind + 1 
    
    # i = startIndex + 1 

# Function for getting the distance between two address inputs. 
# it gets the row/column for the distance array by calling the 
# addressMap function and then gets the distance from distanceArray
# at rowx and columny. The distance array column is one sided so
# indicies with lower value have to be put into the column index.
def getDistance(address1, address2):
    index1 = addressMap.lookUp(addressMap, address1)
    index2 = addressMap.lookUp(addressMap, address2)

    if index1 < index2:
        return distanceArray[index2][index1]
    
    return distanceArray[index1][index2]

# This is the primary routing algorithm. Using the nearest insert method
# described in prompt f1 and f3. It gets the best insert for all unrouted
# packages at all possible indexes and inserts into the appropriate index. 
def route(truck, startIndex):
    index = startIndex

    # Loops through all packages assigned to a truck.
    for outerLoop in truck.packages:

        # Temporary array representing the cheapest or 'best' insert.
        # it holds the distance for that given insert, the package 
        # and the index of that given insert. The package and index
        # with the lowest distance overide the defualt values of this
        # temporary array.
        cheapest = [-1, None, None, 0]

        # second loop through all packages in a truck. This second loop
        # through all packages only inserts one package. Since every
        # package needs to be inserted the nested loop is required so that
        # every package can be inserted. 
        for package in truck.packages:

            # Whenver a packaes is put into the route it gets marked
            # as routed and so doesn't need to be checked again.
            # this if block insures that the while loop doesn't excecute
            # if that's the case. 
            if package.status == 'Routed':

                continue

            # This is the loop that actually checks for the best insert.
            # it loops through every package/location already routed and
            # checks it against the current package. If at any time the
            # current insert is the best so far it will be put into the
            # cheapest array.
            while index < len(truck.route) - 1:

                # If the index is the start index it's the hub and so has no address
                # property. In that case i will get set to the row/column corresponding
                # to the hub. If not i will be set to the row/column of whatever address
                # is assigned to the package
                if index == startIndex:
                    i = addressMap.lookUp(addressMap, truck.route[index][0])
                else:
                    i = addressMap.lookUp(addressMap, truck.route[index][0].address)
                
                # j represents the row/column index for the distanceArray
                # of the current unrouted package. 
                j = addressMap.lookUp(addressMap, package.address)
                
                # if i == j then the package has the same address as the
                # already routed package. This means they should be next
                # to eachother in the route. The cheapest array is set
                # to this package at this index and given a value of zero
                # representing no distance needs to be travled. The rest
                # of the function doesn't need to excecute in this case
                # and so it continues.
                if (i == j):
                  
                    cheapest = [0, package, index + 1, 0]

                    cheapest[1].address
                    index = index + 1
                    continue

                # iP1 repsresents the row/column index for the distanceArray
                # of the routed object at the index one above the routed object 
                # currently being checked. Getting this distance is a requirement
                # of the closest insert method. Like wise with the i variable the
                # if block is to check if it's the HUB or not. Since the last
                # index of the route is always the return to the hub. 
                if index+1 == len(truck.route) -1:
                    iP1 = addressMap.lookUp(addressMap, truck.route[index + 1][0])
                else:
                    iP1 = addressMap.lookUp(addressMap, truck.route[index + 1][0].address)

                # Variables for distance between i and j, j and i + 1, and i and i plus one.
                # These distances are all requirements for calculating deltaij which is
                # the representation of the 'cost' of the given insert. 
                distanceij = 0.0
                distanceJi1 = 0.0
                distanceii1 = 0.0

                # The below if blocks get the actual distance for
                # distanceij distanceji1 and distanceii1. The if
                # blocks again are because the distance array is one
                # sided and so the index with the lowest value needs
                # to be passed to the column index of the 2d array and
                # not the row index
                if i < j:
                    distanceij = float(distanceArray[j][i])
                    if iP1 < j:
                        distanceJi1 = float(distanceArray[j][iP1])
                    else:    
                        distanceJi1 = float(distanceArray[iP1][j])

                    if iP1 < i:
                        distanceii1 = float(distanceArray[i][iP1])
                    else:
                        distanceii1 = float(distanceArray[iP1][i])
                else:
                    distanceij = float(distanceArray[i][j])
                    if iP1 < j:
                        distanceJi1 = float(distanceArray[j][iP1])
                    else:    
                        distanceJi1 = float(distanceArray[iP1][j])

                    if iP1 < i:
                        distanceii1 = float(distanceArray[i][iP1])
                    else:
                        distanceii1 = float(distanceArray[iP1][i])

                # Calculates deltaij
                deltaij = distanceij + (distanceJi1 - distanceii1)

                # If the o index of cheapest, which is the cost,
                # is still negitive one that means no inserts have
                # been made. In this case or if the deltaij of the 
                # current package and route index combo is lower
                # then the current cheapest insert. The cheapest
                # array will be updated to represent this insert. 
                if cheapest[0] == - 1 or deltaij < cheapest[0]:

                    # The insert will only be done if the package
                    # doesn't have a delivery deadline or if the
                    # delivery of the routed package the new package
                    # will be inserted at is less then the new packages
                    # deadline
                    try:
                        if truck.route[index][1] <= package.deadline:
                            cheapest = [deltaij, package, index + 1, distanceij]

                    except:
                        if package.deadline == 'EOD':
                            cheapest = [deltaij, package, index + 1, distanceij]

                index = index + 1

            index = startIndex

        # If the cheapest array has been updated then an insert is required
        # in this case it sets the newly inserted package status to routed.
        # if the distance of the cheapest insert isn't zero it 
        # finds the delivery time and then calls the adjust function which
        # both cacades updated delivery times to all the packages and
        # checks if any updated delivery time makes any package go outside
        # its deadline. If it is zero then that means it matches the address
        # of the index it's being inserted into. In this case the delivery
        # time is set equal to the delivery time at the previous index since
        # it's the same address. No cascade is done since no change in delivery
        # times for any packages happens in this case. 
        if cheapest[0] != - 1:
            cheapest[1].status = 'Routed'
            if cheapest[3] != 0:
                delta = getDelta(cheapest[3])
                time = delta + truck.route[cheapest[2] - 1][1]
                truck.route.insert(cheapest[2], [cheapest[1], time])

                adjust(startIndex + 1, startIndex, truck, delta, 0, len(truck1.route) - 1)

            else:
                truck.route.insert(cheapest[2], [cheapest[1], truck.route[cheapest[2] - 1][1]])

        cheapest = [-1, None, None, 0]

    returnDistance = getDistance(truck.route[len(truck.route) - 2][0].address, 'HUB')#distanceArray[lastAddress][0]
    delta = getDelta(returnDistance)
    time = delta + truck.route[len(truck.route) - 2][1]
    truck.route[len(truck.route)-1][1] = time 

# Calls the route function for truck1 and truck2
route(truck1, 0)
route(truck2, 0)

# This array will hold packages that were delayed and that had a deadline
# They will take priority over packages that were delayed that didn't
# have a deadline
delayedWithDeadline = []

# Appends all delayed packages with deadlines to the delayedWithDeadline array
for array in packageHash.table:
    for package in array:
        if package.status == 'Delayed':
            if package.deadline != 'EOD':
                delayedWithDeadline.append(package)


# This was a function that sorted the delayedWithDeadline array
# by earliest deadline. In this scenario all the deadlines are the
# same 10:30. So I commented it out cause it didn't have any purpose.
# in another scenario where there was a wider range of deadlines it
# may be beneficial to sort by earliest deadline. 

if len(delayedWithDeadline) != 0:
    earliestDeadline = []
    i = 0
    j = 0
    while i < len(delayedWithDeadline):
        while j < len(delayedWithDeadline):
            if delayedWithDeadline[j].deadline < delayedWithDeadline[i].deadline:
                delayedWithDeadline.insert(i, delayedWithDeadline[j])
                delayedWithDeadline.pop(j + 1)
            j = j + 1

        i = i + 1
        j = i


needsReroute = False   

# This if ealse block checks to see which of the two trucks would have
# finished their initial 16 packages earliest. The fastest truck
# gets the earlyTruck variable and is used as the first truck to go
# back to the hub to get the delayed packages. 
if truck1.route[len(truck1.route) - 1][1] < truck2.route[len(truck2.route) - 1][1]:
    earlyTruck = truck1
    latterTruck = truck2

else:

    earlyTruck = truck2 
    latterTruck = truck1  
    
tempArray = []

# This function checks to see if any of the delayedWithDeadline packages
# have deadlines that are before the earlyTruck finishes its initial
# route. If so needs reRoute is set to true. A few blocks down if it's
# set to true the route function is called again with a restriction
# on the start index being the index of the first package who's delivery
# time is past 9:05. The truck will then go back to the hub at 9:05
# to pickup the delayed packages that had dealines and the route past
# that index will be adjusted to work in the new delayed packages after
# 9:05. All delayed packages that have deadlines arrive at 9:05 in this
# scenario so that value is hard coded. In a more general application
# This value would be parsed out of each packaged and included in the
# delayedWithDeadline package automate the reroute processes and return
# times based on those values. 
for index, package in enumerate(delayedWithDeadline):
    
    # This bit of code takes into account differing deadlines
    # it was made to check the deadline of the package with the
    # earliest deadline against the return to hub time of the origional
    # route. This is what the index == 0 if block is for. The first
    # index checks agains hub and so 'HUB' and not package.address needs
    # to be passed to getDistance. After that it checks for the delivery
    # time of the delayedWithDeadline package at the current index to 
    # that of the delayedWithDeadline package at the last index had
    # it not gone over its deadline. If chaining the delayed packages
    # with deadlines after the initial return to hub in this way would
    # result in any of the packages being delivered outside their deadline
    # a reroute is needed. If This happens needs reroute is set true and
    # the loop is exited out of. The re route is then done after 9:05 delivery
    # as described above.  
    if index == 0:

        distance = getDistance(package.address, 'HUB')
        delta = getDelta(distance)
        time = delta + earlyTruck.route[len(earlyTruck.route) - 1][1]
        if time > delayedWithDeadline[0].deadline:
            needsReroute = True
            break
        tempArray.append([package, time])
    else:

        distance = getDistance(package.address, tempArray[index - 1][0].address)
        delta = getDelta(distance)
        time = delta + tempArray[index - 1][1]
        if time > delayedWithDeadline[0].deadline:
            needsReroute = True
            break
        tempArray.append([package, time])

# This is the block that does the reroute on the earlyTruck if needsReroute
# is set to true. 
if needsReroute == True:

    # Sets the initial startIndex for the reroute to None for now until
    # it's determined. Also sets the packages to be added-newPackages-
    # to all the packages in delayedWithDeadline
    startIndex = None
    newPackages = delayedWithDeadline

    # Loops through all the packages in the route of the early truck
    # and finds the first one with a delivery time after 9:05
    for index, array in enumerate(earlyTruck.route):
        if array[1] > timedelta(hours=9, minutes=5, seconds=0):

            # Get distance between the first address delivered after 9:05
            # and the hub
            distance = getDistance(array[0].address, 'HUB')

            # Get time to travel that distance
            delta = getDelta(distance)
            time = array[1] + delta
            
            # Insert a new trip back to the hub in the route at the
            # index after the index of the first package delivered after
            # 9:05
            earlyTruck.route.insert(index + 1, ['HUB', time])

            i = index + 2

            # Cascade delivery times for this one insert of the trip back
            # the hub using the adjust function. This starts at index plus
            # 2 since index plus 1 is the return to hub that has already
            # had its time calculated.
            adjust(i, i - 1, earlyTruck, delta, 0, len(truck1.route) - 1)
            
            # Start index for the new call to route will be the index
            # of the return to hub. So I set startIndex to that index
            # here and then break out of the loop that checks for
            # the packages delivered after 9:05
            startIndex = index + 1
            break
        
    # Add all the new packages to the earlyTruck packages. These
    # won't have a routed status and so will get re worked into
    # the route when route is called. 


    for package in newPackages:
        earlyTruck.addPackage(package)

    # Call route on the earlyTruck with the return to hub
    # as the start index. This ensures none of the packages that
    # were only available after 9:05 and the return to the hub
    # will be routed before the return to the hub. 
    route(earlyTruck, startIndex)
 

# Check again which truck has the earlist return time after the re route
# of the previous earlyTruck. This truck is set to earlyTruck and is
# set to return back to the hub after 10:20 when the correct address
# for package 9 is added. This truck will pick up package 9 and all
# remaining packages at this time and a reroute after the index for the
# return to hub will be called. 
if truck1.route[len(truck1.route) - 1][1] < truck2.route[len(truck2.route) - 1][1]:
    earlyTruck = truck1
    latterTruck = truck2
else:
    earlyTruck = truck2 
    latterTruck = truck1 

waitTell = timedelta(hours=10, minutes=20, seconds=0)
earlyTruckReturnTime = earlyTruck.route[len(earlyTruck.route) - 1][1]

# If the return time of the earlyTruck is before 10:20 a departure time
# from the hub at 10:20 is set. This simulates the truck waiting at
# the hub until the package address is updated
if earlyTruckReturnTime < waitTell:
    earlyTruck.route.append(['HUB', waitTell])

# Adds all remaining packages to the earlyTruck. If the package
# address was 300 state st and had the delayed status then it's package
# 9 and is set to the updated delivery address of 410 S state st before
# being added to the earlyTruck 
for array in packageHash.table:
    for package in array:
        if package.status == 'Delayed':
            if package.address == '300 State St':
                package.address = '410 S State St'
            earlyTruck.addPackage(package)
        if 'At hub' in package.status:
            earlyTruck.addPackage(package)

# The truck needs to have a new last index representing the final
# return time to the hub after all remaining packages have been delivered.
# This append statement does that. 
earlyTruck.route.append(['HUB', None])

# call route on early truck with the start index beind the second
# To last index of the route array. This is the departure from the
# hub at 10:20 if it had to wait and the return/departure to the hub
# if it finished after 10:20 after this call the final route for
# both trucks is set.
route(earlyTruck, len(earlyTruck.route) - 2)   


miles = 0
index = 1

# Creates a new miles input for the first index of the route.
# The loop below it sets this and calculates it for every index.
# This keeps track of how many miles have been driven at each
# delivery point. 
truck1.route[0].append(miles)
truck2.route[0].append(miles)
while index < len(truck1.route):

    timeMilliSeconds = int((truck1.route[index][1] - truck1.route[index-1][1]).total_seconds())
    
    distance = ((timeMilliSeconds)/3600)*18
    miles = miles + round(distance, 1)
    truck1.route[index].append(round(miles, 1))
    index = index + 1

    try:
        truck1.route[index - 1][0].status = "At Hub"
    except AttributeError as err:
        continue


# Adds the total miles driven to truck1s total miles driven variable. 
# it gets this from the miles driven of the last index in its route. 
truck1.totalMilesDriven = truck1.route[len(truck1.route) - 1][2]


# Same as above but for truck2
index = 1
miles = 0
while index < len(truck2.route):
    # array[2] = miles 
    timeSeconds = int((truck2.route[index][1] - truck2.route[index-1][1]).total_seconds())
    
    distance = (timeSeconds/3600)*18
    miles = miles + round(distance, 1)
    truck2.route[index].append(round(miles, 1))
    index = index + 1

    try:
        truck2.route[index - 1][0].status = "At Hub"
    except AttributeError as err:
        continue

truck2.totalMilesDriven = truck2.route[len(truck2.route) - 1][2]

# I created three programs that can be run from the command line.
# these are to check the delivery status of a single package by id,
# check delivery times of all packages at the end of the day, and
# check the status of all packages at a specific time of day.
# program1 below is the first one. Gets one package status by id 
# and time of day. Tehse three programs fulfil all of prompt D.
def program1():
    # Gets an id input from the user. If invalid a message is displayed
    # indicating valid inputs and the program is called again so that
    # the user may input a valid id
    id = input("pick an id between 1 and 40: ")
    try:
        if int(id) < 1 or int(id) > 40:
            print("Invalid id. Choose a number between 1 and 40")
            program1()
            return
    except ValueError as err:
        print("Invalid id. Choose a number between 1 and 40")
        program1()
        return
    
    # Same as above but for the time of day. 
    time = input("pick a time in the formate h:m:s ")
    timeComponents = time.split(':')
    try:
        delta = timedelta(hours= int(timeComponents[0]), minutes=int(timeComponents[1]), seconds=int(timeComponents[2]))
    except:
        print("Invalid input. All inputs must be integers and in the format h:m:s")
        program1()
        return

    route = 0
    inputPackage = None
    deliveryTime = None
    truck = None
    lastHubTime = None

    # This loops through each truck route and checks for the package
    # id provided. route = 0 loops through truck1 route = 1 loops through
    # truck2. 
    while route <= 1:

        if route == 0:
            for package in truck1.route:
                try:
                    
                    # Once a match is found the
                    # package object, delivery time
                    # and truck name are saved to variables
                    # to be printed
                    if package[0].id == id:
                        inputPackage = package[0]
                        deliveryTime = package[1]
                        truck = truck1.name
                        break
                    
                except AttributeError as err:
                    # When the route index is a return
                    # to hub it updates a variable
                    # that represents the last time
                    # at the hub. This helps in determining
                    # the delivery status at the given 
                    # input time.
                    lastHubTime = package[1]
                  
                    continue
       
        if route == 1:

                for package in truck2.route:
                    try:
                        # Once a match is found the
                        # package object, delivery time
                        # and truck name are saved to variables
                        # to be printed                       
                        if package[0].id == id:
                            inputPackage = package[0]
                            deliveryTime = package[1]
                            truck = truck2.name
                            break
                        
                    except AttributeError as err:
                        # When the route index is a return
                        # to hub it updates a variable
                        # that represents the last time
                        # at the hub. This helps in determining
                        # the delivery status at the given 
                        # input time.
                        lastHubTime = package[1]
                        continue
        # once a package has been assigned to input package there's
        # no need to keep looping. This checks if it's still none
        # and breaks out of the loop if not. 
        if inputPackage != None:
            break
        route = route + 1

    # if delivery time of the package is less then the input time, which
    # is the varialbe delta, the package delivered status is printed with
    # the delivery time. If not one of two things in the below if block
    # happens
    if deliveryTime > delta:
        # If the last time at the hub is greater then the time input
        # this means that the packages must still be at the hub and
        # not en route. And so package at hub is printed. if delta
        # is after the last hub time that means that the time that
        # was input was after the return to the hub or that the package
        # was delivered in the first route. Meaning that the last time at
        # hub is the start time of 8:00. In either case the package has been
        # loaded on the truck and is en route. Once the route is determined
        # There's no need to pack any more packages on the truck then would
        # be delivered before returning. So any packages not delivered
        # before return to the hub are left at the hub. 
        if lastHubTime > delta:
            print("Package At Hub \n")
            return
        print("Package en Route with {} \n".format(truck))
        return
    
    print("Package Delivered at {}".format(deliveryTime) + " by " + truck + "\n")


# Get's delivery time of all packages at end of day
def program2():
    print('\n')
    print("Truck1 packages")

    # Loops through route of truck1 and prints all delivery times
    for package in truck1.route:
        try:
            # print(package[0].address + " ID " + '{}'.format(package[0].id)+ ': ' + '{}'.format(package[1]))
            print(package[0].address + " " + package[0].city + ", "  + package[0].zipCode + ", ID " + package[0].id + ", Deadline {}".format(package[0].deadline)  + ", Weight " + package[0].weight + ", Delivered at {}".format(package[1]))
        except AttributeError as err:
            continue

    print('\n')
    print("Truck2 packages")
    
    # Loops through route of truck2 and prints all delivery times
    for package in truck2.route:
        try:
            # print(package[0].address + " ID " + '{}'.format(package[0].id) + ': ' + '{}'.format(package[1]))
            print(package[0].address + " " + package[0].city + ", "  + package[0].zipCode + ", ID " + package[0].id + ", Deadline {}".format(package[0].deadline)  + ", Weight " + package[0].weight + ", Delivered at {}".format(package[1]))
        except AttributeError as err:
            continue
    print('\n')


# Get's delivery status of all packages at a given time of day
def program3():

    # Same as the time input for program 1
    time = input("pick a time in the formate h:m:s ")
    timeComponents = time.split(':')
    try:
        delta = timedelta(hours= int(timeComponents[0]), minutes=int(timeComponents[1]), seconds=int(timeComponents[2]))
    except:
        print("Invalid input. All inputs must be integers and in the format h:m:s")
        program3()
        return

    route = 0
    lastHubTime = None
    
    # The basic structure of this loop is similar to that of the loop
    # in program 1. The difference is that instead of breaking out of the
    # loop when a package id is found and only printing that id it instead
    # prints the status of each package at each iteration of the loop.
    # it uses the same logic as program1 to determine if the package is
    # at hub en route or delivered. Prints all for truck1 first and then
    # truck2. There's a clear break in the formatting between both trucks
    # so it's easty to tell which packages are in which trucks. Also a prompt
    # stating the truck is given before each truck.route loop
    while route <= 1:

        if route == 0:
            print("Truck1 package statuses at {}".format(delta))
            for package in truck1.route:
                try:
                    
                    if package[0].id:
                        if package[1] < delta:
                            package[0].status = "Delivered at: {}".format(package[1])
                            print(package[0].address + " " + package[0].city + ", "  + package[0].zipCode + ", ID " + package[0].id + ", Deadline {}".format(package[0].deadline)  + ", Weight " + package[0].weight)
                            print('Status: ' + package[0].status)
                            print("Miles Driven: {}".format(package[2]) + '\n')
                        else:
                            if delta < lastHubTime:

                                package[0].status = "At Hub" 
                                print(package[0].address + " " + package[0].city + ", "  + package[0].zipCode + ", ID " + package[0].id + ", Deadline {}".format(package[0].deadline)  + ", Weight " + package[0].weight)
                                # print(package[0].address + " ID " + package[0].id)
                                print('Status: ' + package[0].status + '\n')
                                continue
                            package[0].status = "En Route"
                            # print(package[0].address + " ID " + package[0].id)
                            print(package[0].address + " " + package[0].city + ", "  + package[0].zipCode + ", ID " + package[0].id + ", Deadline {}".format(package[0].deadline)  + ", Weight " + package[0].weight)
                            print('Status: ' + package[0].status + '\n')
                        
                    
                except AttributeError as err:
                    lastHubTime = package[1]
                  
       
        if route == 1:
            print("Truck2 package statuses at {}".format(delta))
            for package in truck2.route:
                try:
                    
                    if package[0].id:
                        if package[1] < delta:
                            package[0].status = "Delivered at: {}".format(package[1])
                            # print(package[0].address + " ID " + package[0].id)
                            print(package[0].address + " " + package[0].city + ", "  + package[0].zipCode + ", ID " + package[0].id + ", Deadline {}".format(package[0].deadline)  + ", Weight " + package[0].weight)
                            print('Status: ' + package[0].status)
                            print("Miles Driven: {}".format(package[2]) + '\n')
                        else:
                            if delta < lastHubTime:
                                package[0].status = "At Hub" 
                                # print(package[0].address + " ID " + package[0].id)
                                print(package[0].address + " " + package[0].city + ", "  + package[0].zipCode + ", ID " + package[0].id + ", Deadline {}".format(package[0].deadline)  + ", Weight " + package[0].weight)
                                print('Status: ' + package[0].status + '\n')
                                continue
                            package[0].status = "En Route"
                            # print(package[0].address + " ID " + package[0].id)
                            print(package[0].address + " " + package[0].city + ", "  + package[0].zipCode + ", ID " + package[0].id + ", Deadline {}".format(package[0].deadline)  + ", Weight " + package[0].weight)
                            print('Status: ' + package[0].status + '\n')
                  
                    
                except AttributeError as err:
                    lastHubTime = package[1]

        print('\n')

        route = route + 1

print("Choose a program using the numbers listed below")
print("1: Find delivery status of individual package by package id and time of day")
print("2: Show all package delivery times")
print("3: Show package status of all packages at a given time of day for both trucks")
validProgram = False

# This loops until the user inputs a valid number for which program to
# choose. Once a valid number-being 1 2 or 3-is selected. That particular
# program is called. 
while validProgram == False:

    program = input()

    if (program == "1"):
        print("program 1 chosen")
        program1()
        validProgram = True

    elif (program == "2"):
        print("program 2 chosen")
        program2()
        validProgram = True

    elif (program == "3"):
        print("program 3 chosen")
        program3()
        validProgram = True

    else:
        print("Invalid input. Program must be 1 or 2")   

# After any of the programs run the total miles of both trucks
# and combined miles is printed. 
print("Truck1 total miles {} ".format(truck1.totalMilesDriven))
print("Truck2 total miles {} ".format(truck2.totalMilesDriven))
print("Truck3 total miles 0" )
print("Total miles for all trucks {} ".format(truck1.totalMilesDriven + truck2.totalMilesDriven))




    



    





























