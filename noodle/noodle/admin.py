from django.contrib import admin
from rango.models import Admin, Staff, Student, Course, Subject, Material, File, Assessment
	
class PageAdmin(admin.ModelAdmin):
	list_display = ('category', 'title', 'url')
	
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}

admin.site.register(Admin)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Material)
admin.site.register(File)
admin.site.register(Assessment)