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
	url(r'^pager_debug/$',views.test_pagination,name='pager_debug'),
	url(r'^(?P<subject_name_slug>[\w\-]+)/(?P<course_name_slug>[\w\-]+)/add_material/$',views.add_material, name='add_material'),
	
	url(r'^(?P<subject_name_slug>[\w\-]+)/$', 
        views.show_subject, name='show_subject'),
		
	url(r'^(?P<subject_name_slug>[\w\-]+)/(?P<course_name_slug>[\w\-]+)/$', 
        views.show_course, name='show_course'),
	
	url(r'^(?P<subject_name_slug>[\w\-]+)/(?P<course_name_slug>[\w\-]+)/announcements/$', 
        views.show_announcements, name='show_announcements'),
		
	url(r'^(?P<subject_name_slug>[\w\-]+)/(?P<course_name_slug>[\w\-]+)/announcements/(?P<announcement_name_slug>[\w\-]+)/$', 
        views.show_announcement, name='show_announcement'),
	
	url(r'^(?P<subject_name_slug>[\w\-]+)/(?P<course_name_slug>[\w\-]+)/(?P<assessment_name_slug>[\w\-]+)/$', 
        views.show_assessment, name='show_assessment'),
	
        ]
