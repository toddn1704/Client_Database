"""cdbgui.py
Developers: Christina Hammer, Noelle Todd
Last Updated: August 19, 2014

This file contains a class version of the interface, in an effort to
make a program with no global variables.

"""


from datetime import datetime, timedelta, date
from tkinter import *
from tkinter import ttk
from cdbifunc import *
import cdbvolunteer

class allobjects:
    """This class attempts to contain ALL labels, entries, etc.,
    so that there are no global variables.
    """

    def __init__(self, volunteerID, volunteerName, bgcolor):
        """This function declares all variables that are used by
        more than one function.
        """

        self.volID = volunteerID #the id of the volunteer who logged in
        self.volunteerName = volunteerName
        self.bgcolor = bgcolor
        
        #Variables used later on
        self.cursel = 0
        self.selectedVisit = 0
        self.id_list = []
        self.mem_list = []
        self.clientlist = list_people()
        self.visitDict = {}
        #holds entryboxes for family members
        self.memDict = {}
        self.info = {}
        self.addmemberON = False #checks if member boxes have already been added

        #dictionaries/lists used for date entry
        self.month_li = ["January", "February", "March", "April",
                             "May", "June", "July", "August", "September",
                             "October", "November", "December"]
        self.month_day_dict = {"January":31, "February":29, "March":31,
                               "April":30, "May":31, "June":30, "July":31,
                               "August":31, "September":30, "October":31,
                               "November":30, "December":31}
        self.month_int = {1:"January", 2:"February", 3:"March",
                          4:"April", 5:"May", 6:"June", 7:"July",
                          8:"August", 9:"September", 10:"October",
                          11:"November", 12:"December"}
        self.int_month = {"January":1, "February":2, "March":3,
                          "April":4, "May":5, "June":6, "July":7,
                          "August":8, "September":9, "October":10,
                          "November":11, "December":12}

        #customize colors/fonts
        #This will connect to the database itself,
        #and retrieve the colors from there.
        #self.bgcolor = 'light blue' #'lavender'
        #self.labfont = 'Helvetica'
        #self.labBGcolor = 'gray10'
        #self.labFGcolor = 'white'
        #self.cliSearLabBG = 'Coral'
        #self.cliSearLabFG = 'white'

        
        #configuring window
        self.ciGui=Tk()
        self.gridframe=Frame(self.ciGui).grid()
        self.ciGui.configure(background=self.bgcolor)
        self.ciGui.title('Food Pantry Database')
        

        #CLIENT SEARCH SETUP        
        self.cslabel = Label(self.gridframe,text='Client Search',
                             font=("Helvetica", 16),fg='white',bg='gray10')\
                             .grid(row=0,column=0,columnspan=2, sticky=W)
        self.csblank = Label(self.gridframe, text='     ',
                             font=('Helvetica',10), bg=self.bgcolor)\
                             .grid(row=0,column=2,sticky=E)

        #Name Searchbox
        self.ns = StringVar()
        self.nameSearchEnt = Entry(self.gridframe, cursor = 'shuttle',
                                   textvariable=self.ns)
        self.nameSearchEnt.grid(row=2,column=0)
        self.nameSearchEnt.bind('<Key>',self.nameSearch) 

        self.searchButton = Button(self.gridframe, text='Search Clients',
                                    command=self.nameSearch)
        self.searchButton.grid(row=2, column=1)

        #Client Listbox
        self.client_listbox = Listbox(self.gridframe,height=10,width=40)
        self.client_listbox.bind('<<ListboxSelect>>', self.displayInfo )
        self.client_listbox.config(exportselection=0)

        self.scrollb = Scrollbar(self.gridframe)
        self.client_listbox.bind('<<ListboxSelect>>',self.displayInfo )
        self.client_listbox.config(yscrollcommand=self.scrollb.set)
        self.scrollb.config(command=self.client_listbox.yview)
        
        self.client_listbox.grid(row=3, column=0, rowspan=5, columnspan=2)
        self.scrollb.grid(row=3, column=1, rowspan=5, sticky=E+N+S)

        self.firstSep = ttk.Separator(self.gridframe, orient='vertical')\
                        .grid(row=1,column=2,rowspan=40,sticky=NS)

        self.NCButton = Button(self.gridframe, text='New Client',
                                command=self.newClientDisplay, width=25)\
                                .grid(row=9, column=0, columnspan=2)


        #CLIENT INFORMATION SETUP       
        self.secondSep = ttk.Separator(self.gridframe, orient='horizontal')\
                                .grid(row=0,column=3,columnspan=40,sticky=EW)
        self.cilabel = Label(self.gridframe, text='Client Information',
                           font=("Helvetica", 16),fg='white',bg='gray10')\
                           .grid(row=0,column=3,columnspan=12, sticky=W)
        self.ciblank = Label(self.gridframe, text='   ',font=('Helvetica',10),
                        bg=self.bgcolor).grid(row=1,column=3,sticky=E)
        
        #First name
        self.fnv = StringVar()
        self.fnlabel = Label(self.gridframe, text="First Name: ",
                             font=('Helvetica',12),bg=self.bgcolor)\
                             .grid(row=2, column=3,rowspan=2,sticky=E)
        self.fname = Entry(self.gridframe, textvariable=self.fnv,bd=4)
        self.fname.grid(row=2, column=4, rowspan=2, columnspan=1, sticky=W)

        #Last name
        self.lnv = StringVar()
        self.lnlabel = Label(self.gridframe, text='Last Name: ',
                             font=('Helvetica',12),bg=self.bgcolor)\
                             .grid(row=2,column=5,rowspan=2, sticky=W)
        self.lname = Entry(self.gridframe, textvariable=self.lnv,bd=4)
        self.lname.grid(row=2,column=6, rowspan=2, columnspan=1, sticky=W)

        #Phone
        self.phv = StringVar()
        self.phlabel = Label(self.gridframe, text='Phone: ',
                             font=('Helvetica',12),bg=self.bgcolor)\
                             .grid(row=2, column=7,rowspan=2, sticky=E)
        self.phone = Entry(self.gridframe, textvariable=self.phv, bd=4)
        self.phone.grid(row=2, column=8, columnspan=2, rowspan=2, sticky=W)

        #Date of Birth
        self.doblabel = Label(self.gridframe, text='Date of Birth: ',
                              font=('Helvetica',12),bg=self.bgcolor)\
                              .grid(row=4,column=3, rowspan=2, sticky=E)
        self.mv = StringVar()
        self.dv = StringVar()
        self.yv = StringVar()

        #dob month combobox
        self.mob = ttk.Combobox(self.gridframe, width=10, state='readonly',
                                values=self.month_li, textvariable=self.mv)
        self.mob.bind('<<ComboboxSelected>>', self.monthbox_select)
        #dob day spinbox
        self.dob = Spinbox(self.gridframe, from_=0, to=0,
                           textvariable=self.dv, width=5, bd=4)
        #dob year spinbox
        self.yob = Spinbox(self.gridframe, from_=1900, to=2500,
                           textvariable=self.yv, width=7, bd=4)
        self.mob.grid(row=4, column=4, rowspan=2, sticky=W)
        self.dob.grid(row=4, column=4, rowspan=2, sticky=E)
        self.yob.grid(row=4, column=5, rowspan=2)

        #Age
        self.agev = StringVar()
        self.avallabel = Label(self.gridframe, textvariable=self.agev,
                               font=('Helvetica',12),bg=self.bgcolor)\
                               .grid(row=4,column=6, rowspan=2)

        #Date Joined
        self.datejoinv = StringVar()
        self.djlabel = Label(self.gridframe, text="Date Joined:",
                             font=('Helvetica',12), bg=self.bgcolor)\
                             .grid(row=4,column=7,rowspan=2, sticky=E)
        self.djEntry = Entry(self.gridframe, textvariable=self.datejoinv,
                             bd=4).grid(row=4, column=8, rowspan=2)

        #VISIT INFORMATION SETUP
        self.thirdSep = ttk.Separator(self.gridframe, orient='horizontal')\
                        .grid(row=6,column=3,columnspan=40,sticky=EW)
        self.vilabel = Label(self.gridframe,text='Visit Information',
                             font=("Helvetica", 16),fg='white', bg='gray10')\
                             .grid(row=6,column=3,columnspan=12, sticky=W)
        self.datelab = Label(self.gridframe, text='Date: ',
                             font=('Helvetica',14), bg=self.bgcolor)\
                             .grid(row=7,column=3)
        self.notelab = Label(self.gridframe, text='Notes:',
                             font=('Helvetica',14), bg=self.bgcolor)\
                             .grid(row=7,column=4)
        self.vislab = Label(self.gridframe, text='Visitor: ',
                            font=('Helvetica',14),bg=self.bgcolor)\
                            .grid(row=7,column=7, padx=10)
        self.vollab = Label(self.gridframe, text='Volunteer: ',
                            font=('Helvetica',14),bg=self.bgcolor)\
                            .grid(row=9, column=7, padx=10)
        
        self.visit_listbox = Listbox(self.gridframe,height=4,width=15,font=12, bd=4)
        self.visit_listbox.bind('<<ListboxSelect>>', self.displayVisit)
        self.visit_listbox.config(exportselection=0)
        self.visit_scroll = Scrollbar(self.gridframe)
        self.visit_listbox.config(yscrollcommand=self.visit_scroll.set)
        self.visit_scroll.config(command=self.visit_listbox.yview)

        self.visit_listbox.grid(row=8, column=3, rowspan=4, columnspan=1, sticky=W)
        self.visit_scroll.grid(row=8, column=3, rowspan=4, columnspan=1, sticky=E+N+S)

        #Entry box for visit (when new visit is added)
        self.visdatev = StringVar()
        self.visitdate = Entry(self.gridframe,textvariable=self.visdatev,bd=4)
        #self.visitdate.grid(row=8, column=3)

        #visit notes
        self.notv = StringVar()
        self.notescv = Text(self.gridframe, state='disabled', width=50, height=4, bd=4, font='Helvetica')
        self.vnotes_scroll = Scrollbar(self.gridframe)
        self.notescv.config(yscrollcommand=self.vnotes_scroll.set)
        self.vnotes_scroll.config(command=self.notescv.yview)

        #visit notes
        self.notescv.grid(row=8, column=4, columnspan=3, rowspan=4, sticky=W, padx=10)
        self.vnotes_scroll.grid(row=8, column=4, rowspan=4, columnspan=3, sticky=E+N+S)

        #visit visitor
        self.visv = StringVar()
        self.visitor = Entry(self.gridframe,textvariable=self.visv,
                             state='readonly',bd=4)
        self.visitor.grid(row=8, column=7, rowspan=1, sticky=E, padx=10)

        #visit volunteer
        self.volv = IntVar()
        self.volun = Entry(self.gridframe,textvariable=self.volv,bd=4,
                           state='readonly')
        self.volun.grid(row=10, column=7, rowspan=1, padx=10)
        
        #Extra blank label
        self.blankLab2 = Label(self.gridframe, text='   ',
                               font=('Helvetica',10), bg=self.bgcolor)\
                               .grid(row=13,column=3, rowspan=2, sticky=E)
        #Visit buttons
        self.newVisit = Button(self.gridframe, text='New Visit', width=15,
                               command=self.newvisitf)
        self.newVisit.grid(row=8, column=8, sticky=W)

        self.editVisit = Button(self.gridframe, text='Edit Visit', width=15,
                                command=self.editvisitf)
        self.editVisit.grid(row=9, column=8, sticky=W)

        self.deleteVisit = Button(self.gridframe, text='Delete Visit', width=15,
                                  command=self.deletevisitf)
        self.deleteVisit.grid(row=10, column=8, sticky=W)
        
        #records/updates visit        
        self.saveVisit = Button(self.gridframe, text='Save Visit', width=15,
                                command=self.recordVisit)
        self.saveVisitE = Button(self.gridframe, text='Save Visit', width=15,
                                 command=self.savevisitf)
        #self.saveVisit.grid(row=8,column=8,sticky=W)
        self.cancelVisit = Button(self.gridframe, text='Cancel', width=15,
                                  command=self.cancelvisitf)
        #self.cancelVisit.grid(row=9, column=8, sticky=W)


        #HOUSEHOLD INFORMATION SETUP
        self.fourthSep = ttk.Separator(self.gridframe, orient='horizontal')\
                    .grid(row=15,column=3,columnspan=40,sticky=EW)
        self.hilabel = Label(self.gridframe,text='Household Information',
                        font=("Helvetica", 16),fg='white', bg='gray10')\
                        .grid(row=15,column=3,columnspan=12, sticky=W)
        #blank line
        self.hiblank = Label(self.gridframe, text='   ',font=('Helvetica',10),
                        bg=self.bgcolor).grid(row=16,column=3,sticky=E)

        #street address
        self.adv = StringVar()
        self.adlab = Label(self.gridframe, text='Address: ',
                           font=('Helvetica',12), bg=self.bgcolor)\
                           .grid(row=17,column=3, rowspan=2, sticky=E)
        self.address = Entry(self.gridframe,textvariable=self.adv,
                             width=40,bd=4)
        self.address.grid(row=17, column=4,columnspan=2, rowspan=2)

        #apartment
        self.apv = StringVar()
        self.aplab = Label(self.gridframe, text='Apt: ',font=('Helvetica',12),
                           bg=self.bgcolor).grid(row=17,column=6,
                                                 rowspan=2, sticky=E)
        self.aptn = Entry(self.gridframe,textvariable=self.apv,width=10,bd=4)
        self.aptn.grid(row=17,column=7, rowspan=2, sticky=W)

        #city
        self.ctyv = StringVar()
        self.cilab = Label(self.gridframe, text='City: ',font=('Helvetica',12),
                      bg=self.bgcolor).grid(row=17,column=8, rowspan=2, sticky=E)
        self.city = Entry(self.gridframe,textvariable=self.ctyv,bd=4)
        self.city.grid(row=17,column=9, rowspan=2, sticky=W)

        #state
        self.stav = StringVar()
        self.stlab = Label(self.gridframe, text='State: ',
                           font=('Helvetica',12), bg=self.bgcolor)\
                           .grid(row=20,column=3, rowspan=2, sticky=E)
        self.state = Entry(self.gridframe,textvariable=self.stav,bd=4)
        self.state.grid(row=20,column=4, rowspan=2)

        #zip
        self.zpv = StringVar()
        self.zilab = Label(self.gridframe, text='Zip Code: ',font=('Helvetica',12),
                      bg=self.bgcolor).grid(row=20, column=5, rowspan=2, sticky=E)
        self.zipc = Entry(self.gridframe,textvariable=self.zpv,bd=4)
        self.zipc.grid(row=20, column=6, rowspan=2)

        #Date Verified
        self.dverilabel = Label(self.gridframe, text='Last Verified: ',
                              font=('Helvetica',12),bg=self.bgcolor)\
                              .grid(row=20,column=7, rowspan=2, sticky=E)
        self.mvv = StringVar()
        self.dvv = StringVar()
        self.yvv = StringVar()

        self.mvv.set("")
        self.dvv.set("")
        self.yvv.set("")
        
        #for month entry
        self.mov = ttk.Combobox(self.gridframe, width=10, state='readonly',
                                values=self.month_li, textvariable=self.mvv)
        #self.mob.bind('<<ComboboxSelected>>', self.monthbox_select)
        
        #for day entry
        self.dov = Spinbox(self.gridframe, from_=0, to=0,
                           textvariable=self.dvv, width=5, bd=4)
        #for year entry
        self.yov = Spinbox(self.gridframe, from_=1900, to=2500,
                           textvariable=self.yvv, width=9, bd=4)
        
        self.mov.grid(row=20, column=8, rowspan=2, sticky=E, padx=10)
        self.dov.grid(row=20, column=9, columnspan=2, rowspan=2, padx=10, sticky=W)
        self.yov.grid(row=20, column=10, rowspan=2, padx=10, sticky=W)


        #formatting labels/objects
        self.blankLab5 = Label(self.gridframe, text='   ',
                               font=('Helvetica',12), bg=self.bgcolor)\
                               .grid(row=23,column=3,sticky=E)
        self.blankLab6 = Label(self.gridframe, text='   ',
                               font=('Helvetica',10), bg=self.bgcolor)\
                               .grid(row=25,column=3,sticky=E)
        self.fifthsep = ttk.Separator(self.gridframe, orient='horizontal')\
                        .grid(row=27,column=3,columnspan=40,sticky=EW, pady=10)
        
        #The following variables will be removed and re-gridded
        #as the function of the interface changes.
        #

        #HOUSEHOLD MEMBERS SETUP
        #These variables appear on the updateClientDisplay only
        #
        #info display widgets
        self.adl = StringVar()
        self.dispad = Label(self.gridframe,textvariable=self.adl,
                            font=('Helvetica',12),bg=self.bgcolor)
        self.chil = StringVar()
        self.dischil = Label(self.gridframe,textvariable=self.chil,
                             font=('Helvetica',12),bg=self.bgcolor)
        self.sen = StringVar()
        self.dissen = Label(self.gridframe,textvariable=self.sen,
                            font=('Helvetica',12),bg=self.bgcolor)
        self.inf = StringVar()
        self.disinf = Label(self.gridframe,textvariable=self.inf,
                       font=('Helvetica',12),bg=self.bgcolor)
        self.tot = StringVar()
        self.distot = Label(self.gridframe, textvariable=self.tot,
                            bg=self.bgcolor,font=('Helvetica',12))

        self.houseSep = ttk.Separator(self.gridframe, orient='horizontal')
        self.houseSep.grid(row=23,column=3,columnspan=40,sticky=EW)
        self.housetitle = Label(self.gridframe,text='Household Members',
                                font=("Helvetica", 16),fg='white',bg='gray10')
        self.housetitle.grid(row=23,column=3,columnspan=12, sticky=W)  

        #listbox of family members
        self.family_listbox = Listbox(self.gridframe,height=5,width=35,font=12)
        self.family_listbox.config(exportselection=0)
        self.fam_scroll = Scrollbar(self.gridframe)
        self.family_listbox.config(yscrollcommand=self.fam_scroll.set)
        self.fam_scroll.config(command=self.family_listbox.yview)
        
        self.family_listbox.grid(row=24, column=3, rowspan=3, columnspan=2, sticky=W)
        self.fam_scroll.grid(row=24, column=4, rowspan=3, columnspan=1, sticky=E+N+S)

        #family member buttons
        self.addmemb = Button(self.gridframe, text='Add Member', width=14,
                              command=self.addMemberEntryBoxes)
        self.addmemb.grid(row=24,column=5,sticky=E+N+S)
        self.removmemb = Button(self.gridframe, text='Remove Member',width=14,
                                command=self.removeMemberConfirm)
        self.removmemb.grid(row=25,column=5,sticky=E+N+S)
        self.viewmemb = Button(self.gridframe, text='View Member',width=14,
                               command=self.runViewMember)
        self.viewmemb.grid(row=26,column=5,sticky=E+N+S)

        #update save/cancel buttons
        self.saveB = Button(self.gridframe, text='Save Changes',
                            command=self.updateInfo,width=20)
        self.saveB.grid(row=28, column=3, columnspan=2)

        self.cancelB = Button(self.gridframe, text='Cancel Changes',
                              command=self.cancel_changes,width=20)
        self.cancelB.grid(row=28, column=5, columnspan=2)

        #NEW CLIENT DISPLAY WIDGETS
        #These variables appear on the newClientDisplay only
        #

        self.addhhsep = ttk.Separator(self.gridframe, orient='horizontal')
        self.addhhtitle = Label(self.gridframe,text='Add Household Members',
                                font=("Helvetica", 16),fg='white',bg='gray10')
        
        #add members to new household variable
        self.q = IntVar()
        self.famNum = Entry(self.gridframe, textvariable=self.q)
        self.entNum = Label(self.gridframe,
                            text='Total Family Members: ',
                            font=('Helvetica',10),bg=self.bgcolor)
        self.famname = Label(self.gridframe, text='Name:',
                             font=('Helvetica',10),bg=self.bgcolor)
        self.famfn = Label(self.gridframe, text='First Name:',
                           font=('Helvetica',10),bg=self.bgcolor)
        self.famln = Label(self.gridframe, text='Last Name:',
                           font=('Helvetica',10),bg=self.bgcolor)
        self.famdob = Label(self.gridframe, text='Date of Birth:',
                            font=('Helvetica',10),bg=self.bgcolor)
        self.famphone = Label(self.gridframe, text='Phone',
                              font=('Helvetica',10),bg=self.bgcolor)
        self.fammon = Label(self.gridframe,text='mm',
                            font=('Helvetica',10),bg=self.bgcolor)
        self.famday = Label(self.gridframe,text='dd',
                            font=('Helvetica',10),bg=self.bgcolor)
        self.famyear = Label(self.gridframe,text='yyyy',
                             font=('Helvetica',10),bg=self.bgcolor)
   
        self.newMembersB = Button(self.gridframe, text='Add Members',
                                  command=self.familyEntryBoxes)
        self.newClientSave = Button(self.gridframe, text='Save Client',
                                    command=self.addNew)
        self.cancelNewB = Button(self.gridframe, text='Cancel New Entry',
                                 command=self.newClientDisplay)

        
        #MENU SETUP
        self.menubar = Menu(self.ciGui)
    
        #^Essentially re-selects client

        self.volmenu = Menu(self.menubar, tearoff=0)
        self.volmenu.add_command(label='Log Off', command=self.logoff)
        self.volmenu.add_command(label='Configure Color', command=self.configure_background)
        self.menubar.add_cascade(label='Volunteers',menu=self.volmenu)
        
        self.optionsmenu = Menu(self.menubar,tearoff=0)
        self.optionsmenu.add_command(label='Quit', command=self.quitprogram)
        #self.optionsmenu.add_command(label='Change Instructions', command=self.edit_instructions)
        
        self.menubar.add_cascade(label='Options',menu=self.optionsmenu)

        #Reports Menu
        self.reportmenu = Menu(self.menubar,tearoff=0)
        self.reportmenu.add_command(label='View Weekly Report',
                                    command=self.weeklyReport)
        self.reportmenu.add_command(label='View Monthly Report',
                                    command=self.monthlyReport)
        self.reportmenu.add_command(label='View Yearly Report',
                                    command=self.yearlyReport)
        self.menubar.add_cascade(label='Reports',menu=self.reportmenu)

        #add menubar to grid
        self.ciGui.config(menu=self.menubar)

        #instructive labels
        self.instructions = Text(self.gridframe, bd=4, width=20, font=('Helvetica', 12), wrap=WORD)
        f = open('instructions.txt', 'r')
        instruct = f.read()
        f.close()
        self.instructions.insert('1.0', instruct)

                                 #"Questions to Ask:\n" +\
                                  #      "\n1. Has anything changed in your "+\
                                   #     "family composition?\n"+\
                                    #    "\nReminders:\n"+\
                                     #   "\n1. If family has infants, mention"+\
                                      #  " the Alight Care Center offers "+\
                                       # "clothing and diapers.\n"+\
                                        #"\n2. If family has children, see if"+\
                                        #" there are any milk cards in the "+\
                                        #"drawer, and offer them one if "+\
                                        #"there is."
                                        #)
        self.i_scroll = Scrollbar(self.gridframe)
        self.instructions.config(yscrollcommand=self.i_scroll.set)
        self.i_scroll.config(command=self.instructions.yview)
        self.instructions.grid(row=14, column=0, rowspan=20, columnspan=2, padx=10)
        self.i_scroll.grid(row=14, column=0, rowspan=20, columnspan=2, sticky=E+N+S, padx=10)

        #Sets some sizing stuff
        for i in range(0, 10):
            self.ciGui.columnconfigure(i, weight=1, minsize=10)

        for i in range(0, 30):
            self.ciGui.rowconfigure(i, weight=1, minsize=10)
        
        for i in range(7, 11):
            self.ciGui.rowconfigure(i, weight=1, minsize=20)
            
        self.ciGui.rowconfigure(18, weight=1, minsize=25)

        
        #mainloop
        self.newClientDisplay()
        self.ciGui.mainloop()


    #DISPLAY SCREENS

    def newClientDisplay(self):
        """This function will clear all irrelevant widgets, and
        grid all widgets necessary for the new client screen.
        """
	    #clear widgets
        self.clearEntries()
        
	    #grid widgets
        self.addhhsep.grid(row=23,column=3,columnspan=40,sticky=EW, pady=10)
        self.addhhtitle.grid(row=23,column=3,columnspan=12, sticky=W, pady=10)
        self.famNum.grid(row=24, column=4)
        self.entNum.grid(row=24, column=3)
        self.newMembersB.grid(row=24, column=5)
        self.newClientSave.grid(row=40,column=3, columnspan=2)
        self.cancelNewB.grid(row=40, column=5, columnspan=2)

        self.newvisitf()
        self.saveVisit.grid_forget()
        self.cancelVisit.grid_forget()
        return


    def updateClientDisplay(self):
        """This function will clear all irrelevant widgets and
        grid all widgets necessary for the updating-client screen.
        """
        #clear widgets
        self.clearEntries()
			
	#grid widgets
        self.family_listbox.grid(row=24, column=3, rowspan=3, columnspan=2, sticky=W)
        self.fam_scroll.grid(row=24, column=4, rowspan=3, columnspan=1, sticky=E+N+S)
        self.addmemb.grid(row=24,column=5,sticky=E+N+S)
        self.removmemb.grid(row=25,column=5,sticky=E+N+S)
        self.viewmemb.grid(row=26,column=5,sticky=E+N+S)
        self.housetitle.grid(row=23,column=3,columnspan=12, sticky=W) 
        self.houseSep.grid(row=23,column=3,columnspan=40,sticky=EW)
        self.saveB.grid(row=28, column=3, columnspan=2)
        self.cancelB.grid(row=28, column=5, columnspan=2)
        return

		
    #DISPLAY FOR SELECTED CLIENTS
	
    def displayInfo(self, *args):
       """This function displays the information for a client that
       has been selected in the client_listbox.
       """
       try:
           self.cursel = int(self.id_list[self.client_listbox.curselection()[0]])
           info = select_client(self.cursel)
           self.info = info
           self.updateClientDisplay()
       
           self.displayHouseholdMem(info)
           self.displayVisitInfo(info)
           self.displayClientInfo(info)
           self.displayHouseholdInfo(info)
       except IndexError:
           pass       
       return


    def displayNewInfo(self, client_id):
       """This function displays the information for a specified
       client whose id is client_id.
       """
       cursel = client_id 
       info = select_client(cursel)
       self.info = info
       self.updateClientDisplay()
       
       self.displayHouseholdMem(info)
       self.displayVisitInfo(info)
       self.displayClientInfo(info)
       self.displayHouseholdInfo(info)
       
       return
 
 
    #DISPLAY INFORMATION FUNCTIONS
		
    def displayClientInfo(self, info, *args):
       """This function displays the client information.
       """
	   #retrieve info from dictionary
       visitor = info["visitor"]
       
	   #set variables
       self.fnv.set(visitor.firstname)
       self.lnv.set(visitor.lastname)
       month = self.month_int[visitor.dob.month]
       self.mv.set(month)
       self.dv.set(visitor.dob.day)
       self.yv.set(visitor.dob.year)
       self.phv.set(visitor.phone)
	   
       #parse and set datejoined
       joined = str(visitor.dateJoined.month) + "/" +\
                str(visitor.dateJoined.day) + "/" +\
                str(visitor.dateJoined.year)
       self.datejoinv.set(joined)

       #set age 
       ad=str(age(visitor.dob))
       a="Age: "
       ad=str(a+ad)
       self.agev.set(ad)
       return


    def displayHouseholdInfo(self, info, *args):
       """This function displays the household information for
       a client.
       """
       #retrieve info from dictionary
       house = info["household"]
	   
       #set variables
       self.adv.set(house.street)
       self.apv.set(house.apt)
       self.ctyv.set(house.city)
       self.stav.set(house.state)
       self.zpv.set(house.zip)

       #check dateVerified, and set variables accordingly
       if house.dateVerified != None:
           month = house.dateVerified.month
           self.mvv.set(self.month_int[month])
           self.dvv.set(house.dateVerified.day)
           self.yvv.set(house.dateVerified.year)

       #parse and set label variables for all members
       ad=str(info["agegroup_dict"]["adults"])
       a="Adults: "
       ad=str(a+ad)
       self.adl.set(ad)
       
       ch=str(info["agegroup_dict"]["children"])
       c="Children: "
       ch=c+ch
       self.chil.set(ch)
       
       sn=str(info["agegroup_dict"]["seniors"])
       s="Seniors: "
       sn=s+sn
       self.sen.set(sn)
       
       infa=str(info["agegroup_dict"]["infants"])
       i="Infants: "
       infa=i+infa
       self.inf.set(infa)

       tl = str(info["agegroup_dict"]["total"])
       t="Total: "
       tl = t+tl
       self.tot.set(tl)
       
       #grid family member labels
       self.dispad.grid(row=22,column=3,sticky=W, pady=10)
       self.dischil.grid(row=22,column=4,sticky=W)
       self.dissen.grid(row=22,column=5,sticky=W)
       self.disinf.grid(row=22,column=6,sticky=W)
       self.distot.grid(row=22,column=7,sticky=W)
       return


    def displayVisitInfo(self, info, *args):
       """This function display the visit information for a client.
       """
       self.clearVisits()
       self.visitDict = {}
       
       visitor = info["visitor"]

       name = str(visitor.firstname)+ " " +str(visitor.lastname)
       self.visv.set(name)

       #visit info
       visits = info["visit_list"]

       if len(visits) == 0:
           pass
        
       else: 
           vdatelabs = []
           vnlabs = []
           vvisitors = []
           vvols = []
           vids = []
           
           for v in visits:
               d=str(v.date.month)+'/'+str(v.date.day)+'/'+str(v.date.year)
               n=v.notes
               vi=v.visitor
               vol=v.volunteer
               vid=v.visitID

               vdatelabs.append(d) 
               vnlabs.append(n) 
               vvisitors.append(vi) 
               vvols.append(vol)
               vids.append(vid)

           #set variables to display first visit 
           self.visv.set(vvisitors[0])
           self.volv.set(vvols[0])
           self.notv.set(vnlabs[0])

           self.notescv.config(state='normal')
           self.notescv.insert('1.0', vnlabs[0])
           self.notescv.config(state='disabled')

           #save lists in dictionary
           self.visitDict['dates'] = vdatelabs
           self.visitDict['notes'] = vnlabs
           self.visitDict['visitors'] = vvisitors
           self.visitDict['volunteers'] = vvols
           self.visitDict['ids'] = vids

           for i in range(0, len(vdatelabs)): 
               self.visit_listbox.insert(i, vdatelabs[i])
           self.visit_listbox.selection_set(0) 
       
           
    def displayVisit(self, *args):
        """This function will display the data for a visit when
        a visit date is selected.
        """
        try:
            self.notescv.config(state='normal')
            self.notescv.delete('1.0', END)
            datev = int(self.visit_listbox.curselection()[0])
            self.selectedVisit = datev
            n = self.visitDict['notes']
            vi = self.visitDict['visitors']
            vol = self.visitDict['volunteers']

            self.visv.set(vi[datev])
            self.volv.set(vol[datev])
            self.notv.set(n[datev])
            notes = str(self.notv.get())
            self.notescv.insert('1.0', notes)
            self.notescv.config(state='disabled')
        except IndexError:
            pass
        

    def displayHouseholdMem(self, info, *args):
       """This function displays the household information for a client.
       """ 
       self.family_listbox.delete(0,END)
       a=[]
       del self.mem_list[:]
       for member in info["member_list"]:
           self.mem_list.append(member.id)
           s=str(age(member.dob))
           q='Age: '
           s=q+s
           x=(member.firstname, member.lastname,s)
           a.append(x)

       for i in range(len(a)):
           self.family_listbox.insert(i,a[i])
       

	
	#DISPLAY EXTRA ENTRY BOXES FOR ADDITIONAL FAMILY MEMBERS
	
	#BUG: WHEN Add Member IS PRESSED MORE THAN ONCE, EXTRA 
	#BOXES HANG AROUND, AND ARE NEVER CLEARED
	    
    def familyEntryBoxes(self, *args):
       """This function generates entry boxes for adding new family members.
       The entry boxes are saved in list form and added to the dictionary
       memDict.
       """
       #clears any boxes already displayed
       self.clearFamily()
       
       try:
           n = int(self.q.get())
       except ValueError:
           return
        
       #add instructive labels to grid
       self.famfn.grid(row=25,column=3)
       self.famln.grid(row=25,column=4)
       self.famdob.grid(row=25,column=5)
       self.famphone.grid(row=25,column=8)

       #create lists
       fnames = []
       lnames = []
       mm = []
       dd = []
       yy = []
       phnum = []

       #create entry boxes, grid them, and append them to a list
       for i in range(0, n):
           fname = Entry(self.gridframe)
           fname.grid(row=26+i, column=3)
           fnames.append(fname)
           
           lname = Entry(self.gridframe)
           lname.grid(row=26+i, column=4)
           lnames.append(lname)

           month = ttk.Combobox(self.gridframe, width=12, state='readonly',
                              values=self.month_li)
           #month.bind('<<ComboboxSelected>>', self.monthbox_select)
           month.grid(row=26+i, column=5)
           mm.append(month)
           
           day = Spinbox(self.gridframe, from_=0, to=0, width=5)
           day.grid(row=26+i, column=6)
           dd.append(day)
           
           year = Spinbox(self.gridframe, from_=1900, to=2500, width=7)
           year.grid(row=26+i, column=7)
           yy.append(year)
           
           phone = Entry(self.gridframe)
           phone.grid(row=26+i, column=8)
           phnum.append(phone)
           

       #add all lists to dictionary
       self.memDict["first"] = fnames
       self.memDict["last"] = lnames
       self.memDict["mm"] = mm
       self.memDict["dd"] = dd
       self.memDict["yy"] = yy
       self.memDict["phone"] = phnum


    def addMemberEntryBoxes(self, *args):
        """This function generates entry boxes for adding new family members.
        The entry boxes are saved in list form and added to the dictionary
        memDict.
        """
        if self.addmemberON == True:
           pass
        
        else:   
            #add instructive labels to grid
            self.famfn.grid(row=24,column=6) #, sticky=NE)
            self.famln.grid(row=24,column=8) #, sticky=NE)
            self.famdob.grid(row=25,column=6)
            self.famphone.grid(row=26,column=6)

            #create entry boxes, grid them, and append them to a list
            #first name 
            self.fname = Entry(self.gridframe)
            self.fname.grid(row=24, column=7, sticky=W)
            self.memDict["first"]=[self.fname]

            #last name
            self.lname = Entry(self.gridframe)
            self.lname.grid(row=24, column=9, sticky=W)
            self.memDict["last"]=[self.lname]

            #dob: month 
            self.month = ttk.Combobox(self.gridframe, width=12, state='readonly',
                                  values=self.month_li)
            #self.month.bind('<<ComboboxSelected>>', self.monthbox_select)
            self.month.grid(row=25, column=7, sticky=W)
            self.memDict["mm"]=[self.month]

            #dob: day 
            self.day = Spinbox(self.gridframe, from_=0, to=0, width=5)
            self.day.grid(row=25, column=8, sticky=W)
            self.memDict["dd"]=[self.day]

            #dob: year
            self.year = Spinbox(self.gridframe, from_=1900, to=2500, width=7)
            self.year.grid(row=25, column=9, sticky=W)
            self.memDict["yy"]=[self.year]

            #phone
            self.phone = Entry(self.gridframe)
            self.phone.grid(row=26, column=7, sticky=W)
            self.memDict["phone"]=[self.phone]

            #self.addmemberON = True
            

	 
	#CLEAR WIDGETS FUNCTIONS

    def clearVisits(self):
        """This function clears the entry boxes/visit notes
        used for visits.
        """
        self.visit_listbox.delete(0, END)
        self.visv.set("")
        self.volv.set("")
        self.notv.set("")
        self.notescv.config(state='normal')
        self.notescv.delete('1.0', END)
        self.notescv.config(state='disabled')

        visitob = [self.visit_listbox, self.visit_scroll, self.visitdate,
                   self.newVisit, self.editVisit, self.deleteVisit,
                   self.saveVisit, self.saveVisitE, self.cancelVisit]
        for ob in visitob:
            ob.grid_forget()

        self.visit_listbox.grid(row=8, column=3, rowspan=4, columnspan=1, sticky=W)
        self.visit_scroll.grid(row=8, column=3, rowspan=4, columnspan=1, sticky=E+N+S)
        self.newVisit.grid(row=8, column=8, sticky=W)
        self.editVisit.grid(row=9, column=8, sticky=W)
        self.deleteVisit.grid(row=10, column=8, sticky=W)
        
       
    def clearFamily(self):
       #forgets additional family members
       self.family_listbox.delete(0, END)
       
       try:
           mfname = self.memDict["first"]
           mlname = self.memDict["last"]
           mm = self.memDict["mm"]
           dd = self.memDict["dd"]
           yy = self.memDict["yy"]
           phnum = self.memDict["phone"]
           easylist = [mfname, mlname, mm, dd,
                       yy, phnum]
           for i in range(0, 6):
              for j in range(0, len(easylist[i])):
                  easylist[i][j].grid_forget()
           for i in range(0, 6):
              easylist[i] = []
           self.memDict = {}

       except KeyError:
           pass
        

    def clearEntries(self):
       """This function clears the entry boxes that will never be
       removed from the display.
       """
              
       allvaries = [self.fnv, self.lnv, self.phv, self.mv, self.dv, self.yv,
                    self.adv, self.apv, self.q, self.agev,
                    self.notv, self.volv, self.visv, self.adl, self.chil,
                    self.sen, self.inf, self.tot, self.datejoinv, self.mvv,
                    self.dvv, self.yvv]
       
       #Clears the entryboxes
       for i in range(0, len(allvaries)):
          allvaries[i].set("")

       #sets defaulted entries
       today = datetime.now()
       todaystr = str(today.month)+'/'+str(today.day)+\
                         '/'+str(today.year)
       #self.visdatev.set(todaystr)
       self.datejoinv.set(todaystr)
       self.ctyv.set("Troy")
       self.stav.set("NY")
       self.zpv.set(12180)

       #new client stuff
       
       allforgets = [self.family_listbox,
                     self.fam_scroll, self.addmemb, self.removmemb,
                     self.viewmemb, self.housetitle, self.houseSep, self.saveB,
                     self.cancelB, self.dispad, self.dischil, self.dissen,
                     self.disinf, self.distot, self.addhhsep, self.addhhtitle,
                     self.famNum, self.entNum, self.newMembersB,
                     self.newClientSave, self.cancelNewB, self.famname,
                     self.famfn, self.famln, self.famdob, self.famphone,
                     self.fammon, self.famday, self.famyear]
       
       
       for i in range(0, len(allforgets)):
          allforgets[i].forget()
          allforgets[i].grid_forget()
       
       #forgets additional family members
       #self.family_listbox.delete(0, END)
       self.clearFamily()
       
       #forgets previous visit notes
       self.clearVisits()
       self.visitDict = {}
 
	   
    def monthbox_select(self, *args):
        """This function is called when a month is selected from the
        month combobox. It will look up the month in the month_day_dict,
        and assign the right number of days to the "dob" spinbox.
        """
        month = self.mv.get()
        days = self.month_day_dict[month]
        self.dob.config(from_=1, to=days)
        return


    #visit buttons
    def newvisitf(self):
        """This function will clear unnecessary widgets, add an entrybox
        for the date, and prepopulate the date, volunteer, and visitor fields.
        """
        #clear Notes, Vol, & Visitor
        self.visit_listbox.grid_forget()
        self.visit_scroll.grid_forget()
        self.newVisit.grid_forget()
        self.editVisit.grid_forget()
        self.deleteVisit.grid_forget()

        #set date of visit to today 
        today = datetime.now()
        tstr = str(today.month) + "/" + str(today.day) + "/" + str(today.year)
        self.visdatev.set(tstr)
        self.visitdate.grid(row=8, column=3)

        #prepopulate volunteer
        self.volv.set(self.volunteerName)
        #prepopulate visitor (add test to see if this exists, in case of newclient)
        self.notescv.config(state='normal')
        self.notescv.delete('1.0', END)
        self.saveVisit.grid(row=8, column=8, sticky=W)
        self.cancelVisit.grid(row=9, column=8, sticky=W)


    def editvisitf(self):
        """This function sets up a display identical to the "new visit"
        display, but the date, visitor, notes, and volunteer are all
        prepopulated with information from the database.
        """
        #gridding
        self.visit_listbox.grid_forget()
        self.visit_scroll.grid_forget()
        self.newVisit.grid_forget()
        self.editVisit.grid_forget()
        self.deleteVisit.grid_forget()

        #set volunteer from database
        self.volv.set(self.visitDict['volunteers'][self.selectedVisit])
        
        #set visitor from database
        self.visv.set(self.visitDict['visitors'][self.selectedVisit])
        
        #set visdatev to Visit Date from database
        vdate = self.visitDict['dates'][self.selectedVisit]
        self.visdatev.set(vdate)
        self.visitdate.grid(row=8, column=3)

        self.notescv.config(state='normal')
        self.saveVisitE.grid(row=8, column=8, sticky=W)
        self.cancelVisit.grid(row=9, column=8, sticky=W)

        
    def cancelvisitf(self):
        """This function will cancel a visit/changes to a visit,
        and return to the normal visit display.
        """
        self.clearVisits()
        d = self.visitDict["dates"]
        for i in range(0, len(d)): 
               self.visit_listbox.insert(i, d[i])
        self.visit_listbox.selection_set(0)
        self.displayVisit()
        

    def savevisitf(self):
        """this will connect to Update Visit"""
        try:
            notes = str(self.notescv.get('1.0', END))
            d = str(self.visdatev.get())
            da = d.split('/')
            dat = date(month=int(da[0]), day=int(da[1]), year=int(da[2]))
        except:
            self.error_popup("Check the visit date!")
        
        idlist = self.visitDict['ids']
        vid = idlist[self.selectedVisit]

        update_vis(vid, dat, notes)

        #refresh screen
        self.clearVisits()
        pid = self.cursel
        info = select_client(pid)
        self.displayVisitInfo(info)
        
    
    def deletevisitf(self):
        """This function will delete the selected visit, first asking
        the user to confirm the action, and will update the visit display
        to reflect the change. This function connects to the "delete visit"
        button.
        """
        conf = messagebox.askquestion(
            title='Confirm Delete',
            message='Are you sure you want to delete this visit?')
        if conf == 'yes':
            idlist = self.visitDict['ids']
            vid = idlist[self.selectedVisit]
            remove_visit(vid)
            
            #refresh screen
            self.clearVisits()
            pid = self.cursel
            info = select_client(pid)
            self.displayVisitInfo(info)
            return
        else:
            return    

        
    def cancel_changes(self):
        """This function will clear the display and refill it with
        the selected client's information from the database.
        """
        self.updateClientDisplay()
        self.displayInfo()
        return

    
    def quitprogram(self):
        """This function safely closes the database and
        interface window.
        """
        quit_session()
        self.ciGui.destroy()
        return
       

    def logoff(self):
        """This function closes the database and interface window,
        and returns to the volunteer login page.
        """
        quit_session()
        self.ciGui.destroy()
        vo = cdbvolunteer.VolunteerDisplay()
        return


    def monthlyReport(self):
        generate_monthly_report()
        return

    def yearlyReport(self):
        generate_yearly_report()
        return

    def weeklyReport(self):
        generate_weekly_report()
        return


    def error_popup(self, errmessage):
        """This function implements a simple pop-up window to warn user
        about bad data entry.
        """
        conf = messagebox.showerror(title='Error', message=errmessage)

       
    def recordVisit(self):
        """This function will insert a new visit, clear old visit
        display info, and reset the visit display.
        """
        #inserts new visit
        try:
            vol_id = self.volID #int(self.volv.get())
        except ValueError:
            self.error_popup("Check volunteer id")
            return

        #get visit date
        try:
            dv = (str(self.visdatev.get())).split('/')
            dvm = int(dv[0])
            dvd = int(dv[1])
            dvy = int(dv[2])
            vdate = date(year=dvy, month=dvm, day=dvd)
        except ValueError:
            self.error_popup("Check visit date field!\n Enter: MM/DD/YYYY")
            return

        #get visit notes
        try:
            note = self.notescv.get("1.0", END)
        except ValueError:
           self.error_popup("Uh, oh! Better check the visit info!")
           return

        #create visitData object, and call function to record new visit    
        visitInfo = visitData(vol_id, visitDate=vdate, notes=note)
        new_visit(self.cursel, visitInfo)
           
        #clears old visit notes
        self.clearVisits()
        
        #refreshes visit note display
        info = select_client(self.cursel)
        self.displayVisitInfo(info)
        
  
    #"Get All Input and Test It" functions
    
    def getVisitorInput(self, ctype, cID=None):
        """This function tests all of the data for the visitor
        entry boxes and returns an object.
        """
        #Error checking for visitor's name and phone
        try:
            fname = str(self.fnv.get())
        except ValueError:
            self.error_popup("Check visitor's first name!")
            return
        try:
            lname = str(self.lnv.get())
        except ValueError:
            self.error_popup("Check visitor's last name!")
            return
        try:
            phnum = str(self.phv.get())
        except ValueError:
            self.error_popup("Check visitor's phone number!")
            return
         #Error checking for visitor's DOB
        try:
            month = str(self.mv.get())
            dm = self.int_month[month]
        except ValueError and KeyError:
            self.error_popup("Check visitor's month of birth!")
            return
        try:
            dd = int(self.dv.get())
        except ValueError:
            self.error_popup("Check visitor's day of birth!")
            return
        try:
            dy = int(self.yv.get())
        except ValueError:
            self.error_popup("Check visitor's year of birth!")
            return
        try:
            DOB = date(year=dy, month=dm, day=dd)
        except ValueError:
            self.error_popup("Was an invalid day of birth chosen?")
            return

        #Error checking for datejoined
        try:
            dj = (str(self.datejoinv.get())).split('/')
            djm = int(dj[0])
            djd = int(dj[1])
            djy = int(dj[2])
            datejoined = date(year=djy, month=djm, day=djd)
        except ValueError:
            self.error_popup("Check Date Joined field!\n Enter: MM/DD/YYYY")
            return

        if ctype == "old":                          
            cd = oldClientData(cID, firstname=fname, lastname=lname,
                               dob=DOB, phone=phnum, dateJoined=datejoined)
        elif ctype == "new":
            cd = newClientData(firstname=fname, lastname=lname,
                               dob=DOB, phone=phnum, dateJoined=datejoined)
        return cd


    def getMemberInput(self, clist):
        """This function tests all of the input data for members
        entry boxes and returns a data object.
        """
        
        #Error checking for datejoined
        try:
            dj = (str(self.datejoinv.get())).split('/')
            djm = int(dj[0])
            djd = int(dj[1])
            djy = int(dj[2])
            datejoined = date(year=djy, month=djm, day=djd)
        except ValueError:
            self.error_popup("Check Date Joined field!\n Enter: MM/DD/YYYY")
            return

        #Check to see if any
        if self.memDict != {}:          
            mfname = self.memDict["first"]
            mlname = self.memDict["last"]
            mm = self.memDict["mm"]
            dd = self.memDict["dd"]
            yy = self.memDict["yy"]
            phnum = self.memDict["phone"]

            for i in range(0, len(mfname)):
                try:
                    fname = str(mfname[i].get())
                except ValueError:
                    self.error_popup("Check family member "+str(i)+"'s first name!")
                    return
                try:
                    lname = str(mlname[i].get())
                except ValueError:
                    self.error_popup("Check family member "+str(i)+"'s last name!")
                    return
                try:
                    phn = str(phnum[i].get())
                except ValueError:
                    self.error_popup("Check family member "+str(i)+"'s phone!")
                    return
                try:
                    month = str(mm[i].get())
                    dm = self.int_month[month]
                except ValueError and KeyError:
                    self.error_popup("Check family member "+str(i)\
                                     +"'s month of birth!")
                    return
                try:
                    dday = int(dd[i].get())
                except ValueError:
                    self.error_popup("Check family member "+str(i)\
                                     +"'s day of birth!")
                    return
                try:
                    dy = int(yy[i].get())
                except ValueError:
                    self.error_popup("Check family member "+str(i)\
                                     +"'s year of birth!")
                    return
                try:
                    DOB = date(year=dy, month=dm, day=dday)
                except ValueError:
                    self.error_popup("Was an invalid day of birth chosen for"\
                                     " family member "+str(i)+"?")
                    return
                            
                ncd = newClientData(firstname=fname, lastname=lname,
                                    dob=DOB, phone=phn, dateJoined=datejoined)
                clist.append(ncd)
                
        return clist


    def getHouseholdInput(self):
        """This function tests all input for households in the household
        entry boxes, and returns a data object.
        """

        #get street address
        try:
            streeta = str(self.adv.get())
        except ValueError:
            self.error_popup("Check street address!")
            return
        
        #get city
        try:
            citya = str(self.ctyv.get())
        except ValueError:
            self.error_popup("Check city!")
            return
        
        #get state
        try:
            statea = str(self.stav.get())
        except ValueError:
            self.error_popup("Check state!")
            return

        #get zip code
        try:
            zipa = int(self.zpv.get())
        except ValueError:
            self.error_popup("Check zip code!")
            return

        #get apartment number
        try:
            apta = str(self.apv.get())
        except ValueError:
            self.error_popup("Check apartment number!")
            return
        
        #get date verified
        
        if self.mvv.get() == self.dvv.get() == self.yvv.get() == "":
            datev = None
            
        else:
            #get month
            try:
                month = str(self.mvv.get())
                vm = self.int_month[month]
            except ValueError and KeyError:
                self.error_popup("Check month of date verified!")
                return

            #get day
            try:
                vd = int(self.dvv.get())
            except ValueError:
                self.error_popup("Check day of date verified!")
                return

            #get year
            try:
                vy = int(self.yvv.get())
            except ValueError:
                self.error_popup("Check day of date verified!")
                return

            #final date testing
            try:
                datev = date(year=vy, month=vm, day=vd)
            except ValueError:
                self.error_popup("Was an invalid day for date"\
                                 +" verified chosen?")
                return
            
        houseInfo = houseData(street=streeta, city=citya, state=statea,
                                zip=zipa, apt=apta, dateVerified=datev)
        return houseInfo


    def getVisitInput(self):
        """This function tests all visit input and returns an object.
        """
        #IMPLEMENT get volunteer id
        try:
            v = str(self.visdatev.get())
            vd = v.split('/')
            vdate = date(year=int(vd[2]), month=int(vd[0]), day=int(vd[1]))
        except ValueError:
            self.error_popup("Check the visit date!")

        #get visit notes
        try:
            note = self.notescv.get("1.0", END)
        except ValueError:
            note = None
            
        visitInfo = visitData(Vol_ID=self.volID, visitDate=vdate, notes=note)
        return visitInfo
        
        
    def addNew(self):
        """This function adds a new household to the database.
        #NOTE: we need to check checkboxes for dummy addresses
        #(domestic violence address, and homeless address)
        """

        #What if one of our "gets" fail?
        
        #Test all input and create newClientData object for visitor
        cd = self.getVisitorInput("new")
        clist = [cd]

        newClientInfo_list = self.getMemberInput(clist)
        houseInfo = self.getHouseholdInput()
        visitInfo = self.getVisitInput()

        #send all objects to new_household function
        client_id = new_household(houseInfo, visitInfo, newClientInfo_list)
        self.cursel = client_id
    
        #refresh list of clients
        self.clientlist = list_people()

        #refresh screen
        self.displayNewInfo(client_id)
        


    def updateInfo(self, *args):
        """This function will update the visitor's information, the household
        information, and the visit information. It will also add family members,
        but it will NOT update the family members.
        """
        sel_id = self.cursel
        nclist = []
        
        cd = self.getVisitorInput("old", cID=sel_id)
        oldClientInfo_list = [cd]
        houseInfo = self.getHouseholdInput()        
        newClientInfo_list = self.getMemberInput(nclist)
        
        update_all(sel_id, houseInfo, oldClientInfo_list, newClientInfo_list)

        #refresh list of clients
        self.clientlist = list_people()

        #refresh screen
        #self.updateClientDisplay()
        self.displayNewInfo(self.cursel)
        
   
    def nameSearch(self, *args):
       """This function returns relevant results
       """

       #removes old listbox contents
       self.client_listbox.delete(0, END)
       del self.id_list[:]

       #get user input 
       name = str(self.ns.get())
       nameC = name.capitalize()
       
       #name = str(self.ns.get()).capitalize()
       #NOTE:Get lowercase names, too

       c = self.clientlist

       #find matching names in list
       found_clients = []
       for i in range(len(c)):
           if name in c[i][0] or nameC in c[i][0]:
               found_clients.append(c[i])

       found_clients.sort()

       #listing just the names and addresses of the people
       x=[]
       for i in range(len(found_clients)):
           dobstr=str(found_clients[i][1].month)+\
                   "/"+str(found_clients[i][1].day)+\
                   '/'+str(found_clients[i][1].year)
           a=str(found_clients[i][0])+" --"+dobstr
           
           x.append(a)
           self.id_list.append(found_clients[i][2])

       #insert results into listbox       
       for i in range(len(x)):
           self.client_listbox.insert(i,x[i])
       
       return
    

    def runViewMember(self):
        """This function displays the information for a client that
        has been selected in the family_listbox.
        """
        try:
            n = self.family_listbox.curselection()[0]
            self.cursel = self.mem_list[n]
            info = select_client(self.cursel)
       
            self.displayHouseholdMem(info)
            self.displayVisitInfo(info)
            self.displayClientInfo(info)
            self.displayHouseholdInfo(info)
        except IndexError:
            pass
        return

    
    def removeMemberConfirm(self):
        """This function removes a family member.
        """
        try:
            n = self.family_listbox.curselection()[0]
            tbd = self.mem_list[n]
            conf = messagebox.askquestion(
                title='Confirm Removal',
                message='Are you sure you want to delete this client?')
            if conf == 'yes':
                remove_client(tbd)
                self.updateInfo()           
                return
            else:
                return
            
        except IndexError:
            pass
        return


    def configure_background(self, *args):
        """This function takes in a string and, if it matches a
        valid color, will set the color of the interface to
        the new color.
        """
        import tkinter.colorchooser as cc
        color = cc.askcolor()
        color_name = color[1]
        self.bgcolor = color_name
        self.ciGui.configure(background=self.bgcolor)
        #for i in range(0, len(self.alllabs)):
         #    self.alllabs[i].configure(bg=self.bgcolor)
        self.cslabel.configure(self.gridframe, bg=self.bgcolor)
        #for lab in self.alllabs:
         #   lab.config(background=self.bgcolor)
        return
        #print(color_name)
        
