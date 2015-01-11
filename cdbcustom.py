"""cdbcustom.py
Developer: Noelle Todd
Last Updated: December 12, 2014

This file contains the customwindow class, which is used to
obtain start and end dates from the user for generating a report.

"""

from datetime import datetime, timedelta, date
from tkinter import *
from tkinter import ttk
from cdbifunc2 import *


class customwindow:
    """This class creates a small window that will accept the
    start and end times of a custom, generated report, and
    pass the entered values onto to the correct function.
    """
    def __init__(self):
        #create window
        self.customReportWin = Toplevel()
        self.gridf = Frame(self.customReportWin)
        self.gridf.pack()
        self.customReportWin.title('Generate Custom Report')
        self.bgcolor = 'light blue'
        self.customReportWin.configure(bg=self.bgcolor)
        self.gridf.configure(background=self.bgcolor)

        #create labels/entries
        self.start = StringVar()
        self.end = StringVar()

        textstuff = 'Please enter dates in format: MM/DD/YYYY\n' +\
                    'EXAMPLE: To view visits for 01/05/2015,\n' +\
                    'Start = 01/05/2015, End = 01/06/2015'
        self.instruct = Label(self.gridf,
                              text=textstuff, 
                              font=("Helvetica", 12), bg=self.bgcolor)
        self.startlab = Label(self.gridf, text='Start date:', bg=self.bgcolor,
                              font=("Helvetica", 12))
        self.startentry = Entry(self.gridf, textvariable=self.start, bd=4)
        self.endlab = Label(self.gridf, text='End date:', bg=self.bgcolor,
                            font=("Helvetica", 12))
        self.endentry = Entry(self.gridf, textvariable=self.end, bd=4)

        #create buttons
        self.can = Button(self.gridf, text='Cancel',
                          command=self.cancel_custom)
        self.gen = Button(self.gridf, text='Generate',
                          command=self.generate_report)

        #pack everything into window
        self.instruct.pack()
        self.startlab.pack()
        self.startentry.pack()
        self.endlab.pack()
        self.endentry.pack()
        self.gen.pack(side=RIGHT)
        self.can.pack(side=LEFT)

        self.customReportWin.mainloop()


    def cancel_custom(self):
        """This function will cancel changes.
        """
        self.customReportWin.destroy()
        return


    def generate_report(self):
        """This function will obtain the entered values and generate
        the report.
        """
        #get start date
        try:
            print(self.start.get())
            ds = (str(self.start.get())).split('/')
            print(ds)
            dsm = int(ds[0])
            dsd = int(ds[1])
            dsy = int(ds[2])
            sdate = date(year=dsy, month=dsm, day=dsd)
            
        except ValueError:
            self.cancel_custom()
            errmessage = "Check start date field!\n Enter: MM/DD/YYYY"
            conf = messagebox.showerror(title='Error', message=errmessage)
            return
        
        #get end date
        try:
            de = (str(self.end.get())).split('/')
            print(de)
            dem = int(de[0])
            ded = int(de[1])
            dey = int(de[2])
            edate = date(year=dey, month=dem, day=ded)
            
        except ValueError:
            self.cancel_custom()
            errmessage = "Check end date field!\n Enter: MM/DD/YYYY"
            conf = messagebox.showerror(title='Error', message=errmessage)
            return
        
        generate_custom_report(sdate, edate)
        self.customReportWin.destroy()
        conf = messagebox.showinfo(title='Info',
                                   message='Your report has been generated!')
        return 

if __name__ == '__main__':
    c = customwindow()
    
