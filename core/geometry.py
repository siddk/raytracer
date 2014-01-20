"""
Contains all geometry objects for raytracer, i.e. Points, Vectors, Rays
"""

class Point (object):
    """ 
    Single Point Object 
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vect(self.x - other.x, self.y - other.y, self.z - other.z)

class Vect (object):
    """
    Vector object, with addition and multiplication defined
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return Vect(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        try:
            if isinstance(other, float) or isinstance(other, int):
                return Vect(self.x * other, self.y * other, self.z * other)
            elif isinstance(other, Vect):
                return (self.x * other.x + self.y * other.y + self.z * other.z)
            else:
                return 0
        except:
            return 0

class Ray (object):
    """
    Ray object, with start point and direction passed as parameters
    """

    def __init__(self, startPoint, dirVect):
        self.start = startPoint
        self.dir = dirVect

    def getStart(self):
        return self.start

    def getDir(self):
        return self.dir

