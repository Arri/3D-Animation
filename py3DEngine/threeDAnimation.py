#############################################################
# 3D animation using TKinter
#
# Author: Arasch Lagies
# First Version: 4/16/2020
# Last Update : 
#
# Call:
#############################################################
import os
import graphics.engine

OBJECTPATH = "coords/"
OBJECTVERTICES = "shuttleV.txt"
OBJECTTRIANGLES = "shuttleT.txt"
SENSFOLDER = "sensorData/"
SENSFILE = "accelerometer_sample_data.txt"
NAME = "Animation"
SIZE = 100
SCALE = 3
AUTOROTATE = False

class Animate3D:
    def __init__(self, opath=OBJECTPATH, vertFile=OBJECTVERTICES, trianFile=OBJECTTRIANGLES, name=NAME, 
                size=SIZE, scale=SCALE, sensorFolder=SENSFOLDER, sensorFile=SENSFILE):
        self.points = []
        self.triangles = []
        self.sensor = []
        self.x, self.y, self.z = 0, 0, 0
        self.size = size
        self.verticFile = os.path.join(opath, vertFile)
        self.triangleFile = os.path.join(opath, trianFile)
        self.sensordata = os.path.join(sensorFolder, sensorFile)
        self.name = name
        self.scale = scale
        if not AUTOROTATE:
            with open(self.sensordata, 'r') as f:
                try:
                    for line in f:
                        line = line.replace("\n", "")
                        line = line.split(",")
                        x, y, z = float(line[0]), float(line[1]), float(line[2])
                        print(f"x = {x}, y = {y}, z = {z}")
                        self.sensor.append((x,y,z))
                except:
                    pass
                # make the list iterable...
                self.s = iter(self.sensor)

    def getVertices(self):
        """ Read in the vertix coordinates from a model file """
        with open(self.verticFile, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if not line is None:
                    coords = line[:-2].split(' ')
                    self.points.append([float(coords[0])/self.scale, float(coords[1])/self.scale, float(coords[2])/self.scale])
            f.close()

    def getTriangles(self):
        """ Read in the traingles from a triangle model file """
        with open(self.triangleFile, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if not line is None:
                    coords = line[:-1].split(' ')
                    newCoords = []
                    for coord in coords[1:4]:
                        newCoords.append(int(coord))
                    self.triangles.append(newCoords)
            f.close()

    def startEngine(self):
        """ Start the 3D engine """
        self.engine = graphics.engine.Engine3D(self.points, self.triangles, size=self.size, title=self.name)

    def rotation(self):
        self.engine.rotate('z', 0.1)
        self.engine.rotate("x", 0.1)
        self.engine.rotate("y", 0.1)

    def animation(self):
        """ Run the animation """
        self.engine.clear()
        if AUTOROTATE:
            self.rotation()
        else:
            """ If not autorotating then read data from sensor file for motion """
            try:
                x,y,z = next(self.s)
                self.x -= x 
                self.y -= y 
                self.z -= z
                self.engine.changeCoordinates(10*self.x, 10*self.y, 10*self.z)
                self.x, self.y, self.z = x, y, z
            except:
                pass

        self.engine.render()
        self.engine.screen.after(1, self.animation)

    def mainloop(self):
        self.engine.screen.mainloop()

def run():
    anim = Animate3D()
    anim.getVertices()
    anim.getTriangles()
    anim.startEngine()
    anim.animation()
    anim.mainloop()

if __name__=="__main__":
    run()
    