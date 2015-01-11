"""cdbvolunteer.py
Developer: Noelle Todd
Last Updated: August 30, 2014

This file contains the VolunteerDisplay class that will allow
a user to login, view and change volunteer information, and
add new volunteers to the database.
"""

from datetime import datetime, timedelta, date
from tkinter import *
from tkinter import ttk
from cdbifunc2 import *
from cdbgui import *
from cdbhelp import *


class VolunteerDisplay:    
    def __init__(self):
        """This function declares all variables that are used by
        more than one function.
        """        
        self.bgcolor = 'light blue'

        self.vold=Tk()
        self.parent=Frame(self.vold).grid()
        self.vold.configure(background=self.bgcolor)
        self.vold.title('Volunteer Login')

        #OPENING DISPLAY SCREEN

        #Labels
        self.vollabel = Label(self.parent, text='Volunteer Information',
                        font=("Helvetica", 16),fg='white',bg='gray10')\
                        .grid(row=0,column=0,columnspan=12, sticky=W)
        self.blanklab1 = Label(self.parent, text='            ', bg=self.bgcolor)
        self.blanklab2 = Label(self.parent, text='            ', bg=self.bgcolor)
        self.blanklab3 = Label(self.parent, text='            ', bg=self.bgcolor)
        self.namelabel = Label(self.parent, text='Select name:',
                          font=("Helvetica", 12), bg=self.bgcolor)

        #Selection Box
        self.vol_id = []
        self.vollist = [] #list_active_volunteers()        
        self.vbox = ttk.Combobox(self.parent, state='readonly',
                            values=self.vollist)

        #Buttons        
        self.loginbutton = Button(self.parent, text="Login", width=10,
                                  command=self.loginf)        
        self.viewbutton = Button(self.parent, text="View", width=10,
                                 command=self.viewf)

        #VIEW VOLUNTEER DISPLAY

        #Labels
        self.fnamelabel = Label(self.parent, text="First name:",
                                bg=self.bgcolor, font=("Helvetica", 12))
        self.lnamelabel = Label(self.parent, text="Last name:",
                                bg=self.bgcolor, font=("Helvetica", 12))
        self.phonelabel = Label(self.parent, text="Phone:",
                                bg=self.bgcolor, font=("Helvetica", 12))
        self.actlabel = Label(self.parent, text="Active:",
                              bg=self.bgcolor, font=("Helvetica", 12))
        self.blanklab4 = Label(self.parent, text='            ', bg=self.bgcolor)
        self.blanklab5 = Label(self.parent, text='            ', bg=self.bgcolor)
        self.blanklab6 = Label(self.parent, text='            ', bg=self.bgcolor)

        #Variables
        self.fnent = StringVar()
        self.lnent = StringVar()
        self.phent = StringVar()
        self.actent = StringVar()

        #Entry boxes
        self.fnameent = Entry(self.parent, textvariable=self.fnent, bd=4)
        self.lnameent = Entry(self.parent, textvariable=self.lnent, bd=4)
        self.phoneent = Entry(self.parent, textvariable=self.phent, bd=4)
        self.activeent = Entry(self.parent, textvariable=self.actent, bd=4,
                               state='readonly')

        #Buttons
        self.activate = Button(self.parent, text="Activate", width=14,
                               command=self.activef)
        self.deactivate = Button(self.parent, text="Deactivate", width=14,
                                 command=self.deactivef)
        self.backb = Button(self.parent, text="Back", width=14,
                            command=self.loginDisplay)
        self.savech = Button(self.parent, text="Save Changes", width=14,
                            command=self.updateVol)
        self.savenew = Button(self.parent, text="Save Changes", width=14,
                            command=self.newVol)
        

        #HELP
        self.helpbutton = Button(self.parent, text=' ? ', font=("Helvetica", 10),
                                 command=self.issuehelp)
        

        #MENU
        
        self.menubar = Menu(self.vold)
        self.actionsmenu = Menu(self.menubar,tearoff=0)
        self.actionsmenu.add_command(label='Add New Volunteer',
                                     command=self.addNewVol)
        self.actionsmenu.add_command(label='View Active Volunteers',
                                     command=self.viewActiveVol)
        self.actionsmenu.add_command(label='View All Volunteers',
                                     command=self.viewAllVol)
        self.menubar.add_cascade(label='Actions',menu=self.actionsmenu)
        self.menubar.add_command(label='Quit', command=self.quitf)        
        self.vold.config(menu=self.menubar)

        self.loginDisplay()
        self.vold.mainloop()

        
    def issuehelp(self):
        ch = cdbHelp('login')
        """
        self.helpwin = Tk()
        #self.frame=Frame(self.helpwin).grid()
        self.helpwin.configure(background=self.bgcolor)
        self.helpwin.title('Help')

        instruct = Text(self.helpwin, width=10, height=10).grid(row=3, column=1, padx=20, pady=10)
        """
        return
        

    #functions connected to menu options
    
    def addNewVol(self):
        """This function grids the display for a user to
        input a new volunteer.
        """
        #grid "new" instructive labels
        self.viewDisplay()
        self.actent.set('Currently Active')
        self.savech.grid_forget()
        self.savenew.grid(row=5, column=2, pady=15)
        return
    

    def viewAllVol(self):
        """This function allows a user to view all volunteers,
        regardless of their activity-state.
        """
        self.clearAll()
        self.clearLists()
        self.vbox.set("")
        
        #Labels
        self.blanklab1.grid(self.parent, row=1, column=0, rowspan=2)
        self.blanklab2.grid(self.parent, row=4, column=0, rowspan=2, pady=20)
        self.blanklab3.grid(self.parent, row=3, column=7, columnspan=2)
        self.namelabel.grid(row=3, column=1, rowspan=2)

        #Selection Box
        lav = list_all_volunteers()
        self.vol_id = list_all_volunteers()
        for vol in lav:
            self.vollist.append(vol[0])
        self.vbox.configure(values=self.vollist)
        self.vbox.grid(row=3, column=2, rowspan=2, padx=15, pady=15)

        #Buttons
        self.viewbutton.grid(row=3, column=4, rowspan=2)
        self.helpbutton.grid(row=3, column=5, rowspan=2)
        return
    

    def viewActiveVol(self):
        """This function allows a user to view only active
        volunteers.
        """
        self.clearAll()
        self.clearLists()
        self.vbox.set("")
        
        #Labels
        self.blanklab1.grid(self.parent, row=1, column=0, rowspan=2)
        self.blanklab2.grid(self.parent, row=4, column=0, rowspan=2, pady=20)
        self.blanklab3.grid(self.parent, row=3, column=7, columnspan=2)
        self.namelabel.grid(row=3, column=1, rowspan=2)

        #Selection Box
        lav = list_active_volunteers()
        self.vol_id = list_active_volunteers()
        for vol in lav:
            self.vollist.append(vol[0])
        self.vbox.configure(values=self.vollist)
        self.vbox.grid(row=3, column=2, rowspan=2, padx=15, pady=15)

        #Buttons
        self.viewbutton.grid(row=3, column=4, rowspan=2)
        self.helpbutton.grid(row=3, column=5, rowspan=2)
        return
    

    #functions for displaying
    
    def loginDisplay(self):
        """This function grids all widgets necessary for the login
        screen.
        """
        
        self.clearAll()
        self.clearLists()
        self.vbox.set("")
        
        #Labels
        self.blanklab1.grid(self.parent, row=1, column=0, rowspan=2)
        self.blanklab2.grid(self.parent, row=4, column=0, rowspan=2, pady=20)
        self.blanklab3.grid(self.parent, row=3, column=7, columnspan=2)
        self.namelabel.grid(row=3, column=1, rowspan=2)

        #Selection Box
        self.vol_id = list_active_volunteers()
        for vol in self.vol_id:
            self.vollist.append(vol[0])
                               
        self.vbox.configure(values=self.vollist)
        self.vbox.grid(row=3, column=2, rowspan=2, padx=15, pady=15)

        #Buttons
        self.loginbutton.grid(row=3, column=4, rowspan=2)
        self.viewbutton.grid(row=3, column=5, rowspan=2)
        self.helpbutton.grid(row=3, column=6, rowspan=2)
        return
    

    def viewDisplay(self):
        """This function allows a user to view a single volunteer's
        information.
        """
        #clear unnecessary widgets
        self.clearAll()

        #grid widgets
        self.fnamelabel.grid(row=1, column=1, pady=15)
        self.fnameent.grid(row=1, column=2, pady=15)
        self.lnamelabel.grid(row=2, column=1, pady=15)
        self.lnameent.grid(row=2, column=2, pady=15)
        self.phonelabel.grid(row=3, column=1, pady=15)
        self.phoneent.grid(row=3, column=2, pady=15)
        self.actlabel.grid(row=4, column=0, pady=15, padx=10)
        self.activeent.grid(row=4, column=1, pady=15)
        self.blanklab4.grid(row=1, column=3, padx=15)

        self.backb.grid(row=5, column=1, pady=15) 
        self.savech.grid(row=5, column=2, pady=15)
      
        return
    

    def fillViewDisplay(self):
        """This function will prepopulate fields from the database.
        """
        vid = self.vol_id[self.vbox.current()][1]
        vclass = select_volunteer(vid)
        
        #get selected volunteer's info
        #prepopulate fields
        self.fnent.set(vclass.firstname) 
        self.lnent.set(vclass.lastname) 
        self.phent.set(vclass.phone) 
        if vclass.active == 1:
            self.actent.set('Currently Active')
            self.deactivate.grid(row=4, column=2)
        else:
            self.actent.set('Not Active')
            self.activate.grid(row=4, column=2)
        return
    

    def clearAll(self):
        """This function clears all widgets from the grid.
        """
        #Clear Widgets
        allwid = [self.blanklab1, self.blanklab2, self.blanklab3,
                  self.namelabel, self.vbox, self.loginbutton,
                  self.viewbutton, self.fnamelabel, self.lnamelabel,
                  self.phonelabel, self.actlabel, self.fnameent,
                  self.lnameent, self.phoneent, self.activeent,
                  self.activate, self.deactivate, self.savech, self.savenew,
                  self.backb]
        for wid in allwid:
            wid.grid_forget()

        #Clear Variables
        self.fnent.set("")
        self.lnent.set("") 
        self.phent.set("")
        self.actent.set("")
        return

    
    def clearLists(self):
        """This function clears lists.
        """
        self.vollist = []
        self.vol_id = []
        return


    #functions connected to buttons
    
    def loginf(self):
        """Retrieves volunteer info, sends to allobjects;
        closes volunteer program.
        """
        #retrive volunteer id
        try:
            vid = self.vol_id[self.vbox.current()][1]
            vname = self.vol_id[self.vbox.current()][0]
            vclass = select_volunteer(vid)
            color = vclass.color
            
                
            #send volunteer id to allobjects()
            import cdbgui
            self.quitf()
            ao = cdbgui.allobjects(vid, vname, color)
            return
        
        except IndexError:
            return

    
    def viewf(self):
        """This function will call other functions to view a
        volunteer's info.
        """
        self.viewDisplay()
        self.fillViewDisplay() 
        return

        
    def quitf(self):
        """This function will close the program.
        """
        quit_session()
        self.vold.destroy()
        return


    #activation buttons
    def activef(self):
        """Activates a volunteer.
        """
        self.actent.set('Currently Active')
        self.updateVol()
        return

    
    def deactivef(self):
        """Deactivates a volunteer.
        """
        self.actent.set('Not Active')
        self.updateVol()
        return

    
    def updateVol(self):
        """This function updates a volunteer's record.
        """
        try:
            fname = str(self.fnent.get())
            lname = str(self.lnent.get())
            phone = str(self.phent.get())
            active = str(self.actent.get())
            if active == 'Currently Active':
                active = True
            else:
                active = False
            vid = self.vol_id[self.vbox.current()][1]
            volcolor = (select_volunteer(vid)).color
            update_vol(vid, fname, lname, phone, active, volcolor)

        except ValueError:
            conf = messagebox.showerror(title='Error',
                        message="Did you forget to type something?")
            return
        return


    def newVol(self):
        """This function creates a record for new volunteer.
        """
        try:
            fname = str(self.fnent.get())
            lname = str(self.lnent.get())
            phone = str(self.phent.get())
            active = True
            new_volunteer(fname, lname, phone, active)
            self.loginDisplay()
            
        except ValueError:
            conf = messagebox.showerror(title='Error',
                        message="Did you forget to type something?")
            return
        return
        
    
if __name__ == '__main__':
    vd = VolunteerDisplay()
