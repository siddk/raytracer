from core.color import Color
from core.features import Light, Material
from core.geometry import Point, Vect
from core.sphere import Sphere

"""
Reads in a .txt scene file, and parses the data for the necessary components.

Creates objects for spheres, lights, materials, and the scene in general
"""

def convertStr(s):
    """
    Converts string number to respective data type
    """
    try:
        ret = int(s)
    except ValueError:
        ret = float(s)
    return ret

class Scene (object):
    """
    Scene object, with fields for width, height, materials, lights, and spheres.

    Lays out the scene for raytracing.
    """

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getMaterials(self):
        return self.materials

    def getMaterialFromId(self, materialId):
        for material in self.materials:
            currentId = material.getId()
            if currentId == materialId:
                return material
        return None

    def getLights(self):
        return self.lights

    def getSpheres(self):
        return self.spheres
    
    def __init__(self, filePath):
        """
        Parser for .txt scene file
        """
        self.width = 0
        self.height = 0
        self.materials = []
        self.lights = []
        self.spheres = []
        f = open(filePath)
        section = ''
        for line in f:
            l = line.strip()
            if section == '':
                if len(l) != 0:
                    if l[:2] != '//':
                        section = l
            else:
                if section.find('Scene') != -1:
                    if l == '{':
                        pass
                    elif l == '}':
                        section = ''
                    else:
                        words = l.split('=')
                        if words[0] == 'Width':
                            self.width = convertStr(words[1])
                        elif words[0] == 'Height':
                            self.height = convertStr(words[1])
                elif section.find('Material') != -1:
                    if l == '{':
                        tempMat = Material()
                    elif l == '}':
                        self.materials.append(tempMat)
                        section = ''
                    else:
                        words = l.split('=')
                        if words[0] == 'Diffuse':
                            params = words[1].split()
                            tempMat.setDiffuse(Color(convertStr(params[0]),convertStr(params[1]),convertStr(params[2])))
                        elif words[0] == 'Reflection':
                            tempMat.setReflection(convertStr(words[1]))
                        elif words[0] == 'Id':
                            tempMat.setId(convertStr(words[1]))
                elif section.find('Sphere') != -1:
                    if l == '{':
                        tempSphere = Sphere()
                    elif l == '}':
                        self.spheres.append(tempSphere)
                        section = ''
                    else:
                        words = l.split('=')
                        if words[0] == 'Center':
                            params = words[1].split()
                            tempSphere.setPosition(Point(convertStr(params[0]),convertStr(params[1]),convertStr(params[2])))
                        elif words[0] == 'Size':
                            tempSphere.setSize(convertStr(words[1]))
                        elif words[0] == 'Material':
                            tempSphere.setMaterial(convertStr(words[1]))
                elif section.find('Light') != -1:
                    if l == '{':
                        tempLight = Light()
                    elif l == '}':
                        self.lights.append(tempLight)
                        section = ''
                    else:
                        words = l.split('=')
                        if words[0] == 'Position':
                            params = words[1].split()
                            tempLight.setPosition(Point(convertStr(params[0]),convertStr(params[1]),convertStr(params[2])))
                        elif words[0] == 'Intensity':
                            params = words[1].split()
                            tempLight.setIntensity(Color(convertStr(params[0]),convertStr(params[1]),convertStr(params[2])))


