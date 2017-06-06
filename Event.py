class Event():
    def __init__(self, eventid, time, voltage):
        self.eventid = eventid
        self.time = time
        self.voltage = voltage
    def GetEventID(self):
        return self.eventid
    def SetRisetime(self, time):
        self.risetime = time
    def GetRisetime(self):
        return self.risetime
    def SetFalltime(self, time):
        self.falltime = time
    def GetFalltime(self):
        return self.falltime
    def SetAmplitude(self, amplitude):
        self.amplitude = amplitude
    def GetAmplitude(self):
        return self.amplitude
    def SetLinearS1(self, S1):
        self.linearS1 = S1
    def GetLinearS1(self):
        return self.linearS1
    def SetQuadraticS1(self, S1):
        self.quadraticS1 = S1
    def GetQuadraticS1(self):
        return self.quadraticS1
    def Print(self):
        print ""
        print "Raw Data: ", self.time, self.voltage
        print "Event ID: %s" % self.eventid
        print "Risetime: %s" % self.risetime
        print "Falltime: %s" % self.falltime
        print "Amplitude: %s" % self.amplitude
        print "S1 (Linear): %s" % self.linearS1
        print "S1 (Quadratic): %s" % self.quadraticS1
        print ""
