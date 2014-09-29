"""cdbifunc.py

Developer: Noelle Todd
Last Updated: September 12, 2014

This module holds all functions that will be called directly by the user
interface. This module uses several functions in cdbfunctions.py; the two
modules have been split to make designing the user interface as simple as
simple as possible.

"""
import sqlalchemy
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy import desc
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from cdbtabledef import Household, Person, Volunteer, Visit
from cdbfunctions import *

engine = create_engine('sqlite:///test2_db.sqlite')
session = sessionmaker()
session.configure(bind=engine)

base = declarative_base()

s = session()

####Closing, cancelling, and resetting functions####

def quit_session():
	"""This function will close the session.
	"""
	s.close()
	
	
def cancel_changes():
	"""This function will rollback transactions.
	"""
	s.rollback()

	
def reset(I_ID):
	"""	This function sends the original data back.
	"""
	info = select_client(I_ID)
	return info


####Functions for listing####

def list_people():
	"""This function takes no arguments and returns a list of tuples.
	Each tuple contains a string for a person's full name, a string for
	the person's street_address, and an integer for the person's unique id.
	
	Note: this only returns people that are members of a household.
	"""
	people = []
	
	#create a list of tuples, where each tuple contains a string holding a 
	#person's full-name, a string holding the person's street, and an integer
	#holding the person's unique id. The names are added in alphabetic (A-Z)
	#order.
	#
	
	for instance in s.query(Person).order_by(Person.last_name):
		try:
			h = s.query(Household).filter(Household.id == instance.HH_ID).one()
			fullname = instance.first_name + " " + instance.last_name
			people.append((fullname, instance.DOB, instance.id))
		except NoResultFound:
			pass

	return people
	

def list_historical_members():
	"""This function lists all people who are no longer associated with a
	household.
	"""
	people = []
	for instance in s.query(Person).order_by(Person.last_name):
		if instance.HH_ID == None:
			fullname = instance.first_name + " " + instance.last_name
			people.append(fullname)
		else: pass
	return people
	
		
def list_active_volunteers():
	"""This function takes no arguments and returns a list of tuples.
	Each tuple contains a string for a volunteer's full name, and a string
	for their phone number.
	
	"""
	volunteers = []
	for instance in s.query(Volunteer).order_by(Volunteer.last_name):
		if instance.active == True:
			fullname = instance.first_name + " " + instance.last_name
			volunteers.append((fullname, instance.id))
		else: pass
	return volunteers
	
	
def list_all_volunteers():
	"""This function takes no arguments and returns a list of tuples.
	This lists all volunteers, whether active or not, and their activity
	status.
	
	"""
	volunteers = []
	for instance in s.query(Volunteer).order_by(Volunteer.last_name):
		fullname = instance.first_name + " " + instance.last_name
		volunteers.append((fullname, instance.id))
	return volunteers
	
	
def list_households():
	"""This function simply lists all households.
	"""
	houses = []
	for instance in s.query(Household).order_by(Household.city):
		houses.append((instance.street_address, instance.city, instance.id))
	return houses

def list_vis():
	"""This function simply lists all visits.
	"""
	visits = []
	for instance in s.query(Visit).order_by(Visit.date):
		visits.append((instance.HH_ID, instance.id, instance.I_ID))
	return visits


def select_volunteer(Vol_ID):
        """This returns all volunteer information.
        """
        vol = s.query(Volunteer).filter(Volunteer.id == Vol_ID).one()
        volreturn = volunteerData(firstname=vol.first_name, lastname=vol.last_name,
                                  phone=vol.phone, active=vol.active,
                                  color=vol.color)
        return volreturn

        
