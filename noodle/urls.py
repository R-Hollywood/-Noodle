from django.conf.urls import url
from noodle import views
app_name = 'noodle'
urlpatterns = [
    url(r'^$',views.home, name='homepage'),
    url(r'teachhome/',views.teachhome, name='teachhome'),
    url(r'^login/$',views.user_login,name='login'),
    url(r'^logout/$',views.user_logout,name='logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'teachhome/',views.teachhome, name='teachhome'),
        ]
