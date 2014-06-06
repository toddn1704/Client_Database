"""cdbtabledef.py

Developer: Noelle Todd
Last Updated: June 5, 2014

This module will create 4 tables for the client database, using the
sqlalchemy module, and the sqlite database. This module is still in
early testing stages, and as such, is subject to many changes, and 
probably contains bugs.
"""

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test_db.sqlite')
session = sessionmaker()
session.configure(bind=engine)

base = declarative_base()

class Household(base):
	"""
	This class creates a table with columns for household data.
	"""
	__tablename__ = 'household'
	id = Column(Integer, primary_key = True)
	street_address = Column(String)
	apt = Column(String)
	city = Column(String, default = 'Troy')
	state = Column(String, default = 'NY')
	zip = Column(Integer, default = '12180')
	#contact_ID = Column(Integer, ForeignKey('person.id'))
	date_verified = Column(DateTime)
	
class Person(base):
	"""
	This class creates a table with columns for individual's data.
	"""
	__tablename__ = 'person'
	id = Column(Integer, primary_key = True)
	first_name = Column(String)
	last_name = Column(String)
	DOB = Column(DateTime)
	age = Column(Integer)
	phone = Column(Integer)
	date_joined = Column(DateTime)
	HH_ID = Column(Integer, ForeignKey('household.id'))
	household = relationship(Household, backref=backref('members',
														uselist = True))
		
class Volunteer(base):
	"""
	This class creates a table with columns for volunteer data.
	"""
	__tablename__ = 'volunteer'
	id = Column(Integer, primary_key = True)
	first_name = Column(String)
	last_name = Column(String)
	phone = Column(Integer)
	
class Visit(base):
	"""
	This class creates a table with columns tracking visit history.
	"""
	__tablename__ = 'visit'
	id = Column(Integer, primary_key = True)
	I_ID = Column(Integer, ForeignKey('person.id'))
	HH_ID = Column(Integer, ForeignKey('household.id'))
	Vol_ID = Column(Integer, ForeignKey('volunteer.id'))
	date = Column(DateTime, default = func.now())

base.metadata.create_all(engine)
