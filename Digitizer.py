import time
import random
import math

class Digitizer():
    def __init__(self, trigger):
        self.trigger = trigger
        self.noiset = []
        self.noisev = []
        self.signalt = []
        self.signalv = []

    def ReadADC(self, rpidetectorpipe):
	A = 0.0
	B = 0.0
	C = 0.0
	starttime = 0.0
	counter = 0
        while(True):
	    if(counter % 500 == 100):
		A = random.gauss(300.0, 5.0)
	    	B = random.gauss(10.0, 1.0)
	    	C = random.gauss(500.0, 50.0)
		starttime = self.noiset[-1]
	    elif(counter % 500 == 200):
		A = random.gauss(50.0, 2.0)
		B = random.gauss(10.0, 1.0)
		C = random.gauss(500.0, 50.0)
		starttime = self.noiset[-1]
	    elif(counter % 500 == 300):
		A = random.gauss(150.0, 3.0)
                B = random.gauss(10.0, 1.0)
                C = random.gauss(500.0, 50.0)
		starttime = self.noiset[-1]
	    elif(counter % 500 == 400):
		A = random.uniform(0.0, 400.0)
		B = random.gauss(10.0, 1.0)
		C = random.gauss(500.0, 50.0)
		starttime = self.noiset[-1]
            t = time.time()
	    voltage = A * (1 - math.exp(-B * (t - starttime))) * math.exp(-C * (t - starttime)) + random.gauss(0.0, 0.02)
            
	    counter = counter + 1

	    if(voltage > 3.3):
		voltage = 3.3

	    if(self.Trigger(voltage) == True):
                if(len(self.signalv) == 0):
                    self.signalt.append(self.noiset[-1])
                    self.signalv.append(self.noisev[-1])
                self.signalt.append(t)
                self.signalv.append(voltage)
            else:
                self.noiset.append(t)
                self.noisev.append(voltage)
                if(len(self.signalv) > 0):
                    self.signalt.append(t)
                    self.signalv.append(voltage)
                    self.signalv = [i - self.average for i in self.signalv]
                    rpidetectorpipe.send(self.signalt)
                    rpidetectorpipe.send(self.signalv)
                    self.signalt = []
                    self.signalv = []
		    firstsignal = True
            if(len(self.noisev) == 50):
                del self.noiset[0]
                del self.noisev[0]
            if(rpidetectorpipe.poll()):
                break
        rpidetectorpipe.close()

    def Trigger(self, voltage):
        self.Average()
        self.Sigma()
	if(len(self.noisev) <= 1):
            return False
        elif(voltage > self.average + self.trigger * self.sigma or voltage < self.average - self.trigger * self.sigma):
            return True
        else:
            return False  
      
    def Average(self):
        self.average = 0.0
        for i in self.noisev:
            self.average = self.average + (i / len(self.noisev))

    def Sigma(self):
        self.sigma = 0.0
        for i in self.noisev:
            self.sigma = self.sigma + (i - self.average) ** 2 / len(self.noisev)
        self.sigma = math.sqrt(self.sigma)
