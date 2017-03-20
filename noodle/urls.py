from django.conf.urls import url
from noodle import views

app_name = 'noodle'
urlpatterns= [ url(r'^$',views.home, name='homepage'),
    url(r'^login/$',views.user_login,name='login'),
    url(r'^logout/$',views.user_logout,name='logout'),
	url(r'^register/$',views.register,name='register'),
    url(r'^register/staff/$',views.registerStaff,name='registerStaff'),
	url(r'^register/student/$',views.registerStudent,name='registerStudent'),
    url(r'studenthome/',views.studenthome, name='studenthome'),
    url(r'teachhome/',views.teachhome, name='teachhome'),
	
	url(r'^(?P<subject_name_slug>[\w\-]+)/$', 
        views.show_subject, name='show_subject'),
	url(r'teachhome/add_subject',views.add_subject, name='add_subject'),
	
	url(r'^(?P<course_name_slug>[\w\-]+)/$', 
        views.show_course, name='show_course'),
	url(r'teachhome/add_course',views.add_course, name='add_course'),
	
	url(r'^(?P<course_name_slug>[\w\-]+)/(?P<material_name_slug>[\w\-]+)/$', 
        views.show_assessment, name='show_assessment'),
    url(r'teachhome/add_assessment',views.add_material, name='add_material'),
        ]
