from django import shortcuts
from noodle.models import *
from noodle.forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from datetime import timedelta
from noodle.webhose_search import run_query


def render(request, page, context_dict):
	
	context_dict['tier'] = 0
	user = request.user
	
	if(user.is_authenticated()):
		
		homePage = (page == 'noodle/homepage_extends_base.html')
			
		#we can separate staff from admin
		#but in practise, identification with 'is_superuser' is likely more practical
		if(hasattr(user, 'admin') and user.admin != None):
			context_dict['tier'] = 2
			
		if(hasattr(user, 'staff') and user.staff != None):
			context_dict['tier'] = 1
				
	return shortcuts.render(request, page, context_dict)

def home(request):

	user = request.user
	
	if(user.is_authenticated()):
		if(hasattr(user, 'admin') and user.admin != None):
			return HttpResponseRedirect(reverse('noodle:teachhome'))
	
		if(hasattr(user, 'staff') and user.staff != None):
			return HttpResponseRedirect(reverse('noodle:teachhome'))
		
		return HttpResponseRedirect(reverse('noodle:studenthome'))
	
	return render(request, 'noodle/homepage_extends_base.html', {})

@login_required
def teachhome(request):
	context_dict = {}
	context_dict['myCourses'] = pager(request, Course.objects.filter(staffManagers__in=[request.user]), 10)
	context_dict['subjects'] = pager(request, Subject.objects.all(), 10)
	context_dict['courses'] = pager(request, Course.objects.all(), 10)
	context_dict['recentFiles'] = (File.objects.all())[:5]

	form = SubjectForm()
	if request.method == 'POST':
		form = SubjectForm(request.POST)
		if form.is_valid():
			form.save()
			request.method = 'GET'
			return teachhome(request)
		else:
			print(form.errors)
	context_dict['subject_form'] = form
	
	return render(request,'noodle/teachhome.html', context_dict)
	
@login_required
def studenthome(request):
	context_dict = {}
	context_dict['myCourses'] = pager(request, Course.objects.filter(enrolledStudents__in=[request.user.student]), 10)
	context_dict['subjects'] = pager(request, Subject.objects.all(), 10)
	context_dict['courses'] = pager(request, Course.objects.all(), 10)
	recentCourses = VisitedCourse.objects.all()[:5]
	context_dict['recentCourses'] = []
	for recentCourse in recentCourses:
		(context_dict['recentCourses']).append(recentCourse.course)
	
	return render(request,'noodle/studenthome.html', context_dict)
	
@login_required	
def show_subject(request, subject_name_slug):
	context_dict = {}
	try:
		subject = Subject.objects.get(slug=subject_name_slug)
		courses = Course.objects.filter(subject=subject)
		context_dict['courses'] = pager(request, courses, 10)
		context_dict['subject'] = subject
		
		form = CourseForm()
		if request.method == 'POST':
			form = CourseForm(request.POST)
			if form.is_valid():
				if subject:
					course = form.save(commit=False)
					course.subject = subject
					course.staffManagers.add(request.user)
					course.save()
					request.method = 'GET'
					return show_subject(request, subject_name_slug)
			else:
				print(form.errors)
		context_dict['course_form'] = form
				
	except Subject.DoesNotExist:
		context_dict['subject'] = None
		context_dict['course'] = None
		
	return render(request, 'noodle/subject.html', context_dict)
	
@login_required	
def show_course(request, subject_name_slug, course_name_slug):
	context_dict = {}
	try:
		print 'memel'
		course = Course.objects.get(slug=course_name_slug)
		print course
		subject = course.subject
		material = Material.objects.filter(courseFrom=course)
		context_dict['subject'] = subject
		context_dict['course'] = course
		print course
		context_dict['material'] = material
		context_dict['files'] = pager(request, Material.objects.filter(courseFrom=course, assessment=None), 10)
		context_dict['assignments'] = pager(request, Material.objects.filter(courseFrom=course, file=None), 10)
		
		#update student's visited courses
		user = request.user
		if(user.is_authenticated() and hasattr(user, 'student') and user.student != None):
			VisitedCourse.objects.update_or_create(
							student = user.student, course = course, 
							defaults={'date': datetime.now()})[0]
							
		form = MaterialForm(courseName=course.name)
		fileForm = FileForm()
		assignmentForm = AssignmentForm()
	
		if request.method == 'POST':
			form = MaterialForm(data=request.POST, courseName=course.name)
			fileForm = FileForm(request.POST, request.FILES)
			assignmentForm = AssignmentForm(data=request.POST)
		
			if form.is_valid() and fileForm.is_valid():
				ass = form.save(commit=False)
				ass.datePosted = datetime.now()
				ass.courseFrom = course
				ass.createdBy = request.user
				ass.save()
				file = fileForm.save(commit=False)
				file.material = ass
				file.save()
				print(ass, ass.slug)
				request.method = 'GET'
				return show_course(request, subject_name_slug, course_name_slug)
			
			elif form.is_valid() and assignmentForm.is_valid():
				ass = form.save(commit=False)
				ass.datePosted = datetime.now()
				ass.courseFrom = course
				ass.createdBy = request.user
				ass.save()
				assignment = assignmentForm.save(commit=False)
				assignment.material = ass
				assignment.save()
				print(ass, ass.slug)
				request.method = 'GET'
				return show_course(request, subject_name_slug, course_name_slug)
			else:
				print(form.errors)
		
		context_dict['form'] = form
		context_dict['file_form'] = fileForm
		context_dict['assignment_form'] = assignmentForm
							
	except Course.DoesNotExist:
		context_dict['subject'] = None
		context_dict['course'] = None
		context_dict['material'] = None
	return render(request, 'noodle/course.html', context_dict)
	
