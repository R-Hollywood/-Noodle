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
	user = models.OneToOneField(User, null = False, related_name = 'admin')
	
	def save(self, *args, **kwargs):
		self.user.is_superuser = True
		super(Admin, self).save(*args, **kwargs)
	
	def __str__(self): 
		return self.user.username
		
	def __unicode__(self): 
		return self.user.username

class Staff(models.Model):

	#'inheritance'
	user = models.OneToOneField(User, null = False, related_name = 'staff')
	
	subject = models.CharField(max_length = 128)
	status = models.CharField(max_length = 128)
	
	def __str__(self): 
		return self.user.username
		
	def __unicode__(self): 
		return self.user.username

class Subject(models.Model):
	name = models.CharField(max_length = 128)
	slug = models.SlugField(unique=True)
	
	class Meta:
		ordering = ['name']
	
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
	
	class Meta:
		ordering = ['name']
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Course, self).save(*args, **kwargs)

	def __str__(self): 
		return self.name
		
	def __unicode__(self): 
		return self.name
		
		
class Student(models.Model):

	#'inheritance'
	user = models.OneToOneField(User, null = False, related_name = 'student')
	
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
	createdBy = models.ForeignKey(Staff, related_name = 'createdMaterial', null = False)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Material, self).save(*args, **kwargs)
		
	def __str__(self): 
		return self.name
		
	def __unicode__(self): 
		return self.name

class File(models.Model):
	
	material = models.OneToOneField(Material, unique = True)
	file = models.FileField(upload_to='noodle/uploads/%Y/%m/%d', null = True)
	#so paginator can access slug directly
	slug = models.SlugField(unique=True)
	datePosted = models.DateTimeField(default=None, null=True)
	
	class Meta:
		ordering = ['datePosted']
	
	def save(self, *args, **kwargs):
		self.slug = self.material.slug
		super(File, self).save(*args, **kwargs)

	def __str__(self): 
		return self.material.name
		
	def __unicode__(self): 
		return self.material.name

class Assessment(models.Model):
	
	material = models.OneToOneField(Material, unique = True)
	submission = models.FileField(null = True)
	#so paginator can access slug directly
	slug = models.SlugField(unique=True)

	deadline = models.DateTimeField()
	submissionDate = models.DateTimeField()
	
	class Meta:
		ordering = ['-submissionDate']
	
	def save(self, *args, **kwargs):
		self.slug = self.material.slug
		super(Assessment, self).save(*args, **kwargs)

	def __str__(self): 
		return self.material.name
		
	def __unicode__(self): 
		return self.material.name
		
class StudentSubmission(models.Model):
	file = models.FileField(upload_to='noodle/submissions/%Y/%m/%d', null = True)
	student = models.ForeignKey(Student, related_name="user_submission")
	assignment = models.ForeignKey(Assessment, related_name="user_submission")
		
class Announcement(models.Model):
	
	name = models.CharField(max_length = 128)
	body = models.CharField(max_length = 1024)
	slug = models.SlugField(unique=True)
	date = models.DateTimeField()
	
	course = models.ForeignKey(Course, null = False, related_name="Announcement")
	
	class Meta:
		ordering = ['-date']
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Announcement, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.course.name + ":" + self.name
		
	def __unicode__(self):
		return self.course.name + ":" + self.name
	
class UserProfile(models.Model):
	#'inheritance'
	user = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username

	def __unicode__(self):
		return self.user.username
