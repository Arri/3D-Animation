#####################################################################
# Plot animation class
# Author: Arasch Lagies
# First Version: 4/20/2020
# Last Update: 
#
# Call: 
#####################################################################
import os
import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as Tk
from tkinter.ttk import Frame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import queue
import time

X_WINSIZE = 50
Y_AX_MAX = 20000
FIX_Y_AXIS = False
style.use('ggplot')

class plotAnimation:
    def __init__(self, sensor, t1, x_axis=X_WINSIZE, y_axis=Y_AX_MAX, fixY=FIX_Y_AXIS):
        print("Initializing the animation")
        self.xx = []
        self.yy = []
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.sensor = sensor
        self.t1 = t1
        self.fixY = fixY
        
    def animate(self, i, q, ax):
        print("running animation")
        if self.fixY:
            ax.set_ylim([0,self.y_axis])
        ax.grid(True)
        ax.set_ylabel("Rotation")
    
        # Get measurement values
        value = q.get() / 10.
        print(f"value = {value}")
        with q.mutex:
            q.queue.clear()

        self.xx.append(i)
        self.yy.append(value)

        ## Collect data in a list / array for display    
        if i > self.x_axis:
            # Remove earliest value from the list
            self.xx.remove(self.xx[0])
            self.yy.remove(self.yy[0])
        valx = np.asarray(self.xx)
        valy = np.asarray(self.yy)

        # Update display settings
        ax.clear()
        ax.grid(True)
        ax.set_ylabel('Distance [cm]')
        ax.set_title('Measurement = blue --- Fusion = red')

        # Plot the graph...
        if i <= self.x_axis:
            ax.plot(valx[:i], valy[:i], 'b')
        else:
            ax.plot(valx, valy, 'b')

    def onClick(self, event):
        self.sensor.terminate()
        self.t1.join()
        time.sleep(1)
        print("[INFO] Exiting...")
        exit(0)