import Tkinter
import time
import pg
import smtplib
import multiprocessing
import sys
import os

import matplotlib
matplotlib.use('TKAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot

import Run
import Digitizer
import EventManager
import Event

class RPiDetector(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.configure(background="white")
        self.geometry(str(self.winfo_screenwidth()/4) + "x" + str(self.winfo_screenheight()/2))
        self.SetupHVCanvas()
        self.SetupHVButtons()
        self.SetupSignalCanvas()
        self.SetupRunButtons()
	self.update()

    def SetupHVCanvas(self):
        HVFigure = matplotlib.pyplot.figure(facecolor="white", tight_layout=True)
        self.HVAxes = HVFigure.add_subplot(111)
        self.HVAxes.set_title("Silicon Photomultiplier High Voltage")
        self.HVAxes.set_xlabel('Time [a.u.]')
        self.HVAxes.set_xlim(0.0, 1.0)
        self.HVAxes.set_ylabel('Voltage [a.u.]')
        self.HVAxes.set_ylim(0.0, 1.0)
        self.HVPlot, = self.HVAxes.plot([], [])
        self.HVCanvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(HVFigure,
                                                                            master = self)
        self.HVCanvas.get_tk_widget().configure(background="white",
                                                highlightcolor="white",
                                                highlightbackground="white")
        self.HVCanvas.show()
        self.HVCanvas.get_tk_widget().place(x=0,y=0,width=self.winfo_screenwidth() / 8.0,height=self.winfo_screenwidth() * 4.0 / 48.0)

    def SetupHVButtons(self):
        self.HVButton = Tkinter.Button(self,
                                       text="HV ON",
                                       font=("arial", 14, "bold"),
                                       activeforeground="white",
                                       foreground="white",
                                       activebackground="black",
                                       background="blue",
                                       command=self.HVOn)
        self.HVButton.place(x=0, y=self.winfo_screenwidth()*4.0 / 48.0, width = 80, height = 50)
        self.SetHVButton = Tkinter.Button(self,
                                          text="SET HV",
                                          font=("arial", 14, "bold"),
                                          activeforeground="white",
                                          foreground="white",
                                          activebackground="black",
                                          background="purple",
                                          command=self.SetHV,
                                          state="disabled")
        self.SetHVButton.place(x=0, y=self.winfo_screenwidth()*4.0 / 48.0 + 50, width=80, height=50)
        self.BiasVoltage = Tkinter.DoubleVar(value=0.0)
        self.BiasVoltageEntry = Tkinter.Entry(self,
                                              font=("arial", 14, "bold"),
                                              foreground="black",
                                              background="white",
                                              justify="center",
                                              state="disabled",
                                              textvariable=self.BiasVoltage)
        self.BiasVoltageEntry.place(x=80, y=self.winfo_screenwidth()*4.0/48.0+50,  width=80, height=50)
        self.VoltageText = Tkinter.Label(self,
                                        text="V",
                                        font=("arial", 14, "bold"),
                                        foreground="black",
                                        background="white",
                                        justify="center",
                                        state="disabled")
        self.VoltageText.place(x=160, y=self.winfo_screenwidth()*4.0/48.0+50, width=40, height=50)

    def HVOn(self):
        self.HVButton.configure(text="HV OFF",
                                foreground="white",
                                background="orange",
                                command=self.HVOff)
        self.SetHVButton.configure(state="normal")
        self.BiasVoltage.set(50.0)
        self.BiasVoltageEntry.configure(state="normal")
        self.VoltageText.configure(state="normal")
        self.RunButton.configure(state="normal")
        self.EventsText.configure(state="normal")
        self.NumberOfEventsEntry.configure(state="normal")
        self.CommentsText.configure(state="normal")
        self.CommentsEntry.configure(state="normal") 

    def HVOff(self):
        self.HVButton.configure(text="HV ON",
                                foreground="white",
                                background="blue",
                                command=self.HVOn)
        self.SetHVButton.configure(state="disabled")
        self.BiasVoltage.set(0.0)
        self.BiasVoltageEntry.configure(state="disabled")
        self.VoltageText.configure(state="disabled")
        self.RunButton.configure(state="disabled")
        self.EventsText.configure(state="disabled")
        self.NumberOfEventsEntry.configure(state="disabled")
        self.CommentsText.configure(state="disabled")
        self.CommentsEntry.configure(state="disabled") 

    def SetHV(self):
        pass

    def SetupSignalCanvas(self):
        self.SignalFigure = matplotlib.pyplot.figure(facecolor="white", tight_layout=True)
        self.SignalAxes = self.SignalFigure.add_subplot(111)
        self.SignalAxes.set_title("Waveform Viewer")
        self.SignalAxes.set_xlabel('Time [ms]')
        self.SignalAxes.set_xlim(0, 100.0)
        self.SignalAxes.set_ylabel('Voltage [a.u.]')
        self.SignalAxes.set_ylim(0.0, 3.3)
        self.SignalPlot, = self.SignalAxes.plot([], [])
        self.SignalCanvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.SignalFigure,
                                                                                master = self)
        self.SignalCanvas.get_tk_widget().configure(background="white",
                                                    highlightcolor="white",
                                                    highlightbackground="white")
        self.SignalCanvas.show()
        self.SignalCanvas.get_tk_widget().place(x=self.winfo_screenwidth()/8.0,y=0,width=self.winfo_screenwidth() / 8.0,height=self.winfo_screenwidth() * 4.0 / 48.0)
        
    def SetupRunButtons(self):
        self.RunButton = Tkinter.Button(self,
                                        text="RUN",
                                        font=("arial", 14, "bold"),
                                        activeforeground="white",
                                        foreground="white",
                                        activebackground="black",
                                        background="green",
                                        state="disabled",
                                        command=self.BeginRun)
        self.RunButton.place(x=self.winfo_screenwidth()/8.0 - 40, y=self.winfo_screenwidth()*4.0 / 48.0, width = 80, height = 50)
        self.EventsText = Tkinter.Label(self,
                                        text="Events:",
                                        font=("arial", 14, "bold"),
                                        foreground="black",
                                        background="white",
                                        justify="center",
                                        state="disabled")
        self.EventsText.place(x=self.winfo_screenwidth()/8.0 - 40, y=self.winfo_screenwidth()*4.0/48.0+50, width=80, height=50)
        self.NumberOfEvents = Tkinter.IntVar(value=500000)
        self.NumberOfEventsEntry = Tkinter.Entry(self,
                                                 font=("arial", 14, "bold"),
                                                 foreground="black",
                                                 background="white",
                                                 justify="center",
                                                 state="disabled",
                                                 textvariable=self.NumberOfEvents)
        self.NumberOfEventsEntry.place(x=self.winfo_screenwidth()/8.0 + 40, y=self.winfo_screenwidth()*4.0/48.0+50, width=80, height=50)
	self.CommentsText = Tkinter.Label(self,
                                          text="Comments:",
                                          font=("arial", 14, "bold"),
                                          foreground="black",
                                          background="white",
                                          justify="center",
                                          state="disabled")
	self.CommentsText.place(x=self.winfo_screenwidth()/8.0 - 62.5, y=self.winfo_screenwidth()*4.0/48.0+100, width=125, height=50)
	self.Comments = Tkinter.StringVar(value='none')
	self.CommentsEntry = Tkinter.Entry(self,
                                           font=("arial", 14, "bold"),
                                           foreground="black",
                                           background="white",
                                           justify="center",
                                           state="disabled",
                                           textvariable=self.Comments)
	self.CommentsEntry.place(x=self.winfo_screenwidth()/8.0 + 62.5, y=self.winfo_screenwidth()*4.0/48.0+100, width=80, height=50)
	self.QuitButton = Tkinter.Button(self,
                                         text="EXIT",
                                         font=("arial", 14, "bold"),
                                         activeforeground="white",
                                         foreground="white",
                                         activebackground="black",
                                         background="gray",
                                         command=self.Quit)
        self.QuitButton.place(x=self.winfo_screenwidth()/4.0 - 80,y=self.winfo_screenwidth()*4.0/48.0,width = 80, height=50)

    def BeginRun(self):
        self.HVButton.configure(state="disabled")
        self.SetHVButton.configure(state="disabled")
        self.BiasVoltageEntry.configure(state="disabled")
        self.VoltageText.configure(state="disabled")
        self.RunButton.configure(text="STOP",
                                  foreground="white",
                                  background="red",
                                  command=self.EndRun)
        self.EventsText.configure(state="disabled")
        self.NumberOfEventsEntry.configure(state="disabled")
	self.CommentsText.configure(state="disabled")
	self.CommentsEntry.configure(state="disabled")
        self.digitizerpipe, rpidetectorpipe1 = multiprocessing.Pipe()
        digitizer = Digitizer.Digitizer(3.0)
        self.digitizerprocess = multiprocessing.Process(target=digitizer.ReadADC, args=(rpidetectorpipe1, ))
        self.eventmanagerpipe, rpidetectorpipe2 = multiprocessing.Pipe()
        eventmanager = EventManager.EventManager(self.NumberOfEvents.get())
        self.eventmanagerprocess = multiprocessing.Process(target=eventmanager.CheckRPiDetectorPipe, args=(rpidetectorpipe2, ))
        self.ConnectToDatabase()
	query = self.Database.query('SELECT * FROM runinfo ORDER BY runid DESC LIMIT 1').dictresult()
        self.Database.close()
	lastrunid = (query[len(query) - 1])['runid']
	self.runid = lastrunid + 1
	self.run = Run.Run(self.runid)
	self.EndOfRun = False
	self.run.SetStartTime(time.time())
	self.file = open('./data/Run%03d.txt' % (self.runid), 'w')
        self.digitizerprocess.start()
        self.eventmanagerprocess.start()
        self.CheckPipes()

    def EndRun(self):
        self.EndOfRun = True
        self.digitizerpipe.send(0)
        self.digitizerpipe.close()
        self.digitizerprocess.join()
        self.run.SetEndTime(time.time())
        self.eventmanagerpipe.send(0)
        self.eventmanagerpipe.close()
        self.eventmanagerprocess.join()
	# self.run.Print()
	self.ConnectToDatabase()
        self.Database.insert('runinfo',
			     runid=self.runid,
			     events=self.lasteventid,
			     sipmhv=self.BiasVoltage.get(),
			     startt= self.run.GetStartTime(),
			     endt = self.run.GetEndTime(),
			     rate = self.lasteventid / (self.run.endtime - self.run.starttime),
			     comments = self.Comments.get())
	self.Database.close()
	message = '\nRun ID: %d\nEvents: %d\nRate: %.2f Hz' % (self.runid, self.lasteventid, self.lasteventid / (self.run.endtime - self.run.starttime))
	self.ConnectToEmail()
	self.smtpserver.sendmail(self.rpiemail, self.shifteremail, message)
        self.smtpserver.close()
	self.file.close()
	self.HVButton.configure(state="normal")
        self.SetHVButton.configure(state="normal")
        self.BiasVoltageEntry.configure(state="normal")
        self.VoltageText.configure(state="normal")
        self.RunButton.configure(text="RUN",
                                 foreground="white",
                                 background="green",
                                 command=self.BeginRun)
        self.EventsText.configure(state="normal")
        self.NumberOfEventsEntry.configure(state="normal")
        self.CommentsText.configure(state="normal")
        self.CommentsEntry.configure(state="normal") 

    def CheckPipes(self):
        if(self.digitizerpipe.poll()):
            self.eventmanagerpipe.send(self.digitizerpipe.recv())
            self.eventmanagerpipe.send(self.digitizerpipe.recv())
        if(self.eventmanagerpipe.poll()):
            data1 = self.eventmanagerpipe.recv()
            if(data1 == 0):
                self.EndRun()
            else:
		self.lasteventid = data1.eventid
		self.file.write("%6d %+7.6f %+7.6f\n" % (self.lasteventid, data1.linearS1, data1.quadraticS1))
		if(self.lasteventid % 100 == 0):
               	    self.SignalAxes.set_title("Run %d Event %d" % (self.runid, data1.eventid))
                    data1.time = [i * 1E+03 for i in data1.time]
                    self.SignalPlot.set_data(data1.time, data1.voltage)
                    self.SignalAxes.set_xlim(min(data1.time), max(data1.time))
		    # minvoltage = min(data1.voltage)
		    # maxvoltage = max(data1.voltage)
                    # self.SignalAxes.set_ylim(-0.05 * (maxvoltage - minvoltage) + minvoltage,
                    #                          0.05 * (maxvoltage - minvoltage) + maxvoltage)
                    self.SignalCanvas.draw()
        	if(self.lasteventid % 100000 == 0):
		    self.SignalFigure.savefig("./Figures/Run%06d_Event%07d.pdf" % (self.runid, data1.eventid), format='pdf')
	if(not self.EndOfRun):
            self.after(1, self.CheckPipes)

    def Quit(self):
        try:
            self.digitizerpipe.send(0)
        except AttributeError:
            pass
        finally:
            try:
                self.eventmanagerpipe.send(0)
            except AttributeError:
                pass
            finally:
                try:
                    self.digitizerprocess.join()
                except AttributeError:
                    pass
                finally:
                    try:
                        self.eventmanagerprocess.join()
                    except AttributeError:
                        pass
                    finally:
                        self.destroy()
                        sys.exit()

    def ConnectToDatabase(self):
	self.Database = pg.DB(dbname=os.environ.get('DATABASE_NAME'), user=os.environ.get('DATABASE_USER'))

    def ConnectToEmail(self):
	self.rpiemail = os.environ.get('EMAIL_ADDRESS')
	self.rpiemailpassword = os.environ.get('EMAIL_PASSWORD')
	self.shifteremail = ['7174764903@vtext.com']
	# self.shifteremail = ['7174764903@vtext.com', '7083743785@tmomail.net']
	self.smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
	self.smtpserver.ehlo()
	self.smtpserver.starttls()
	self.smtpserver.login(self.rpiemail, self.rpiemailpassword)

rpidetector = RPiDetector()
rpidetector.mainloop()
