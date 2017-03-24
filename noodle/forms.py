from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime
from noodle.models import *

class SubjectForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter the subject name")
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	def clean(self):
		name = self.cleaned_data.get('name')
		
		if(Subject.objects.filter(slug=slugify(name))):
			raise forms.ValidationError("A subject with that name already exists!")
	
	class Meta:
		model = Subject
		fields = ('name',)

class CourseForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter the course name")
	
	def clean(self):
		name = self.cleaned_data.get('name')
		
		if(Course.objects.filter(slug=slugify(name))):
			raise forms.ValidationError("A course with that name already exists!")
	
	class Meta:
		model = Course
		fields = ('name',)

class MaterialForm(forms.ModelForm):
	courseName = None

	name = forms.CharField(max_length=128, help_text="Please enter the material title")
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	visibility = forms.BooleanField(help_text="Please set visibility", initial=True)
	
	def __init__(self, *args, **kwargs):
		self.courseName = kwargs.pop('courseName')
		super(MaterialForm, self).__init__(*args, **kwargs)
		
	def clean(self):
		name = self.cleaned_data.get('name')
		
		if(Material.objects.filter(slug=slugify(name + '_' + self.courseName))):
			raise forms.ValidationError("Material with that name already exists!")
			
	class Meta:
		model = Material
		exclude = ('courseFrom', 'createdBy', 'datePosted')
		
class FileForm(forms.ModelForm):
	
	class Meta:
		model = Doc
		fields = ('file',)

class AssignmentForm(forms.ModelForm):

	deadline = forms.SplitDateTimeField(input_date_formats=['%Y-%m-%d'], input_time_formats=['%H:%M:%S'], help_text="(format: 'YYYY-MM-DD HH:MM:SS')")
		
	class Meta:
		model = Assessment
		fields = ('deadline',)
		
class StudentSubmissionForm(forms.ModelForm):
	
	class Meta:
		model = StudentSubmission
		fields = ('file',)
		
class AnnouncementForm(forms.ModelForm):

	courseName = None
		
	name = forms.CharField(max_length=128, help_text="Please enter the announcement name")
	body = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}))
		
	def __init__(self, *args, **kwargs):
		self.courseName = kwargs.pop('courseName')
		super(AnnouncementForm, self).__init__(*args, **kwargs)
	
	def clean(self):
		name = self.cleaned_data.get('name')
		
		if(Announcement.objects.filter(slug=slugify(name + '_' + self.courseName))):
			raise forms.ValidationError("An announcement with that name already exists!")
		
	class Meta:
		model = Announcement
		fields = ('name', 'body',)
		
class UserForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password',)
		
	def clean(self):
	
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		
		if(User.objects.filter(username = username).exists()):
			raise forms.ValidationError("Username is already in use.")
			
		if(User.objects.filter(email = email).exists()):
			raise forms.ValidationError("Email is already in use.")
		
		if(password and password != confirm_password):
			raise forms.ValidationError("Passwords don't match!")
			
		return self.cleaned_data

class StudentUserProfileForm(forms.ModelForm):
	
	subject = forms.ChoiceField(choices=[])
	
	def __init__(self, *args, **kwargs):
		super(StudentUserProfileForm, self).__init__(*args, **kwargs)
	
		subjects = Subject.objects.all()
		
		subjectList = []
		for subject in subjects:
			subjectList.append((subject.name,subject.name))
		
		self.fields['subject'].choices = subjectList
		
	class Meta:
		model = Student
		fields = ('subject', 'yearOfStudy')
		
class StaffUserProfileForm(forms.ModelForm):

	subject = forms.ChoiceField(choices=[])
	
	def __init__(self, *args, **kwargs):
		super(StaffUserProfileForm, self).__init__(*args, **kwargs)
		
		subjects = Subject.objects.all()
		
		subjectList = []
		for subject in subjects:
			subjectList.append((subject.name,subject.name))
		
		self.fields['subject'].choices = subjectList

	class Meta:
		model = Staff
		fields = ('subject', 'status',)
	
class MarkingForm(forms.ModelForm):
	studentName = forms.CharField(widget=forms.HiddenInput(), required=False)

	def __init__(self, *args, **kwargs):
		student = kwargs.pop('student')
		super(MarkingForm, self).__init__(*args, **kwargs)
	
		if(student != ''):
			self.fields['studentName'].initial = student
		
	class Meta:
		model = StudentSubmission
		fields = ('mark', 'studentName')
	
class StudentSearchForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('username',)
		
	def clean(self):
		username = self.cleaned_data.get('username')
		
		student = Student.objects.filter(user=User.objects.filter(username = username))
		
		if(not student.exists()):
			raise forms.ValidationError("No such student!")
