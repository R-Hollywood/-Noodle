from django.contrib import admin
#from noodle.models import Admin, Staff, Student, Course, Subject, Material, File, Assessment, StudentSubmission, Announcement
from noodle.models import *
from noodle.models import UserProfile

admin.site.register(Admin)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Material)
admin.site.register(File)
admin.site.register(Assessment)
admin.site.register(StudentSubmission)
admin.site.register(Announcement)
admin.site.register(UserProfile)