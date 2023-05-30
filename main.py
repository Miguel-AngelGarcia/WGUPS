'''
Name: Miguel-Angel Garcia
StudentID: 001347769
'''

import csv, datetime
import Truck #class we made
from HashTable import HashTable
from Package import Package


header = "[PackageID][DeliveryAddress][City][State][ZipCode][DeliveryDeadline][PackageWeight][SpecialNotes]"+\
        "[DeliveryStatus][HubDepartureTime][DeliveryTime][DeliverTruck]"

#added encoding='utf-8-sig' to get rid of '\ufeff0' error we were getting
#turns CSV into the Distance List
with open("WGUPS_Distance_Table.csv", "r", encoding='utf-8-sig') as distanceCSV:
    wgupsDistance = csv.reader(distanceCSV)
    wgupsDistance = list(wgupsDistance)

#turns CSV into the Address List
with open("WGUPS_Address_File.csv", "r", encoding='utf-8-sig') as addressCSV:
    wgupsAddress = csv.reader(addressCSV)
    wgupsAddress = list(wgupsAddress)

'''
time checking function
will take the number of colons counted, parse the time, and return it
This helps error check for HH:MM times if use doesnt enter HH:MM:SS
'''
def colonsTimeCheck(countedColons, userTimeEntered):
    timeToBeConverted = None

    if (countedColons == 2):
        (hour, minu, sec) = userTimeEntered.split(":")
        timeToBeConverted = datetime.timedelta(hours=int(hour), minutes=int(minu), seconds=int(sec))
    elif (countedColons == 1):
        (hour, minu) = userTimeEntered.split(":")
        timeToBeConverted = datetime.timedelta(hours=int(hour), minutes=int(minu), seconds=int(0))

    else:
        timeToBeConverted = 'N/A'

    return timeToBeConverted

# will take packages csv and will load each package into the hashtable
def loadPackageInfo(fileName):
    with open(fileName, "r") as csv_file:
        packageData = csv.reader(csv_file)
        #skipping header
        next(packageData, None)

        findingNumPackages = 0

        for package in packageData:
            pID = package[0]
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pNotes = package[7] #hash table for this?
            pStatus = 'At hub' #initially, all packages are at the hub

            #creating packageObject, only need 9. last 2 will be created by class
            loadedPackage = Package(pID, pAddress, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus)

            packageHashTable.insert(pID, loadedPackage)

            #counter for number of packages
            findingNumPackages += 1

        return findingNumPackages

#creates hash table
packageHashTable = HashTable()

totalPackages = 0


#will load package information into table
totalPackages = loadPackageInfo("WGUPS_Package_File.csv")

#will find distances between current location and package
def findDistanceBetween(xValue, yValue):
    intX = int(xValue) #needed to convert here. we were getting 'None' as a return value
    intY = int(yValue)
    #Will find row first, then value within row. Will go Y, then X instead of X,Y
    distanceBetween = wgupsDistance[intY][intX]

    '''
    got error 'could not convert string to float: '
    figured because csv map is mirror, we would try flipping X&Y it may work
    it works
    '''
    if distanceBetween == '':
        distanceBetween = wgupsDistance[xValue][yValue]

    return float(distanceBetween)

#will take address and look it up
def getAddress(address):
    for addressRow in wgupsAddress:
         if address in addressRow[2]:
            #will return address index. think of it as he addressID
            return int(addressRow[0])

#this is our delivery algorithm
def deliverAlgo(truck):
    #create list of all non-delivered packages
    nonDeliveredPackages = []

    #takes a truck's packages and gets their info via Package ID
    for packageID in truck.packages:
        package = packageHashTable.find(packageID)
        nonDeliveredPackages.append(package)

    #will clear packages on truck. Will add them back in delivery order
    truck.packages.clear()

    numNonDeliveredPackages = len(nonDeliveredPackages)
    while numNonDeliveredPackages > 0:
        #sets next package address as 1st package in numNonDeliveredPackages[]
        nextAddressDistance = findDistanceBetween(getAddress(truck.address), getAddress(nonDeliveredPackages[0].address))
        nextPackage = None

        #for each package remaining, will checks its distance between current location and package address
        for currPackage in nonDeliveredPackages:
            currStopToNextAddress = findDistanceBetween(getAddress(truck.address), getAddress(currPackage.address))

            #adds hub departure time
            if currPackage.hubDepartureTime == 'N/A':
                currPackage.addDepartureTime(truck.departTime)

            #assigns delivery truck to package
            if currPackage.deliveryTruck == 'N/A':
                currPackage.addDeliveryTruck(truck.name)

            #if distance to checked package is less than current lowest distance, will assign it as next
            if currStopToNextAddress <= nextAddressDistance:
                nextAddressDistance = currStopToNextAddress
                nextPackage = currPackage

        #will append nearest package in order, at each stop
        truck.packages.append(nextPackage.packageID)

        #removes the package from remaining. Think of it as crossing out a "to-do" item
        nonDeliveredPackages.remove(nextPackage)

        #adds mileage
        truck.mileage += nextAddressDistance

        #sets address at delivered package address
        truck.address = nextPackage.address

        #time
        nextPackage.departureTime = truck.time
        # 18 is the 18mph the truck drives
        truck.time += datetime.timedelta(hours=((float(nextAddressDistance)) / 18))
        numNonDeliveredPackages -= 1

        #time the package is delivered, is the time the truck leaves after arriving
        nextPackage.deliveryTime = truck.time
        #print("delivering package: ", nextPackage.packageID, " departed at ", nextPackage.departureTime, " delivered at ", nextPackage.deliveryTime)

    #add the milage and time from last delivery address back to delivery Hub.
    goingBackToHub = findDistanceBetween(getAddress(truck.address), 0)
    truck.mileage += goingBackToHub
    truck.time += datetime.timedelta(hours=((float(goingBackToHub)) / 18))
    truck.address = "4001 South 700 East"
    truck.returnTime = truck.time


