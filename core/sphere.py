"""
Sphere object (image for raytracing)
"""

class Sphere (object):
	"""
	Sphere object with fields for position, size, and material
	"""

    def setPosition(self, center):
        self.center = center

    def setSize(self, size):
        self.size = size

    def setMaterial(self, mId):
        self.materialId = mId;

    def getPosition(self):
        return self.center

    def getSize(self):
        return self.size

    def getMaterial(self):
        return self.materialId
