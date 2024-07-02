import math
# A class used to hold coordinate data
class Coordinate:
    # Latitude and longitude is in degrees
    def __init__(self, Radius, Latitude, Longitude):
        self.radius = Radius
        self.latitude = Latitude
        self.longitude = Longitude
    
    # Returns the coordinates in X Y Z form where (0, 0, 0) is the center of the earth
    def ConvertToXYZ(self):
        # uses the earth's sea level plus the distance from sea level
        X = math.cos(self.latitude * math.pi / 180) * (6356752 + self.radius)
        Y = math.sin(self.longitude * math.pi / 180) * (6356752 + self.radius)
        Z = math.sin(self.latitude * math.pi / 180) * (6356752 + self.radius)
        return X, Y, Z

    # Takes in another Coordinate object and returns the distance between them in meters linearly
    def DistanceTo(self, Coordinate):
        X1, Y1, Z1 = self.ConvertToXYZ()
        X2, Y2, Z2 = Coordinate.ConvertToXYZ()
        
        distX = X2 - X1
        distY = Y2 - Y1
        distZ = Z2 - Z1
        
        lengthSquared = distX ** 2 + distY ** 2 + distZ ** 2
        return math.sqrt(lengthSquared)
    
    def __str__(self):
        return "Latitude: " + str(self.latitude) + ", Longitude: " + str(self.longitude) + ", Radius: " + str(self.radius)