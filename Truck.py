#Python truck class
import datetime


class Truck:
    def __init__(self, capacity, speed, load, packages, mileage, address, departTime, truckName):
        self.capacity = capacity #how many packages a truck can have
        self.speed = speed #how fast truck travels
        self.load = load
        self.packages = packages #packages loaded
        self.mileage = mileage  #milage between start and end location
        self.address = address  #current address
        self.departTime = departTime #time is leaves
        self.time = departTime #imagine the truck has a clock inside
        self.returnTime = 'N/A'
        self.name = truckName

    #returns a human-readable, or informal, string representation of an object.
    def __str__(self):
        return "%s, $s, $s, $s, $s, $s, $s" %\
            (self.capacity, self.speed, self.load, self.packages, self.mileage, self.address, self.departTime)

    '''
    returns milage of a truck at a given point in time
    if truck departs after time to check, it will be considered "driving"
    If driving, it will check given time to check against return time. 
    If return time is before given time, it will return milage driven
    If return time is after given time, it will calculate miles driven
    '''
    def inAction(self, givenTime):
        driving = givenTime > self.departTime
        mileageToReturn = self.mileage
        if(driving):

            if self.returnTime < givenTime:
                return mileageToReturn

            else: #driven time = time after given time
                drivenTime = givenTime.seconds - self.departTime.seconds
                miles = 18 * (drivenTime/3600) #3600 to convert seconds to MPH
                mileageToReturn = miles
        else:
            mileageToReturn = 0


        return mileageToReturn
        #time_driven = datetime.timedelta(hours)
        #mialge += datetime.timedelta(hours=((float(nextAddressDistance)) / 18))