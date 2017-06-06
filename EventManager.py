import Event

class EventManager():
    def __init__(self, numberofevents):
        self.eventid = 1
        self.numberofevents = numberofevents

    def CheckRPiDetectorPipe(self, rpidetectorpipe):
        self.rpidetectorpipe = rpidetectorpipe
        while(self.eventid <= self.numberofevents):
            if(self.rpidetectorpipe.poll()):
                data1 = self.rpidetectorpipe.recv()
                if(data1 == 0):
                    break
                data2 = self.rpidetectorpipe.recv()
                self.Process(data1, data2)        
        self.rpidetectorpipe.send(0)
        self.rpidetectorpipe.close()

    def Process(self, time, voltage):
        self.time = time
	mintime = min(self.time)
        self.time = [i - mintime for i in self.time]
        self.voltage = voltage
        self.amplitude = self.GetAmplitude()
        self.risetime = self.GetRisetime()
        self.falltime = self.GetFalltime()
        self.linearS1 = self.GetLinearS1()
        if(len(self.voltage) % 2 == 1):
            self.quadraticS1 = self.GetQuadraticS1()
        else:
            self.quadraticS1 = -1
        self.Classify()

    def GetRisetime(self):
        for index in range(self.ampindex):
            if(self.voltage[index] < 0.1 * self.amplitude):
                starttime = self.time[index]
            elif(self.voltage[index] > 0.1 * self.amplitude):
                endtime = self.time[index]
        try:
            return (endtime - starttime)
        except UnboundLocalError:
            return -1;

    def GetFalltime(self):
        for index in range(self.ampindex, len(self.voltage)):
            if(self.voltage[index] > 0.9 * self.amplitude):
                starttime = self.time[index]
            elif(self.voltage[index] > 0.1 * self.amplitude):
                endtime = self.time[index]
        try:
            return (endtime - starttime)
        except UnboundLocalError:
            return -1;

    def GetAmplitude(self):
        for index in range(len(self.voltage)):
            if(index == 0):
                self.amplitude = self.voltage[index]
                self.ampindex = index
            else:
                if(self.amplitude < self.voltage[index]):
                    self.amplitude = self.voltage[index]
                    self.ampindex = index
        return self.amplitude

    def GetLinearS1(self):
        LineIntegral = 0.0
        for i in range(0, len(self.voltage) - 1):
            LineIntegral += 0.5 * (self.voltage[i + 1] + self.voltage[i]) * (self.time[i + 1] - self.time[i])
        return LineIntegral

    def GetQuadraticS1(self):
        QuadIntegral = 0.0
        for i in range(0, len(self.voltage) / 2):
            QuadIntegral += (self.time[i * 2 + 2] - self.time[i * 2]) / (6.0 * (self.time[i * 2 + 1] - self.time[i * 2]) * (self.time[i * 2 + 2] - self.time[i * 2 + 1])) * ((self.time[i * 2 + 2] - self.time[i * 2 + 1]) * self.voltage[i * 2] * (3.0 * self.time[i * 2 + 1] - 2.0 * self.time[i * 2] - self.time[i * 2 + 2]) + (self.time[i * 2 + 1] - self.time[i * 2]) * self.voltage[i * 2 + 2] * (2.0 * self.time[i * 2 + 2] + self.time[i * 2] - 3.0 * self.time[i * 2 + 1]) + self.voltage[i * 2 + 1] * (self.time[i * 2 + 2] - self.time[i * 2]) ** 2)
        return QuadIntegral

    def Classify(self):
        if((self.amplitude > 0.0) and (self.risetime > 0.0) and (self.falltime > 0.0) and ((self.linearS1 > 0.0) or (self.quadraticS1 > 0.0))):
            self.event = Event.Event(self.eventid, self.time, self.voltage)
            self.event.SetRisetime(self.risetime)
            self.event.SetFalltime(self.falltime)
            self.event.SetAmplitude(self.amplitude)
            self.event.SetLinearS1(self.linearS1)
            self.event.SetQuadraticS1(self.quadraticS1)
            self.rpidetectorpipe.send(self.event)
            self.eventid = self.eventid + 1
