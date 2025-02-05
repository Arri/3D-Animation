#############################################################
# Script to convert a paintext STL file into the formant 
# required for the tkinter 3D engine
#
# Author: Arasch Lagies
# First Version: 4/16/2020
# Last Update : 
#
# Call:
#############################################################
import os
import csv

SOURCEPATH = r"C:\Users\arasc\Documents\Projects\animation\objects"
TARGETPATH = r"C:\Users\arasc\Documents\Projects\animation\pyEngine3D-master\coords"
SOURCEFILE = "shuttle.stl"
TARGET_T = "shuttleT.txt"
TARGET_V = "shuttleV.txt"

class collectSTL:
    def __init__(self, path=SOURCEPATH, targetpath=TARGETPATH, sourcefile=SOURCEFILE, traingleFile=TARGET_T, vertexFile=TARGET_V):
        self.source = os.path.join(path, sourcefile)
        self.vertFile = os.path.join(targetpath, vertexFile)
        self.triangleFile = os.path.join(targetpath, traingleFile)
        self.vertex = []
        self.triangleList = []
        self.triangle = []

    def collect(self):
        """ collect unique vertices and the numbers representing the vertices to join them to triangles"""
        with open(self.source, 'r') as f:
            countVertex = 0
            for l in f:
                parts = l.split()
                if parts[0]=="vertex":
                    new_vertex = (float(parts[1]), float(parts[2]), float(parts[3]))
                    try:
                        locV = self.vertex.index(new_vertex)
                        # If the same set of coordiantes was found in the vertex list
                        # then this set of coordinates does not need to be added again
                        # But the nod number needs to be added to the triangles list...
                        self.triangleList.append(locV)
                    except:
                        # If the (x,y,z) tuple of coordinates is not found in the current vertex list
                        # then just add the tuple to the list.
                        self.vertex.append(new_vertex)
                        self.triangleList.append(countVertex)
                        countVertex += 1

        # The list of triangle numbers needs to be rearranged to tuples of 3 values for the 3 
        # corners of triangle...
        for i in range(0,len(self.triangleList)-3,3):
            self.triangle.append((3, self.triangleList[i], self.triangleList[i+1], self.triangleList[i+2]))
        print(self.vertex)
        print(self.triangle)

    def saveVertix(self):
        """ Save Vertices to the vertix file """   
        with open(self.vertFile, "w", newline='') as tfile:
            writer = csv.writer(tfile, delimiter= ' ')
            for l in self.vertex:
                writer.writerow(l) 

    def saveTriangles(self):
        """ Save Traingles in a file """
        with open(self.triangleFile, "w", newline='') as vfile:
            writer = csv.writer(vfile, delimiter= ' ')
            for l in self.triangle:
                writer.writerow(l)

def run():
    stl = collectSTL()
    stl.collect()
    stl.saveVertix()
    stl.saveTriangles()

if __name__=="__main__":
    run()
