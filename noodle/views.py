from django.shortcuts import render

def home(request):
	return render(request, 'noodle/homepage_extends_base.html', {})

