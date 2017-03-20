from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    
class Admin(models.Model):
	#name, password, email, forename and surname attributes are included with django's 'User' model
	#in our case we should simply set the username to be the same as the email address
	#because django has a lot involved in the underlying framework
	user = models.OneToOneField(User, blank = False)
	
	def save(self, *args, **kwargs):
		self.user.is_superuser = True
		super(Admin, self).save(*args, **kwargs)
	
	def __str__(self): 
		return self.user.username
		
	def __unicode__(self): 
		return self.user.username

class Staff(models.Model):
	#'inheritance'
	user = models.OneToOneField(User, blank = False)
	
	subject = models.CharField(max_length = 128)
	status = models.CharField(max_length = 128)
	
	#is this field actually necessary?
	#I don't think so, but I included it for the time being
	#staMaintainedBy = models.ManyToManyField(Admin, related_name = 'staMaintenanceOf')

	def __str__(self): 
		return self.user.username
		
	def __unicode__(self): 
		return self.user.username

class Subject(models.Model):
	name = models.CharField(max_length = 128)
	slug = models.SlugField(unique=True)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Subject, self).save(*args, **kwargs)
	
	def __str__(self): 
		return self.name
		
	def __unicode__(self): 
		return self.name
	
class Course(models.Model):

	name = models.CharField(max_length = 128)
	#I'm assuming we're going to need different urls for each course page here
	slug = models.SlugField(unique=True)
	#I'm treating this as another object for ease of implementation
	#but as in the ER diagram it's practically just an attribute
	subject = models.ForeignKey(Subject)
	
	staffManagers = models.ManyToManyField(Staff, related_name = 'courses')
	#couMaintainedBy = models.ManyToManyField(Admin, related_name = 'couMaintenanceOf')
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Course, self).save(*args, **kwargs)

	def __str__(self): 
		return self.name + "," + self.slug
		
	def __unicode__(self): 
		return self.name
		
class Student(models.Model):
	#'inheritance'
	user = models.OneToOneField(User, blank = False)
	
	subject = models.CharField(max_length = 128)
	yearOfStudy = models.IntegerField(default = 1)
	
	enrolledIn = models.ManyToManyField(Course, related_name = 'students')
	#stuMaintainedBy = models.ManyToManyField(Admin, related_name = 'stuMaintenanceOf')
	
	def __str__(self): 
		return self.user.username
		
	def __unicode__(self): 
		return self.user.username

class Material(models.Model):

	name = models.CharField(max_length = 128)
	visibility = models.BooleanField()
	#I'm assuming we're going to need different urls for each piece of material here
	slug = models.SlugField(unique=True)
	
	#actually, I think this is an implicit relationship from the student accessing the course
	#accessedBy = models.ManyToManyField(Student, related_name = 'hasAccess')
	courseFrom = models.ForeignKey(Course, related_name = 'material')
	createdBy = models.ForeignKey(Staff, related_name = 'createdMaterial', blank = False)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Material, self).save(*args, **kwargs)
		
	def __str__(self): 
		return self.name
		
	def __unicode__(self): 
		return self.name

class File(models.Model):
	#'inheritance'
	material = models.OneToOneField(Material, unique = True)
	

	def __str__(self): 
		return self.name
		
	def __unicode__(self): 
		return self.name

class Assessment(models.Model):
	#'inheritance'
	material = models.OneToOneField(Material, unique = True)
	
	deadline = models.DateTimeField()
	submissionDate = models.DateTimeField()

	def __str__(self): 
		return self.name
		
	def __unicode__(self): 
		return self.name


class UserProfile(models.Model):
		# Links UserProfile to a User model instance
	user = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username


	def __unicode__(self):
		return self.user.username
