from django.conf.urls import url
from noodle import views
app_name = 'noodle'
urlpatterns = [
    url(r'^$',views.home, name='homepage'),
    ]
