from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from django.db import models

#as far as I can tell this functionality is encapsulated by File
#please, whoever added this take a look at File
#class Document(models.Model):
    #docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    
class Admin(models.Model):
	#name, password, email, forename and surname attributes are included with django's 'User' model
	#in our case we should simply set the username to be the same as the email address
	#because django has a lot involved in the underlying framework
	user = models.OneToOneField(User, blank = False, related_name = 'admin')
	
	def save(self, *args, **kwargs):
		self.user.is_superuser = True
		super(Admin, self).save(*args, **kwargs)
	
	def __str__(self): 
		return self.user.username
		
	def __unicode__(self): 
		return self.user.username

class Staff(models.Model):
	#'inheritance'
	user = models.OneToOneField(User, blank = False, related_name = 'staff')
	
	subject = models.CharField(max_length = 128)
	status = models.CharField(max_length = 128)
	
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
	slug = models.SlugField(unique=True)
	subject = models.ForeignKey(Subject)
	
	staffManagers = models.ManyToManyField(Staff, related_name = 'courses')
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Course, self).save(*args, **kwargs)

	def __str__(self): 
		return self.name
		
	def __unicode__(self): 
		return self.name
		
class Student(models.Model):
	#'inheritance'
	user = models.OneToOneField(User, blank = False, related_name = 'student')
	
	subject = models.CharField(max_length = 128)
	yearOfStudy = models.IntegerField(default = 1)
	
	visitedCourse = models.ManyToManyField(Course, through = 'VisitedCourse')
	enrolledIn = models.ManyToManyField(Course, related_name = 'enrolledStudents')
	
	def __str__(self): 
		return self.user.username
		
	def __unicode__(self): 
		return self.user.username
		
#used to track course page visits from students
#basically allows a 'date' field in the the join table
class VisitedCourse(models.Model):
	date = models.DateTimeField()
	
	student = models.ForeignKey(Student, related_name='courseVisit')
	course = models.ForeignKey(Course, related_name='courseVisit')
	
	def __str__(self): 
		return self.student.name + "/" + self.course.name + "/" + date
		
	def __unicode__(self): 
		return self.student.name + "/" + self.course.name + "/" + date

class Material(models.Model):

	name = models.CharField(max_length = 128)
	visibility = models.BooleanField()
	slug = models.SlugField(unique=True)
	
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
	file = models.FileField(upload_to='noodle/uploads/%Y/%m/%d', blank = True)
	#so paginator can access slug directly
	slug = models.SlugField(unique=True)
	
	def save(self, *args, **kwargs):
		self.slug = self.material.slug
		super(File, self).save(*args, **kwargs)

	def __str__(self): 
		return self.material.name
		
	def __unicode__(self): 
		return self.material.name

class Assessment(models.Model):
	#'inheritance'
	material = models.OneToOneField(Material, unique = True)
	submission = models.FileField(blank = True)
	#so paginator can access slug directly
	slug = models.SlugField(unique=True)

	deadline = models.DateTimeField()
	submissionDate = models.DateTimeField()
	
	def save(self, *args, **kwargs):
		self.slug = self.material.slug
		super(Assessment, self).save(*args, **kwargs)

	def __str__(self): 
		return self.material.name
		
	def __unicode__(self): 
		return self.material.name
		
class Announcement(models.Model):
	
	title = models.CharField(max_length = 128)
	body = models.CharField(max_length = 1024)
	slug = models.SlugField(unique=True)
	date = models.DateTimeField()
	
	course = models.ForeignKey(Course, blank = False, related_name="Announcement")
	
	def save(self, *args, **kwargs):
		self.slug = slugify(title)
		super(Material, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.course.name + ":" + self.title
		
	def __unicode__(self):
		return self.course.name + ":" + self.title
	
#do we need this?
class UserProfile(models.Model):
	# Links UserProfile to a User model instance
	user = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username

	def __unicode__(self):
		return self.user.username
