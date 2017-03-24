from django.contrib import admin
from noodle.models import *
from noodle.models import UserProfile

admin.site.register(Admin)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Material)
admin.site.register(Doc)
admin.site.register(Assessment)
admin.site.register(StudentSubmission)
admin.site.register(Announcement)
admin.site.register(UserProfile)