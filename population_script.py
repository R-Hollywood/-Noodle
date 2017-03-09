import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
						'Noodle_project.settings')
						
import django
django.setup()

import datetime

from django.contrib.auth.models import User
from noodle.models import Admin, Staff, Student, Course, Subject, Material, File, Assessment

def populate():

	admins = [
		{'email': "yaaaaaaah@email.com",
		 'password': "Password0001",
		 'fname': "howard",
		 'sname': "dean"}]
		 
	staff = [
		{'email': "habsburgSpain@email.com",
		 'password': "Phillip420",
		 'fname': "Charles II",
		 'sname': "Habsburg",
		 'subject': "History",
		 'status': "Dead"},
		{'email': "honnouji@email.com",
		 'password': "Press9ForRegicide",
		 'fname': "Akechi",
		 'sname': "Mitsuhide",
		 'subject': "History",
		 'status': "Dead"},
		{'email': "constantinople@email.com",
		 'password': "WhyIsTheRumGone9001",
		 'fname': "Mehmet II",
		 'sname': "Fatih",
		 'subject': "History",
		 'status': "Dead"},
		{'email': "socialContract@email.com",
		 'password': "BrutishAndShort42",
		 'fname': "Thomas",
		 'sname': "Hobbes",
		 'subject': "Philosophy",
		 'status': "Dead"},
		{'email': "utilitarianism@email.com",
		 'password': "How2IncreaseUtility",
		 'fname': "John",
		 'sname': "Stuart Mill",
		 'subject': "Philosophy",
		 'status': "Dead"},
		{'email': "realAnalysis@email.com",
		 'password': "letEpsilonBe0",
		 'fname': "Karl",
		 'sname': "Weierstrass",
		 'subject': "Mathematics",
		 'status': "Dead"}]
		 
	students = [
		{'email': "FuncReqs@email.com",
		 'password': "bracketScience4Lyfe",
		 'fname': "Ross",
		 'sname': "McBride",
		 'subject': "History",
		 'yearOfStudy': 2},
		{'email': "ERDiagrams@email.com",
		 'password': "climbMountain2SeeView",
		 'fname': "Ivo",
		 'sname': "Domingos",
		 'subject': "Philosophy",
		 'yearOfStudy': 2},
		{'email': "Wireframes@email.com",
		 'password': "2stylishANDcascading",
		 'fname': "Rachel-Anne",
		 'sname': "Hollywood",
		 'subject': "Philosophy",
		 'yearOfStudy': 2},
		{'email': "SiteMap@email.com",
		 'password': "100percentVerified",
		 'fname': "Jack",
		 'sname': "Conacher",
		 'subject': "Mathematics",
		 'yearOfStudy': 2}]
		 
	
	subjects = ["History", "Mathematics", "Philosophy"]
	
	courses = [
		{'name': 'History2',
		 'courseID': '2H',
		 'subject': 'History',
		 'managers': []},
		{'name': 'Philosophy2',
		 'courseID': '2P',
		 'subject': 'Philosophy',
		 'managers': []},
		{'name': 'Mathematics2',
		 'courseID': '2M',
		 'subject': 'Mathematics',
		 'managers': []}]
		 
	files = [
		{'name': 'CityOfWorldsDesire', 
		 'visibility': True, 
		 'course': 'History2'},
		{'name': 'Leviathan',
		 'visibility': False,
		 'course': 'Philosophy'}]
	
	assessment = [
		{'name': 'CityOfWorldsDesire', 
		 'visibility': True, 
		 'course': 'History2',
		 'deadline': datetime.datetime(1776,06,04),
		 'submissionDate': datetime.datetime(2017,02,24)}]
		 
	for admin in admins:
		add_admin(User.objects.get_or_create(username = admin['email'],
					email = admin['email'], password = admin['password'],
					first_name = admin['fname'], last_name = admin['sname'])[0])
					
	staffMs = []
	for staffM in staff:
		staffMs.append(add_staff(User.objects.create_user(username = staffM['email'],
						email = staffM['email'], password = staffM['password'],
						first_name = staffM['fname'], last_name = staffM['sname']),
					staffM['subject'], staffM['status']))
				  
	for student in students:
		add_student(User.objects.create_user(username = student['email'],
						email = student['email'], password = student['password'],
						first_name = student['fname'], last_name = student['sname']),
					student['subject'], student['yearOfStudy'])
					
	staffBySubject = {}
	for subject in subjects:
		add_subject(subject)
		staffBySubject[subject] = []
		for staffM in staffMs:
			if(staffM.subject == subject):
				staffBySubject[subject].append(staffM)
				
	for course in courses:
		managers = []
		#here we assume all staff members belonging to a course are managers
		for staffM in staffMs[course['subject']]:
			managers.append(staffM)
		
		add_course(course['name'], course['courseID'],
					course['subject'], managers)
					
	for file in files:
		subject = ''
		for course in courses:
			if(course['name'] == file['course']):
				subject = course['subject']
		staffCreator = staffBySubject[subject][0]
		add_file(add_material(file['name'], file['visibility'],
					file['course'], staffCreator))
	
	for assessment in assessments:
		subject = ''
		for course in courses:
			if(course['name'] == assessment['course']):
				subject = course['subject']
		staffCreator = staffBySubject[subject][0]
		add_assessment(add_material(assessment['name'], assessment['visibility'],
						assessment['course'], staffCreator),
						assessment['deadline'], assessment['submission'])
	
def add_admin(user):
	a = Admin.objects.get_or_create(user = user)[0]
	a.save()
	return a

def add_staff(user, subject, status):
	s = Staff.objects.get_or_create(user = user)[0]
	s.subject = subject
	s.status = status
	s.save()
	return s

def add_student(user, subject, yearOfStudy, courses):
	s = Student.objects.get_or_create(user = user)[0]
	s.subject = subject
	s.yearOfStudy = yearOfStudy
	for course in courses:
		s.enrolledIn.append(course)
	s.save()
	return s

def add_subject(name):
	s = Subject.objects.get_or_create(name = name)[0]
	s.save()
	return s

def add_course(name, courseID, subject, managers):
	c = Course.objects.get_or_create(name = name)[0]
	c.courseID = courseID
	c.subject = subject
	for manager in managers:
		m.staffManagers.append(manager)
	c.save()
	return c

def add_material(name, visibility, course, staffCreator):
	m = Material.objects.get_or_create(name = name)[0]
	m.visibility = visibility
	m.courseFrom = course
	m.createdBy = staffCreator
	m.save()
	return m
	
def add_file(material):
	f = File.objects.get_or_create(material = material)[0]
	f.save()
	return f

def add_assessment(material, deadline, submissionDate):
	a = Assessment.objects.get_or_create(material = material)[0]
	a.deadline = deadline
	a.submissionDate = submissionDate
	a.save()
	return a
	
#Start execution here!
if __name__ == '__main__':
	print("Starting Noodle population script...")
	populate()