from django import forms
from django.contrib.auth.models import User
from noodle.models import Page,Category, UserProfile

class DocumentForm(forms.Form):

    docfile = forms.FileField(
        label='Select a file'
    )

class PageForm(forms.Form):
    
