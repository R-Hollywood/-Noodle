import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
						'Noodle_project.settings')
						
import django
django.setup()

#note: the use of datetime objects may require running 'pip install pytz'
import datetime

from django.contrib.auth.models import User
from noodle.models import *
from django.template.defaultfilters import slugify

def populate():

	admins = [
		{'username':"president",
		 'email': "yaah@email.com",
		 'password': "Password0001",
		 'fname': "Howard",
		 'sname': "Dean"}]
		 
	staff = [
		{'username':"kingOfSpain",
		 'email': "habsburgSpain@email.com",
		 'password': "Phillip420",
		 'fname': "Charles II",
		 'sname': "Habsburg",
		 'subject': "History",
		 'status': "Dead"},
		{'username':"shogun",
		 'email': "honnouji@email.com",
		 'password': "Press9ForRegicide",
		 'fname': "Akechi",
		 'sname': "Mitsuhide",
		 'subject': "History",
		 'status': "Dead"},
		{'username':"sultan",
		 'email': "constantinople@email.com",
		 'password': "WhyIsTheRumGone9001",
		 'fname': "Mehmed II",
		 'sname': "Osman",
		 'subject': "History",
		 'status': "Dead"},
		{'username':"contractor",
		 'email': "socialContract@email.com",
		 'password': "BrutishAndShort42",
		 'fname': "Thomas",
		 'sname': "Hobbes",
		 'subject': "Philosophy",
		 'status': "Dead"},
		{'username':"utility",
		 'email': "utilitarianism@email.com",
		 'password': "How2IncreaseUtility",
		 'fname': "John",
		 'sname': "Stuart Mill",
		 'subject': "Philosophy",
		 'status': "Dead"},
		{'username':"analysist",
		 'email': "realAnalysis@email.com",
		 'password': "letEpsilonBe0",
		 'fname': "Karl",
		 'sname': "Weierstrass",
		 'subject': "Mathematics",
		 'status': "Dead"}]
		 
	students = [
		{'username':"developer",
		 'email': "FuncReqs@email.com",
		 'password': "bracketScience4Lyfe",
		 'fname': "Ross",
		 'sname': "McBride",
		 'subject': "History",
		 'yearOfStudy': 2},
		{'username':"viewer",
		 'email': "ERDiagrams@email.com",
		 'password': "climbMountain2SeeView",
		 'fname': "Ivo",
		 'sname': "Domingos",
		 'subject': "Philosophy",
		 'yearOfStudy': 2},
		{'username':"designer",
		 'email': "Wireframes@email.com",
		 'password': "2stylishANDcascading",
		 'fname': "Rachel-Anne",
		 'sname': "Hollywood",
		 'subject': "Philosophy",
		 'yearOfStudy': 2},
		{'username':"authenticator",
		 'email': "SiteMap@email.com",
		 'password': "100percentVerified",
		 'fname': "Jack",
		 'sname': "Conacher",
		 'subject': "Mathematics",
		 'yearOfStudy': 2}]
		 
	
	subjects = ["History", "Mathematics", "Philosophy"]
	
	courses = [
		{'name': 'History2',
		 'courseID': '2H',
		 'subject': 'History'},
		{'name': 'Philosophy2',
		 'courseID': '2P',
		 'subject': 'Philosophy'},
		{'name': 'Mathematics2',
		 'courseID': '2M',
		 'subject': 'Mathematics'}]
		 
	visited_courses = [
	{'date': datetime.datetime(1610,7,4),
	 'student': 'developer',
	 'course': 'History2'}]
	 
	staff_visited_courses = [
	{'date': datetime.datetime(1955,7,8),
	'staffM': 'shogun',
	'course': 'History2'}]
		 
	files = [
		{'name': 'Independence Day', 
		 'visibility': True, 
		 'course': 'History2',
		 'datePosted': datetime.datetime(1776,6,4),
		 'file': '<placeholder>'},
		{'name': 'Leviathan',
		 'visibility': False,
		 'course': 'Philosophy2',
		 'datePosted': datetime.datetime(2017,2,24),
		 'file': '<placeholder>'}]
	
	assessments = [
		{'name': 'Operation Barbarossa', 
		 'visibility': True, 
		 'course': 'History2',
		 'deadline': datetime.datetime(1942,6,22),
		 'datePosted': datetime.datetime(1939,2,01)},
		{'name': 'The Future of Philosophy',
		 'visibility': True,
		 'course':'Philosophy2',
		 'deadline': datetime.datetime(2050,1,1),
		 'datePosted': datetime.datetime(2017,3,24)},
		{'name': 'Imaginary Numbers',
		 'visibility': False,
		 'course':'Mathematics2',
		 'deadline': datetime.datetime(1819,1,27),
		 'datePosted': datetime.datetime(1526,1,20)}]
		 
	studentSubmissions = [
		{'file': '<placeholder>',
		 'submissionDate': datetime.datetime(1945,5,8),
		 'student': 'developer',
		 'course': 'History2'}]
		 
	announcements = [
		{'name': "History2 Created!",
		 'body': "Nice-Memel!",
		 'date': datetime.datetime(1914, 6, 28),
		 'course': 'History2'},
		 {'name': "Philosophy2 Created!",
		 'body': "This sentence is false.",
		 'date': datetime.datetime(1648, 10, 24),
		 'course': 'Philosophy2'},
		 {'name': "Mathematics2 Created!",
		 'body': "Many counting!",
		 'date': datetime.datetime(1918, 11, 11),
		 'course': 'Mathematics2'}]
		 
	for admin in admins:
		add_admin(add_user(admin['username'], admin['email'], admin['password'], 
							admin['fname'], admin['sname']))
			
	for staffM in staff:
		add_staff(add_user(staffM['username'], staffM['email'], staffM['password'], 
							staffM['fname'], staffM['sname']),
					staffM['subject'], staffM['status'])

	for subject in subjects:
		add_subject(subject)
				
	for course in courses:
	
		subject = Subject.objects.filter(name=course['subject'])[0]
		#here we assume all staff members belonging to a course are managers
		managers = Staff.objects.filter(subject=course['subject'])
		managerList = []
		for manager in managers:
			managerList.append(manager.user)
		add_course(course['name'], course['courseID'],
					subject, managerList)
					
	for student in students:
		add_student(add_user(student['username'], student['email'], student['password'], 
							 student['fname'], student['sname']),
					student['subject'], student['yearOfStudy'], 
					Course.objects.filter(subject=Subject.objects.filter(name=student['subject'])))
	developer = Student.objects.filter(user=User.objects.filter(username='developer'))[0]
	developer.enrolledIn.add(Course.objects.filter(name='Philosophy2')[0])
	developer.enrolledIn.add(Course.objects.filter(name='Mathematics2')[0])
					
	for visited_course in visited_courses:
		student = Student.objects.filter(user=User.objects.filter(username=visited_course['student']))[0]
		course = Course.objects.filter(name=visited_course['course'])[0]
		add_visitedcourse(visited_course['date'], student, course)
		
	for visited_course in staff_visited_courses:
		staffM = Staff.objects.filter(user=User.objects.filter(username=visited_course['staffM']))[0]
		course = Course.objects.filter(name=visited_course['course'])[0]
		add_staffvisitedcourse(visited_course['date'], staffM, course)
					
	for file in files:
		course = Course.objects.filter(name=file['course'])[0]
		subject = course.subject
		#here we just take the first staff member for any given subject
		staffCreator = (Staff.objects.filter(subject=subject)[0]).user
		add_file(add_material(file['name'], file['visibility'],
					course, staffCreator, file['datePosted']), file['file'])
	
	for assessment in assessments:
		course = Course.objects.filter(name=assessment['course'])[0]
		subject = course.subject
		staffCreator = (Staff.objects.filter(subject=subject)[0]).user
		add_assessment(add_material(assessment['name'], assessment['visibility'],
									course, staffCreator, assessment['datePosted']), 
									assessment['deadline'])
									
	for announcement in announcements:
		course = Course.objects.filter(name=announcement['course'])[0]
		add_announcement(course, announcement['name'], announcement['body'], announcement['date'])
						