@login_required	
def show_announcements(request, subject_name_slug, course_name_slug):
	context_dict = {}
	try:
		course = Course.objects.get(slug=course_name_slug)
		announcements = Announcement.objects.filter(course=course)
		context_dict['course'] = course
		context_dict['announcements'] = pager(request, announcements, 10)
		
		form = AnnouncementForm(courseName=course.name)
		if request.method == 'POST':
			form = AnnouncementForm(request.POST, courseName=course.name)
			if form.is_valid():
				if(course):
					announcement = form.save(commit=False)
					announcement.date = datetime.now()
					announcement.course = course
					announcement.save()
					request.method = 'GET'
					return show_announcements(request, subject_name_slug, course_name_slug)
			else:
				print(form.errors)
		context_dict['announcement_form'] = form
		
		
	except Course.DoesNotExist:
		context_dict['announcements'] = None
		context_dict['course'] = None
	print context_dict
	return render(request, 'noodle/announcements.html', context_dict)
	
@login_required
def show_announcement(request, subject_name_slug, course_name_slug, announcement_name_slug):
	context_dict = {}
	try:
		course = Course.objects.filter(slug=course_name_slug)[0]
		announcement = Announcement.objects.get(slug=announcement_name_slug)
		context_dict['course'] = course
		context_dict['announcement'] = announcement
	except Course.DoesNotExist:
		context_dict['announcement'] = None
		context_dict['course'] = None
	return render(request, 'noodle/announcement.html', context_dict)
	
@login_required	
def show_assessment(request, subject_name_slug, course_name_slug, assessment_name_slug):
	context_dict = {}
	try:
		course = Course.objects.get(slug=course_name_slug)
		assessment = Assessment.objects.get(slug=assessment_name_slug)
		context_dict['course'] = course
		context_dict['assessment'] = assessment
		student = Student.objects.get(user=request.user)
		
		form = StudentSubmissionForm()
		if request.method == 'POST':
			form = StudentSubmissionForm(request.POST, request.FILES)
			if form.is_valid():
				sub = form.save(commit=False)
				sub.submissionDate = datetime.now()
				sub.assignment = assessment
				sub.student = student
				sub = form.save(commit=True)
				print(sub)
				request.method = 'GET'
				return show_assessment(request, subject_name_slug, course_name_slug, assessment_name_slug)
		context_dict['form'] = form
		
		context_dict['submission_string'] = ''
		submission = StudentSubmission.objects.filter(assignment=assessment, student=student)
		
		if(submission.exists()):
			print submission
			submission = submission[0]
		
			start_time = submission.submissionDate
			end_time = submission.assignment.deadline

			time_delta = ''
			if(end_time >= start_time):
				time_delta = end_time - start_time
				context_dict['submission_string'] = str(timedelta(seconds = 3))
				context_dict['submission_string'] = "You are before the deadline by" + str(timedelta(time_delta))
			else:
				time_delta = start_time - end_time
				context_dict['submission_string'] = "You are late for the deadline by" + str(timedelta(time_delta))
		
	except Course.DoesNotExist:
		context_dict['assessment'] = None
		context_dict['course'] = None
	return render(request, 'noodle/assessment.html', context_dict)

def register(request):
	return render(request, 'noodle/register.html', {'registered':False})
	
def registerStaff(request):
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = StaffUserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()
			return render(request, 'noodle/register.html', {'registered':True})
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = StaffUserProfileForm()
	return render(request, 'noodle/registerStaff.html',
		{'user_form': user_form,
		'profile_form': profile_form})

def registerStudent(request):
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = StudentUserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()
			return render(request, 'noodle/register.html', {'registered':True})
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = StudentUserProfileForm()
	return render(request, 'noodle/registerStudent.html',
		{'user_form': user_form,
		'profile_form': profile_form})		
		
def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('homepage'))
			else:
				return HttpResponse("Your Noodle account is disabled.")
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied. Invalid email or password.")
	else:
		return render(request, 'noodle/login.html', {})
	
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	# Take the user back to the homepage.
	return HttpResponseRedirect(reverse('noodle:homepage'))
	
def test_pagination(request):
	currPage = pager(request, Staff.objects.all(), 3)
	return render(request, 'noodle/pageTest.html', {'currPage':currPage})

#a helper method to page objects
#request should be passed from the calling view
#object_list is last of objects to page
#perPage is the number of objects which should be put into one page
#returns the current page, which should be passed into the context dict
def pager(request, object_list, perPage):
	paginator = Paginator(object_list, perPage)
	
	page = request.GET.get('page')
	try:
		currPage = paginator.page(page)
	except PageNotAnInteger:
		currPage = paginator.page(1)
	except EmptyPage:
		#returns last page
		currPage = paginator.page(paginator.num_pages)
	
	return currPage

def search(request):
	result_list = []
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
	return render(request, 'noodle/search.html', {'result_list': result_list})