# Create truck object truck1
#calling truck class, and then calling Truck to initialize with info
truck1 = Truck.Truck(16, 18, None, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8), "Truck 1")

truck2 = Truck.Truck(16, 18, None, [2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 18, 25, 28, 32, 36, 38], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=9,  minutes=15), "Truck 2")

#check to make sure at least truck1 or truck2 return to the hub before truck3 leaves
#like, if time >10:30, load correct address for package 9, then depart at 10:30
truck3 = Truck.Truck(16, 18, None, [9, 17, 21, 22, 23, 24, 26, 27, 33, 35, 39], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=30), "Truck 3")
deliverAlgo(truck1)
deliverAlgo(truck2)
deliverAlgo(truck3)

if __name__ == '__main__':
    print("[------------WGUPS - Western Governors University Parcel Service------------]")
    print("[------------------------Delivery Information Systems-----------------------]")
    print("[------------Milage for given packages delivered is: ", end='')
    totalMilage = float(truck1.mileage) + float(truck2.mileage) + float(truck3.mileage)
    refinedTotalMilage = round(totalMilage, 2)
    print(float(f'{refinedTotalMilage:.{5}g}'), "miles------------]")
    userSelection = None

    while (userSelection != 0):
        # input menu for user
        print('')
        print("To view delivery data for all packages at a certain point in time, Enter 1")
        print("To view delivery data for a single package at a certain point in time, Enter 2")
        print("To view delivery data for all packages, Enter 3")
        print("To exit, Enter 0")
        userSelection = int(input("Selection -> "))

        if userSelection == 1:
            try:
                timeSelection = input("Please enter a desired time in HH:MM:SS format - ")

                countColon = timeSelection.count(":")

                convert_time = colonsTimeCheck(countColon, timeSelection)

                if convert_time == 'N/A':
                    print("\nPlease enter a valid time -> HH:MM:SS")
                    continue

                print(header)
                #packageID starts at 1, not 0.
                for packageID in range(1, totalPackages + 1):
                    package = packageHashTable.find(packageID)
                    package.statusUpdate(convert_time)
                    print(package)

                mileage1 = float(truck1.inAction(convert_time))
                mileage2 = float(truck2.inAction(convert_time))
                mileage3 = float(truck3.inAction(convert_time))
                mileageAtTime = mileage1 + mileage2 + mileage3
                refinedMileageAtTime = round(mileageAtTime, 2)
                print("Total mileage of all trucks at", convert_time,"->", refinedMileageAtTime)

            except ValueError:
                print("\nPlease enter time in a valid format - HH:MM:SS")
                continue

            except TypeError:
                print("\nPlease enter time in a valid format - HH:MM:SS")
                continue

        if userSelection == 2:
            try:
                packageSelection = int(input("Please enter a packageID -> "))

            except ValueError:
                print("\nPlease enter a valid Package ID")
                continue

            try:
                timeSelection = input("Please enter a desired time in HH:MM:SS format - ")
                countColon = timeSelection.count(":")
                convert_time = colonsTimeCheck(countColon, timeSelection)

                if convert_time == 'N/A':
                    print("\nPlease enter a valid time -> HH:MM:SS")
                    continue

                package = packageHashTable.find(packageSelection)

                if package is None:
                    print("Package ID not found. Please select a valid Package ID")
                    continue

                package.statusUpdate(convert_time)
                print(header)
                print(package)
                print("Status for Package ID:", package.packageID, "at time:", convert_time)

            except ValueError:
                print("\nPlease enter time in a valid format - HH:MM:SS")
                continue

        if userSelection == 3:

            try:
                #packageID starts at 1, not 0.
                print(header)
                for packageID in range(1, totalPackages + 1):
                    package = packageHashTable.find(packageID)
                    convert_time = datetime.timedelta(hours=int(19), minutes=int(0), seconds=int(0))
                    package.statusUpdate(convert_time)
                    print(package)

            except ValueError:
                print("\nThis is weird. Please try again.")
                continue

        elif userSelection == 0:
            break

        elif userSelection > 3:
            print("\nPlease select a valid choice")

        elif TypeError:
            print("\nPlease select a valid choice")

    print("\nThank you, have a great day!")