def add_user(username, email, password, fname, lname):
	
	#necessary to do this rather than get_or_create because create_user hashes passwords
	try:
		return User.objects.get(username = username)
	except User.DoesNotExist:
		return User.objects.create_user(username = username,
					email = email, password = password,
					first_name = fname, last_name = lname)

def add_admin(user):
	return Admin.objects.get_or_create(user = user)[0]

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
		s.enrolledIn.add(course)
	s.save()
	return s

def add_subject(name):
	return Subject.objects.get_or_create(name = name)[0]

def add_course(name, courseID, subject, managers):
	c = Course.objects.update_or_create(name = name, 
										defaults = {'subject': subject})[0]
	c.courseID = courseID
	c.subject = subject
	for manager in managers:
		c.staffManagers.add(manager)
	c.save()
	return c
	
def add_visitedcourse(date, student, course):
	return VisitedCourse.objects.update_or_create(
		student=student, course=course, defaults={'date': date})[0]
		
def add_staffvisitedcourse(date, staffM, course):
	return StaffVisitedCourse.objects.update_or_create(
		staff=staffM, course=course, defaults={'date': date})[0]

def add_material(name, visibility, course, staffCreator, datePosted):
	return Material.objects.update_or_create(name = name, defaults={'visibility' : visibility, 
										'courseFrom' : course, 'createdBy' : staffCreator, 
										'datePosted':datePosted})[0]
	
def add_file(material, file):
	f = File.objects.get_or_create(material = material)[0]
	#f.file = file
	f.save()
	return f

def add_assessment(material, deadline):
	return Assessment.objects.update_or_create(material = material, 
					defaults={'deadline' : deadline})[0]
	
def	add_announcement(course, name, body, date):
	return Announcement.objects.update_or_create(
		course = course, defaults={'name':name, 
									'body':body, 'date':date})[0]
	
#Start execution here!
if __name__ == '__main__':
	print("Starting Noodle population script...")
	populate()