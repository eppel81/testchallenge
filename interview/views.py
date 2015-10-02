from django.shortcuts import render

from models import Interview

# from forms import InterElemForm

def show_interviews(request):
    interviews = Interview.objects.all() # order_by('create_date')

def create_interview(request):

    return render(request, 'interview/createInterview.html', {'title': 'Interview creation'})