def select_client(I_ID):
	"""This a dictionary of objects containing all data for a selected
	client.
	
	The return will include an oldClientData object for the visitor, 
	a houseData object for the household, a list of visitDataReturn objects,
	a list of oldClientData objects for family members, and a dictionary of
	agegroups.
	
	"""
	#find person and associated household
	pers = s.query(Person).filter(Person.id == I_ID).one()	
	house = s.query(Household).filter(Household.id == pers.HH_ID).one()
	
	#create new object to hold visitor's data
	visitor = oldClientData(id=pers.id, firstname=pers.first_name,
							lastname=pers.last_name, dob=pers.DOB,
							phone=pers.phone, dateJoined=pers.date_joined)
	
	#create new object to hold household data
	household = houseData(street=house.street_address, city=house.city,
							state=house.state, zip=house.zip, 
							dateVerified=house.date_verified, apt=house.apt)
							
	#list to hold member-data objects
	members = []
	
	#create new objects to hold data for each additional household member
	for member in house.members:
		if member.first_name == pers.first_name: pass
		else:
			mem = oldClientData(id=member.id, firstname=member.first_name,
								lastname=member.last_name, dob=member.DOB,
								phone=member.phone,
								dateJoined=member.date_joined)
			members.append(mem)
			
	#get list of information about past 3 visits
	visits = list_visits(s, I_ID)
	
	#call to function to get dictionary of ages
	agegroups = get_age_breakdown(house.members)
	house.seniors = agegroups["seniors"]
	house.adults = agegroups["adults"]
	house.children = agegroups["children"]
	house.infants = agegroups["infants"]
	house.total = agegroups["total"]
	
	#create dictionary of all objects to be returned
	info = {"visitor":visitor, "household":household, "member_list":members,
			"visit_list":visits, "agegroup_dict":agegroups}
	return info
	

####Functions for creating new records####

def new_volunteer(firstname, lastname, phone=None, active=True):
	"""This function creates a new record for an active volunteer.
	"""
	insert_volunteer(s, firstname, lastname, phonenum=phone, active=active)
	

def new_visit(I_ID, visitInfo):
	"""This function records a visit for a household.
	"""
	pers = s.query(Person).filter(Person.id == I_ID).one()
	house = s.query(Household).filter(Household.id == pers.HH_ID).one()
	
	#create a new visit
	insert_visit(s, visitInfo.Vol_ID, pers.id, house.id, visitInfo.visitDate,
				visitInfo.notes)

	
def new_household(houseInfo, visitInfo, newClientInfo_list):
	"""This function takes an object for house info, an object for
	visit info, and a list of objects for client info (one object per
	client).
	
	This function creates a new record for each new person, a new record
	for the household, and new record for the a visit.
	
	"""
	#create new household
	newhouse = insert_household(s, houseInfo.street, houseInfo.dateVerified,
								houseInfo.apt, houseInfo.city,
								houseInfo.state, houseInfo.zip)
	
	#create new person for every household member
	data = newClientInfo_list #variable renamed for simplicity	
	
	
	for i in range(0, len(data)):			
		fname = data[i].firstname
		lname = data[i].lastname
		dob = data[i].dob
		phone = data[i].phone
		dateJoined = data[i].dateJoined
		
		pers = insert_person(s, data[i].firstname, data[i].lastname,
							data[i].dob, newhouse.id, data[i].dateJoined,
							data[i].phone)
		
		#the first person is the actual visitor; save for insert_visit
		if i == 0:
			newpers = pers
		
	age_dict = get_age_breakdown(newhouse.members)
	newhouse.seniors = age_dict["seniors"]
	newhouse.adults = age_dict["adults"]
	newhouse.children = age_dict["children"]
	newhouse.infants = age_dict["infants"]
	newhouse.total = age_dict["total"]
	
	#create new visit for household
	insert_visit(s, visitInfo.Vol_ID, newpers.id, newhouse.id, 
				visitInfo.visitDate, visitInfo.notes)	
	return newpers.id
   
				
####Functions for updating records####

