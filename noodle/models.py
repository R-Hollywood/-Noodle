from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    
class Admin(models.Model):
	
	user = models.OneToOneField(User, blank = False, related_name = 'admin')
	
	def save(self, *args, **kwargs):
		self.user.is_superuser = True
		super(Admin, self).save(*args, **kwargs)
	
	def __str__(self): 
		return self.user.username
		
	def __unicode__(self): 
		return self.user.username

class Staff(models.Model):
	
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
		return self.name + "," + self.slug
		
	def __unicode__(self): 
		return self.name
		
class Student(models.Model):

	user = models.OneToOneField(User, blank = False, related_name = 'student')
	
	subject = models.CharField(max_length = 128)
	yearOfStudy = models.IntegerField(default = 1)
	
	enrolledIn = models.ManyToManyField(Course, related_name = 'students')
	
	def __str__(self): 
		return self.user.username
		
	def __unicode__(self): 
		return self.user.username

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
	
	material = models.OneToOneField(Material, unique = True)
	file = models.FileField(blank = True)

	def __str__(self): 
		return self.name
		
	def __unicode__(self): 
		return self.name

class Assessment(models.Model):
	
	material = models.OneToOneField(Material, unique = True)
	submission = models.FileField(blank = True)
	
	deadline = models.DateTimeField()
	submissionDate = models.DateTimeField()

	def __str__(self): 
		return self.name
		
	def __unicode__(self): 
		return self.name


class UserProfile(models.Model):
		
	user = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username


	def __unicode__(self):
		return self.user.username
