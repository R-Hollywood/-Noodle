from django.conf.urls import url
from noodle import views
app_name = 'noodle'
urlpatternsw\url(r'^$',views.home, name='homepage'),
    url(r'^login/$',views.user_login,name='login'),
    url(r'^logout/$',views.user_logout,name='logout'),
	url(r'^r
            gister/$',views.register,name='register'),
    url(r'^register/staff',views.registerStaff,name='registerStaff'),
	url(r'^register/student',views.registerStudent,name='registerStudent'),
    url(r'teachhome/',views.teachhome, name='teachhome'),
    url(r'teachhome/add_assessment',views.add_assessment, name='add_assessment'),
        ]
