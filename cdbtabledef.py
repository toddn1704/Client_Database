"""cdbtabledef.py

Developer: Noelle Todd
Last Updated: December 30, 2014

This module will create 4 tables for the client database, using the
sqlalchemy module, and the sqlite database. This module is still in
early testing stages, and as such, is subject to many changes, and 
probably contains bugs.
"""

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///client_db.sqlite')
session = sessionmaker()
session.configure(bind=engine)

base = declarative_base()


class Household(base):
	"""This class creates a table with columns for household data.
	"""
	__tablename__ = 'household'
	id = Column(Integer, primary_key=True)
	street_address = Column(String)
	apt = Column(String)
	city = Column(String, default = 'Troy')
	state = Column(String(2), default = 'NY')
	zip = Column(Integer, default = '12180')
	date_verified = Column(DateTime)
	seniors = Column(Integer, default = 0)
	adults = Column(Integer, default = 0)
	children = Column(Integer, default = 0)
	infants = Column(Integer, default = 0)
	total = Column(Integer, default = 0)

	
class Person(base):
	"""This class creates a table with columns for individual's data.
	"""
	__tablename__ = 'person'
	id = Column(Integer, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)
	DOB = Column(DateTime)
	age = Column(Integer)
	phone = Column(String)
	date_joined = Column(DateTime)
	HH_ID = Column(Integer, ForeignKey('household.id'))
	household = relationship(Household,
				backref=backref('members',
                                                uselist=True,
                                                passive_updates=False))
		
class Volunteer(base):
	"""This class creates a table with columns for volunteer data.
	"""
	__tablename__ = 'volunteer'
	id = Column(Integer, primary_key = True)
	first_name = Column(String)
	last_name = Column(String)
	phone = Column(String)
	active = Column(Boolean, default=True)
	color = Column(String)
	
	
class Visit(base):
	"""This class creates a table with columns tracking visit history.
	"""
	__tablename__ = 'visit'
	id = Column(Integer, primary_key = True)
	I_ID = Column(Integer, ForeignKey('person.id'))
	HH_ID = Column(Integer, ForeignKey('household.id'))
	Vol_ID = Column(Integer, ForeignKey('volunteer.id'))
	date = Column(DateTime, default = func.now())
	visit_notes = Column(String(256))
	

base.metadata.create_all(engine)


