"""cdbfunctions.py

Developer: Noelle Todd
Last Updated: June 9, 2014

This module consists of helper functions which will be called by another
module that will called directly by the user interface. This module is 
still in its early testing stages; many more functions will be added or
edited in the following weeks.

"""

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from cdbtabledef import Household, Person, Volunteer, Visit


#Functions for inserts
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


def get_age_breakdown(members):
	"""This function will retrieve all the ages of the members, and return the
	number of adults, seniors, children, and infants accordingly.
	
	"""	
	infants = 0
	children = 0
	adults = 0
	seniors = 0
	
	for member in members:
		if member.age < 2:
			infants = infants + 1
		elif member.age >= 2 and member.age < 18:
			children = children + 1
		elif member.age >= 18 and member.age < 65:
			adults = adults + 1
		else:
			seniors = seniors + 1
			
	agegroups = {'infants':infants, 'children':children, 'adults':adults,
				'seniors':seniors}	
	return agegroups
