import itertools

class Waveform():
    def __init__self():
        self.time = []
        self.voltage = []        

    def GetRisetime(self):
        for time, voltage in itertools.islice(itertools.izip(self.time, self.voltage), self.ampindex):
            if(voltage < 0.1 * self.amplitude):
                starttime = time
            elif(voltage > 0.1 * self.amplitude):
                endtime = time
        try:
            return (endtime - starttime)
        except UnboundLocalError:
            return -1

    def GetFalltime(self):
        for time, voltage in itertools.islice(itertools.izip(self.time, self.voltage), self.ampindex, None):
            if(voltage > 0.9 * self.amplitude):
                starttime = time
            elif(voltage > 0.1 * self.amplitude):
                endtime = time
        try:
            return (endtime - starttime)
        except UnbountLocalError:
            return -1;

    def GetAmplitude(self):
        for index, voltage in enumerate(self.voltage):
            if(index == 0):
                self.amplitude = voltage
                self.ampindex = index
            else:
                if(self.amplitude < voltage):
                    self.amplitude = voltage
                    self.ampindex = index
        return self.amplitude

    def GetLinearS1(self):
        LineIntegral = 0.0
        prevTime = None
        prevVoltage = None
        for time, voltage in itertools.izip(self.time, self.voltage):
            if(prevTime == None):
                prevTime = time
                prevVoltage = voltage
                continue
            LineIntegral += 0.5 * (voltage + prevVoltage) * (time - prevTime)
            prevTime = time
            prevVoltage = voltage
        return LineIntegral

    """def GetQuadraticS1(self):
        QuadIntegral = 0.0
        for i in range(0, len(self.voltage) / 2):
            QuadIntegral += (self.time[i * 2 + 2] - self.time[i * 2]) / (6.0 * (self.time[i * 2 + 1] - self.time[i * 2]) * (self.time[i * 2 + 2] - self.time[i * 2 + 1])) * ((self.time[i * 2 + 2] - self.time[i * 2 + 1]) * self.voltage[i * 2] * (3.0 * self.time[i * 2 + 1] - 2.0 * self.time[i * 2] - self.time[i * 2 + 2]) + (self.time[i * 2 + 1] - self.time[i * 2]) * self.voltage[i * 2 + 2] * (2.0 * self.time[i * 2 + 2] + self.time[i * 2] - 3.0 * self.time[i * 2 + 1]) + self.voltage[i * 2 + 1] * (self.time[i * 2 + 2] - self.time[i * 2]) ** 2)
        return QuadIntegral"""
