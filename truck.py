# Class representing trucks. It's main function is holding assigned
# packages and holding its defined route after the route algorithms are
# called.  
from datetime import timedelta

class Truck:

    def __init__(self, name):
        self.name = name
        self.totalMilesDriven = 0
        self.packages = [] 
        self.route = [['HUB', timedelta(hours=8, minutes=0, seconds=0)], ['HUB', None]]

    # Adds package to package array and sets its status to loaded. 
    def addPackage(self, package):
        package.status = 'Loaded'
        self.packages.append(package)