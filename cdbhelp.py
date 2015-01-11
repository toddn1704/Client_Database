"""cdbhelp.py

This file will define a window which displays help information.
"""

from tkinter import *
from tkinter import ttk

class cdbHelp:
    def __init__(self, tag):
        """This function defines a help window. It takes a tag
        as input; this tag specifies the type of help to display.
        
        Valid tags are the following:
        login, client, visit, household, members, search
        view?
        """
        
        self.bgcolor = 'light blue'

        #window
        self.helpwin = Tk()
        self.helpwin.configure(background=self.bgcolor)
        self.helpwin.title('Help')

        #text widget + scrollbar
        self.instruct = Text(self.helpwin, font=('Helvetica', 10), width=40,
                             height=10, wrap=WORD)
        self.instruct_scroll = Scrollbar(self.helpwin)
        self.instruct.config(yscrollcommand=self.instruct_scroll.set)
        self.instruct_scroll.config(command=self.instruct.yview)

        self.instruct.grid(row=3, column=1, padx=20, pady=10)
        self.instruct_scroll.grid(row=3, column=1, sticky=E+N+S, padx=20,
                                  pady=10)

        if tag == 'login':
            self.get_help('volunteer_help.txt')
            
        #elif tag == 'view':
         #   self.get_help('view_help.txt')
            
        elif tag == 'client':
            self.get_help('client_help.txt')
            
        elif tag == 'visit':
            self.get_help('visit_help.txt')
            
        elif tag == 'household':
            self.get_help('household_help.txt')
            
        elif tag == 'members':
            self.get_help('member_help.txt')
            
        elif tag == 'search':
            self.get_help('search_help.txt')
            
        else:
            print("Invalid option")
        
        
    def get_help(self, filename):
        """This function reads in a file and inserts the text into
        the textbox widget.
        
        """
        f = open(filename, 'r')
        helptext = f.read()
        f.close()
        self.instruct.insert('1.0', helptext)
        
        
                          
