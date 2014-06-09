"""cdbifunc.py

Developer: Noelle Todd
Last Updated: June 9, 2014

This module holds all functions that will be called directly by the user
interface. This module uses several functions in cdbfunctions.py; the two
modules have been split to make designing the user interface as simple as
simple as possible.

"""

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from cdbtabledef import Household, Person, Volunteer, Visit
from cdbfunctions import *
from sqlafuntest import *

engine = create_engine('sqlite:///test_db.sqlite')
session = sessionmaker()
session.configure(bind=engine)

base = declarative_base()

s = session()

#Functions to connect to buttons
def quit_session():
	"""This function will close the session.
	"""
	s.close()
	
	
def cancel_changes():
	"""This function will rollback transactions & close session.
	"""
	s.rollback()
	s.close()
	
	
def reset(I_ID):
	"""	This function sends the original data back.
	"""
	info = select_client(I_ID)
	return info

	
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
	
	
#Function to retrieve all data for a client
def select_client(I_ID):
	"""This function returns all client data for a selected client.
	"""
	
	#find person and associated household
	pers = s.query(Person).filter(Person.id == I_ID).one()	
	house = s.query(Household).filter(Household.id == pers.HH_ID).one()
	
	info = [pers.id, pers.first_name, pers.last_name, pers.DOB, pers.age,
			pers.phone, pers.date_joined, house.street_address, house.apt,
			house.city, house.state, house.zip, house.date_verified]
			
	for member in house.members:
		info.append( (member.first_name, member.last_name, member.DOB, member.age) )

	agegroups = get_age_breakdown(house.members)
	info.append(agegroups)
	return info
	

#Function for drop-down, selection menu
def list_people():
	"""This function returns a list of all people in the database, sorted in
	alphabetic order by last name. This will also return the id of the person,
	which should not be displayed, but will be used for selection purposes.
	"""
	people = []
	for instance in s.query(Person).order_by(Person.last_name):
		people.append((instance.first_name, instance.last_name, instance.id))
		#also return street_address
	return people
	
