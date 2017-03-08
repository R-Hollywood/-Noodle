from django.shortcuts import render

def home(request):
	render(request, 'noodle/homepage_extends_base', {})
