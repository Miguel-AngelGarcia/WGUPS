#Package class

class Package:
    def __init__(self, packageID, address, city, state, zipcode, deadline, weight, notes, status):
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.hubDepartureTime = 'N/A'
        self.deliveryTime = None #None will work for statuesUpdate() below
        self.deliveryTruck = 'N/A'

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % \
               (self.packageID, self.address, self.city, self.state, self.zipcode, self.deadline,
                self.weight, self.notes, self.status, self.hubDepartureTime, self.deliveryTime, self.deliveryTruck)

    #when user checks on status of a package, this will find that information
    def statusUpdate(self, time):
        if self.hubDepartureTime <= time:
            if self.deliveryTime <= time:
                self.status = "Delivered at %s" % self.deliveryTime
            elif self.deliveryTime > time:
                self.status = "En route"
        else:
            self.status = "At hub"

    #assigns departure time to package
    def addDepartureTime(self, time):
        self.hubDepartureTime = time

    #assigns delivery truck to package
    def addDeliveryTruck(self, truckName):
        self.deliveryTruck = truckName