def update_all(I_ID, houseInfo, oldClientInfo_list, 
				newClientInfo_list=None):
				
	pers = s.query(Person).filter(Person.id == I_ID).one()
	house = s.query(Household).filter(Household.id == pers.HH_ID).one()
	
	#update household
	update_household(s, house.id, houseInfo.street, houseInfo.city, 
					houseInfo.state, houseInfo.zip, houseInfo.apt,
					houseInfo.dateVerified)
	
	#add new clients (if they exist)
	data = newClientInfo_list #renamed for simplicity
	if data == None: pass
	else:
		for i in range(0, len(data)):
			newpers = insert_person(s, data[i].firstname, data[i].lastname,
									data[i].dob, house.id, 
									phonenum=data[i].phone)
	
	#update old clients
	old = oldClientInfo_list #renamed for simplicity
	for i in range(0, len(old)):
		update_person(s, old[i].id, old[i].firstname, old[i].lastname, 
					old[i].dob, old[i].phone)
    
	
def update_vol(vol_id, firstname, lastname, phonenum, active_state, color):
	"""This function will update a volunteer's records.
	"""
	update_volunteer(s, vol_id, firstname, lastname, phonenum,
                         active_state, color)
	

def update_vis(vis_id, date, notes=None):
        """This function will update a visit.
        """
        update_visit(s, vis_id, date, notes)
        
	
def reactivate_volunteer(Vol_ID):
	"""This function reactivates a volunteer. The volunteer will now
	reappear in lists and such.
	
	"""
	vol = s.query(Volunteer).filter(Volunteer.id == Vol_ID).one()
	vol.active = True
	s.commit()
	
	
####Functions for deleting/deactivating records####

def remove_client(I_ID):
	"""This function will only delete a single client if the client
	has never participated in a visit. If the client has visited, then
	their household is set to "None" and they are placed in a "historical
	members" list, but they remain in the database.
	
	"""
	pers = s.query(Person).filter(Person.id == I_ID).one()
	vis = s.query(Visit).filter(Visit.I_ID == pers.id).all()
	
	#create new household with dummy address
	house = insert_household(s, street="None", dateverified=None, Apt=None, 
					City='None', State='None', Zip='00000')
	pers.HH_ID = house.id
	#pers.HH_ID = None
	s.commit()
	
	
def remove_volunteer(Vol_ID):
	"""This function will delete a volunteer if the volunteer has
	not participated in a visit. Else, it will "deactivate" the 
	volunteer. The volunteer will remain in the database and can be 
	reactivated, but will not appear in the "active_volunteers" list.
	
	"""
	vol = s.query(Volunteer).filter(Volunteer.id == Vol_ID).one()
	vis = s.query(Visit).filter(Visit.Vol_ID == Vol_ID).all()
	
	#if volunteer is not associated with a visit, then delete
	if len(vis) == 0:
		delete_volunteer(s, Vol_ID)
		
	#if volunteer has helped with visits, just deactivate them
	else:
		vol.active = False
		s.commit()
	
	
def remove_household(I_ID):
	"""This function deletes the entire household, all members of the
	household, and all visits associated with the household.
	
	"""
	#get household id
	pers = s.query(Person).filter(Person.id == I_ID).one()
	house = s.query(Household).filter(Household.id == pers.HH_ID).one()
	
	#remove all visits the household has made
	visits = s.query(Visit).filter(Visit.HH_ID == house.id).all()
	for visit in visits:
		delete_visit(s, visit.id)
		
	#remove all members from the household
	for member in house.members:
		delete_person(s, member.id)
		
	#remove all visits the household has made
	delete_household(s, house.id)

	
def remove_visit(vis_id):
        """This function deletes a single visit.
        """
        delete_visit(s, vis_id)

        
####Functions for generating monthly/yearly reports####

def generate_monthly_report():
	"""This function will generate a csv/excel file that holds
	data about households for the past month.
	"""
	duration = timedelta(days=31)
	generate_report(s, duration)

	
def generate_yearly_report():
	"""This function will generate a csv/excel file that holds
	data about households for the past year.
	"""
	duration = timedelta(days=365)
	generate_report(s, duration)
	
	
def generate_weekly_report():
        """This function will generate a csv/excel file that holds
        date about the households for the past 7 days. This will
        include the number of new visitors, and the number of old
        visitors.
        """
        duration = timedelta(days=7)
        generate_report(s, duration)
	
	
	
