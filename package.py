# Package class with all required package fields from the excel spredsheet
from datetime import datetime, timedelta
class Package:
    def __init__(self, id, address, city, zipCode, deadline, weight, status = 'At hub'):
        self.id = id
        self.address = address
        self.city = city
        self.zipCode = zipCode
        if deadline == 'EOD':
            self.deadline = deadline
        else:
            deadline = deadline[0:deadline.index(' ')]
            timeConvert = datetime.strptime(deadline, "%H:%M")
            self.deadline = timedelta(hours=timeConvert.hour, minutes=timeConvert.minute, seconds=timeConvert.second)
        self.weight = weight
        self.status = status
    