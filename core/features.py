"""
Features file containing objects for light source, and material
"""

class Light (object):
    """
    Light source object with fields for position and intensity
    """

    def setPosition(self, pos):
        self.position = pos

    def setIntensity(self, color):
        self.intensity = color

    def getPosition(self):
        return self.position

    def getIntensity(self):
        return self.intensity

class Material (object):
    """
    Material object with coefficients for diffusion rate, reflection, and identifier
    """

    def setDiffuse(self, color):
        self.diffuse = color

    def setReflection(self, r):
        self.reflection = r

    def setId(self, mId):
        self.id = mId

    def getId(self):
        return self.id

    def getReflection(self):
        return self.reflection

    def getDiffuse(self):
        return self.diffuse