import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
						'Noodle_project.settings')
						
import django
django.setup()

#note: the use of datetime objects may require running 'pip install pytz'
import datetime

from django.contrib.auth.models import User
from noodle.models import Admin, Staff, Student, Course, Subject, Material, File, Assessment
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
		 
	files = [
		{'name': 'Independence Day', 
		 'visibility': True, 
		 'course': 'History2',
		 'datePosted': datetime.datetime(1776,06,04)},
		{'name': 'Leviathan',
		 'visibility': False,
		 'course': 'Philosophy2',
		 'datePosted': datetime.datetime(2017,02,24)}]
	
	assessments = [
		{'name': 'Operation Barbarossa', 
		 'visibility': True, 
		 'course': 'History2',
		 'deadline': datetime.datetime(1942,06,22),
		 'submissionDate': datetime.datetime(1945,05,8)}]
		 
	for admin in admins:
		add_admin(add_user(admin['username'], admin['email'], admin['password'], 
							admin['fname'], admin['sname']))
			
	#store this to populate later fields
	staffMs = []
	for staffM in staff:
		staffMs.append(add_staff(add_user(staffM['username'], staffM['email'], staffM['password'], 
											staffM['fname'], staffM['sname']),
								 staffM['subject'], staffM['status']))
			
	subjectMs = {}
	#staff reorganised for convenience
	staffBySubject = {}
	coursesBySubject = {}

	for subject in subjects:
		subjectMs[subject] = add_subject(subject)
		
		staffBySubject[subject] = []
		coursesBySubject[subject] = []
		
		for staffM in staffMs:
			if(staffM.subject == subject):
				staffBySubject[subject].append(staffM)
				
		for course in courses:
			if(course['subject'] == subject):
				coursesBySubject[subject].append(course)
				
	courseL = []
	for course in courses:
	
		managers = []
		#here we assume all staff members belonging to a course are managers
		for staffM in staffBySubject[course['subject']]:
			managers.append(staffM)
		courseL.append(add_course(course['name'], course['courseID'],
					subjectMs[course['subject']], managers))
					
	for student in students:
		add_student(add_user(student['username'], student['email'], student['password'], 
							 student['fname'], student['sname']),
					student['subject'], student['yearOfStudy'], courseL)
					
	for file in files:
		subject = ''
		for course in courses:
			if(course['name'] == file['course']):
				subject = course['subject']
				break
		for course in courseL:
			if(course.name == file['course']):
				pCourse = course
				break
		#here we just take the first staff member for any given subject
		staffCreator = staffBySubject[subject][0]
		add_file(add_material(file['name'], file['visibility'],
					pCourse, staffCreator), file['datePosted'])
	
	for assessment in assessments:
		subject = ''
		for course in courses:
			if(course['name'] == assessment['course']):
				subject = course['subject']
				break
		for course in courseL:
			if(course.name == assessment['course']):
				pCourse = course
				break
		staffCreator = staffBySubject[subject][0]
		add_assessment(add_material(assessment['name'], assessment['visibility'],
									pCourse, staffCreator), assessment['deadline'], 
									assessment['submissionDate'])
						
def add_user(username, email, password, fname, lname):
	
	#necessary to do this rather than get_or_create because create_user hashes passwords
	try:
		return User.objects.get(username = email)
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
	c = Course.objects.get_or_create(name = name, subject = subject)[0]
	c.courseID = courseID
	c.subject = subject
	for manager in managers:
		c.staffManagers.add(manager)
	c.save()
	return c

def add_material(name, visibility, course, staffCreator):
	return Material.objects.get_or_create(name = name, visibility = visibility, 
										courseFrom = course, createdBy = staffCreator)[0]
	
def add_file(material, datePosted):
	f = File.objects.get_or_create(material = material)[0]
	f.datePosted = datePosted
	f.save()
	return f

def add_assessment(material, deadline, submissionDate):
	return Assessment.objects.get_or_create(material = material, deadline = deadline, submissionDate = submissionDate)[0]
	
#Start execution here!
if __name__ == '__main__':
	print("Starting Noodle population script...")
	populate()