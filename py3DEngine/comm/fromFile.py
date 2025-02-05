####################################################
# Read sensor data from file
#
# Arasch Lagies
# Version: 3/19/2020
# Last update:
#
####################################################
import os
import time

FILEPATH = "sensorData/"
FILENAME = "KalmanFiltered_IMUaccelerator.txt"

class Sensor():
	def __init__(self, path= FILEPATH, sensor=FILENAME, test=False):
		self.running = True					# Flag to run and terminate while loop
		self.test    = test
		self.sensor  = os.path.join(path, sensor)
			
	def read_loop(self, q):
		""" This function reads data from a file with sensor data and puts the values 
			slowly in a queue that can be accessed by the plotting fuction... 
		"""
		xvalue = 0
		#while(self.running):
		with open(self.sensor, 'r') as f:
			for l in f:
				try:
					if not self.running:
						break            # The terminate function was called...
					l = l.replace('\n', '')
					x,_,_ = l.split(",")
					xvalue = float(x)
					if self.test:
						print(xvalue)
					else:
						# time.sleep(0.5)
						q.put(xvalue)	
				except:
					break
			print(f"This is what q gets in the sensor fuction : {q.queue}") 
		return 0
						
	def terminate(self):
		""" Calling this function will terminate the sensor measurement process """
		print("[INFO] Terminating Measurement Thread...")
		self.running = False

