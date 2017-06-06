class Run():
    def __init__(self, runid):
        self.runid = runid
    def GetRunID(self):
        return self.runid
    def SetStartTime(self, time):
        self.starttime = time
    def GetStartTime(self):
        return self.starttime
    def SetEndTime(self, time):
        self.endtime = time
    def GetEndTime(self):
        return self.endtime
    def Print(self):
        print ""
        print "Run ID: %s" % self.runid
        print "Start Time: %s" % self.starttime
        print "End Time: %s" % self.endtime
        print "Run Took %s minutes!" % ((self.endtime - self.starttime) / 60.0)
        print ""
