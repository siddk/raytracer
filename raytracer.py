import sys
from struct import *

def draw(outputFile, scene):
    """
    Opens output file, writes header, then writes to buffer pixel by pixel,
    performing raytracing logic on each pixel
    """
    #Opens output file
    output = open(outputFile, 'wb')
    
    #Creates header to write to buffer (initializer)
    header = pack('BBBBBBBBHHHHBB',
                  0, 0, 2, 0, 0, 0, 0, 0, 0, 0,
                  scene.getWidth(), scene.getHeight(),24, 0)
    output.write(header)
    
    #Iterates through every pixel in the scene, performs raytracing logic (getPixel),
    #adds new pixel to dictionary
    n = 0
    pixelDict = dict()
    for y in range(scene.getHeight()):
        for x in range(scene.getWidth()):
            pixelDict[n] = getPixel(x, y, scene)
            n += 1
    
    #Packs each individual pixel, writes it to output .tga file     
    pixelBuffer = ''
    for i, pixel in pixelDict.items():
        pixelBuffer += pack('BBB', pixel.b, pixel.g, pixel.r)
    output.write(pixelBuffer)

def sphereIntersect(ray, sphere, t):
    """
    Check if ray intersects sphere
    """

    #Gets distance from ray and sphere
    dist = sphere.getPosition() - ray.getStart()
    
    #Diagonal direction vector (direction * magnitude)
    B = ray.getDir() * dist

    #Check if ray hits sphere
    D = B * B - dist * dist + sphere.getSize() * sphere.getSize()
    if D < 0.0:
        return False, t
    
    #Check if t is within .1 epsilon, return corresponding value
    t0 = B - math.sqrt(D)
    t1 = B + math.sqrt(D)
    returnValue = False
    if (t0 > 0.1) and (t0 < t):
        t = t0
        returnValue = True
    if (t1 > 0.1) and (t1 < t):
        t = t1
        returnValue = True
    return returnValue, t

def normal(p1, p2):
    """
    Gets normal of two vectors
    """
    return Vect(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)

def getPixel(x, y, scene):
    """
    Performs the raytracing logic on a per pixel basis. Returns color of each pixel
    """

    #Instantiate variables for red, green, blue values that make up pixel,
    #set fields for constant coefficient
    red = 0
    green = 0
    blue = 0
    coef = 1.0
    level = 0
    
    #Create Ray coming from behind point, with direction vector set to 1
    view = Ray(Point(x, y, -1000),
               Vect(0.0, 0.0, 1.0))

    while True:
        if coef > 0.0 and level < 10: 
            
            #Gets spheres in the scene
            t = 2000.0
            currentSphere = None
            spheres = scene.getSpheres()
            
            #Determine if the ray hits any of the spheres in the scene
            for sphere in spheres:
                isIntersected, t = sphereIntersect(view, sphere, t)
                if isIntersected:
                    currentSphere = sphere
            
            #If ray does not hit a sphere, color does not change, remains black
            if currentSphere == None:
                break
            
            #Get ray normal to sphere (bounce/refraction)
            newStart = view.getStart() + view.getDir() * t
            n = normal(newStart, currentSphere.getPosition())
            temp = n * n
            if temp == 0.0:
                break
            temp = 1.0 / math.sqrt(temp)
            n = n * temp
            
            #Get sphere material to compute refraction/diffusal
            currentMaterial = scene.getMaterialFromId(currentSphere.getMaterial())
            if currentMaterial == None:
                break
            
            #Get lights, to establish refraction angle
            lights = scene.getLights()
            for light in lights:
                dist = normal(light.getPosition(), newStart)
                if n * dist <= 0.0:
                    continue
                a = math.sqrt(dist * dist)
                if a <= 0.0:
                    continue
                
                #Create light ray
                lightRay = Ray(newStart, dist * (1/a))
                isShadowed = False
                
                #Check whether light ray intersects sphere, if it does, ignore it, shadowed
                for sphere in spheres:
                    isIntersected, a = sphereIntersect(lightRay, sphere, a)
                    if isIntersected:
                        isShadowed = True
                        break
                
                #If not, run lambert cosine to get diffusal
                if not isShadowed:
                    lambert = (lightRay.getDir() * n) * coef
                    red += lambert * currentMaterial.getDiffuse().r * light.getIntensity().r
                    green += lambert * currentMaterial.getDiffuse().g * light.getIntensity().g
                    blue += lambert * currentMaterial.getDiffuse().b * light.getIntensity().b
            
            #Update values for next level of bounce
            coef = coef * currentMaterial.getReflection()
            refl = 2.0 * (view.getDir() * n)
            view.start = newStart
            view.dir = view.dir - n * refl

            level += 1
        else:
            break
    
    #Return color object for pixel
    return Color(min(red * 255, 255), min(green * 255, 255), min(blue * 255, 255)) 


if __name__ == "__main__":
    """
    Reads in file from std in, parses it for scene, then draws the new image.

    Instructions: python raytracer.py input/sample_input.txt output/outputfile.tga
    """
    args = sys.argv[1:]
    s = Scene(args[0])
    draw(args[1], s)
