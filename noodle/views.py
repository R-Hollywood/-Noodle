from django import shortcuts
from noodle.models import *
from noodle.forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

def render(request, page, context_dict):
	
	context_dict['tier'] = 0
	user = request.user
	
	if(user.is_authenticated()):
		
		homePage = (page == 'noodle/homepage_extends_base.html')
		
		if(homePage):
			page = 'noodle/studenthome.html'
			
		if(hasattr(user, 'staff') and user.staff != None):
			context_dict['tier'] = 1
			if(homePage):
				page = 'noodle/teachhome.html'
				
		if(hasattr(user, 'admin') and user.admin != None):
			context_dict['tier'] = 2
			if(homePage):
				page = 'noodle/teachhome.html'

	return shortcuts.render(request, page, context_dict)

def home(request):
	
	subject_list = Subject.objects
	course_list = Course.objects
	context_dict = {'subject': subject_list, 'course': course_list}
	return render(request, 'noodle/homepage_extends_base.html', context_dict)

@login_required
def teachhome(request):
	context_dict = {}
	return render(request,'noodle/teachhome.html', context_dict)
	
@login_required
def studenthome(request):
	context_dict = {}
	return render(request,'noodle/studenthome.html', context_dict)
	
@login_required	
def show_subject(request, subject_name_slug):
	print subject_name_slug
	context_dict = {}
	context_dict['subject_name'] = None
	try:
		subject = Subject.objects.get(slug=subject_name_slug)
		courses = Course.objects.filter(subject=subject)
		courses = pager(request, courses, 10)
		context_dict['courses'] = courses
		context_dict['subject'] = subject
		context_dict['subject_name'] = subject.name
	except Subject.DoesNotExist:
		context_dict['subject'] = None
		context_dict['course'] = None
	print context_dict
	return render(request, 'noodle/subject.html', context_dict)
	
@login_required	
def show_course(request, course_name_slug):
	context_dict = {}
	#update user's visited courses somewhere
	try:
		course = Course.objects.get(slug=course_name_slug)
		material = Material.objects.filter(courseForm=course)
		context_dict['course'] = course
		context_dict['material'] = material
	except Subject.DoesNotExist:
		context_dict['course'] = None
		context_dict['material'] = None
	return render(request, 'noodle/subject.html', context_dict)
	
@login_required	
def show_assessment(request, assessment_name_slug):
	return 'stub'
	
@login_required	
def show_announcements(request, course_name_slug):
	return 'stub'

@login_required	
def add_material(request):
	form = MaterialForm()
	fileForm = FileForm()
	assignmentForm = AssignmentForm()
	
	if request.method == 'POST':
		form = MaterialForm(request.POST)
		fileForm = FileForm(request.POST, request.FILES)
		assignmentForm = AssignmentForm(request.POST)
		
		if form.is_valid() and fileForm.is_valid():
			ass = form.save(commit=True)
			fileForm.save(commit=True)
			print(ass, ass.slug)
			return teachhome(request)
		elif form.is_valid() and assignmentForm.is_valid():
			ass = form.save(commit=True)
			assignmentForm.save(commit=True)
			print(ass, ass.slug)
			return teachhome(request)
		else:
			print(form.errors)
			
	context_dict = {'form': form, 'file_form': fileForm, 'assignment_form': assignmentForm}
	return render(request, 'noodle/add_material.html', context_dict)
	
@login_required	
def add_subject(request):
	form = SubjectForm()
	if request.method == 'POST':
		form = SubjectForm(request.POST)
		if form.is_valid():
			sub = form.save(commit=True)
			print(sub, sub.slug)
			return index(request)
		else:
			print(form.errors)
	
	return render(request, 'noodle/add_subject.html', {'form': form})

@login_required
def add_course(request, subject_name_slug):
    try:
        course =  Course.objects.get(slug=subject_name_slug)
    except Course.DoesNotExist:
        course = None
    
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            if subject:
                course = form.save(commit=False)
                course.category = category
                course.views = 0
                course.save()
                return show_subject(request, subject_name_slug)
        else:
            print(form.errors)
    
    context_dict = {'form':form, 'subject': subject}
    return render(request, 'noodle/add_course.html', context_dict)

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
	return HttpResponseRedirect(reverse('homepage'))
	
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
