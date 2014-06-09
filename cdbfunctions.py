"""cdbfunctions.py

Developer: Noelle Todd
Last Updated: June 9, 2014

This module consists of functions which will be called by the user
interface, in order to insert, delete, update, etc. data in the database.
This module is still in its early testing stages; many more functions will
be added or edited in the following weeks.

"""

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from cdbtabledef import Household, Person, Volunteer, Visit

engine = create_engine('sqlite:///test_db.sqlite')
session = sessionmaker()
session.configure(bind=engine)

base = declarative_base()

s = session()

def quit_session():
	"""This function will close the session.
	"""
	s.close()
	
def cancel_changes():
	"""This function will rollback transactions & close session.
	"""
	s.rollback()
	s.close()
	
def new_client(firstname, lastname, dob, datejoined, street,
				dateverified = None, phonenum = None, Apt = None,
				City = 'Troy', State = 'NY', Zip = '12180'):
	"""This function creates a new person, household, and first visit.
	If the page viewed is for a new_client, then this connects to the SAVE
	button in the interface.
	
	For input, the function takes lists of strings for firstname and lastname, 
	a list of date objects for dob, a list of integers for phonenum, strings
	for Apt, City, and State, and an integer for Zip. There is no return.
	
	"""
	
	#create new household
	newhouse = insert_household(street, dateverified, Apt, City, State, Zip)
	
	#create new person for every household member
	if type(firstname) == list:
		membersum = len(firstname) #finds length of list of names
		for i in range(0, membersum):
			insert_person(firstname[i], lastname[i], dob[i], datejoined,
						newhouse)
	else:
		insert_person(firstname, lastname, dob, datejoined, newhouse,
					phonenum)

	#Additions:
	#	Can we make the input any simpler?
	#	How do we deal with multiple phone numbers?
	#	Create a new visit.
	
	s.commit()
	
	
def insert_household(street, dateverified = None, Apt = None, City = 'Troy',
					State = 'NY', Zip = '12180'):
	"""This function creates a new row to hold a household's data. It returns
	the household id, which will be used when we insert household members.

	"""
	newhouse = Household(street_address = street, apt = Apt, city = City,
						  state = State, zip = Zip, 
						  date_verified = dateverified)
	s.add(newhouse)
	s.commit()
	return newhouse.id
			  
	
def insert_person(firstname, lastname, dob, datejoined, newhouse,
				phonenum = None):
	"""This function creates a new row to hold an individual's data. There is
	no return.
	
	"""
	newpers = Person(first_name = firstname, last_name = lastname,
					  DOB = dob, date_joined = datejoined, phone = phonenum)
	newpers.HH_ID = newhouse
	newpers.age = age(dob)
	s.add(newpers)
	s.commit()

	
def insert_volunteer(firstname, lastname, phonenum):
	"""	This function creates a new row in the Volunteer table, to hold
	a volunteer's data.
	
	"""
	new_vol = Volunteer(first_name = firstname, last_name = lastname, 
						phone = phonenum)
	s.add(new_vol)
	s.commit()
	
	
def age(dob):
	"""This function calculates a person's age using the dob input to it.
	"""
	timey = datetime.now()
	if timey.month > dob.month:
		return timey.year - dob.year
	elif timey.month < dob.month:
		return timey.year - dob.year - 1
	else:
		if timey.day >= dob.day:
			return timey.year - dob.year
		else:
			return timey.year - dob.year - 1
