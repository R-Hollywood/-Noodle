from django.conf.urls import url
from django.contrib import admin
from noodle import views
from django.conf.urls import include
#requires pip install django-registration-redux==1.4
from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
    def get_success_url(self,user):
        return '/noodle/'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^noodle/',include('noodle.urls')),
    url(r'^$',views.home, name='homepage'),
    url(r'^accounts/register/$',
        MyRegistrationView.as_view(),
            name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),

]
