from django import forms
from django.contrib.auth.models import User
from noodle.models import *

class SubjectForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter the subject name")
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Subject
		fields = ('name',)

class CourseForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter the course name")
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	
	class Meta:
		model = Course
		exclude = ('subject', 'staffManagers',)

class MaterialForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter the material title")
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	visibility = forms.BooleanField(help_text="Please set visibility")
	
	class Meta:
		model = Material
		exclude = ('courseFrom', 'createdBy',)
		
class FileForm(forms.ModelForm):
	
	class Meta:
		model = File
		fields = ('file',)

class AssessmentForm(forms.ModelForm):

	class Meta:
		model = Assessment
		fields = ('deadline', 'submissionDate',)

		
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password',)
		
	def clean(self):
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		
		if(password and password != confirm_password):
			raise forms.ValidationError("Passwords don't match!")
			
		return self.cleaned_data

class StudentUserProfileForm(forms.ModelForm):

	class Meta:
		model = Student
		fields = ('subject', 'yearOfStudy',)


class StaffUserProfileForm(forms.ModelForm):

	class Meta:
		model = Staff
		fields = ('subject', 'status',)