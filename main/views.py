from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    '''
    Function to open main page
    '''
    data = {
        'title': 'Main page',
        'values': ['Some', 'words'],
        'person': {
            'name': 'Anastasia',
            'age': 25
            }
        }
    return render(request, 'main/index.html', data)

def about(request):
    '''
    Function to open page about project
    '''
    #return HttpResponse("About project")
    return render(request, 'main/about.html')

def contacts(request):
    '''
    Function to open page with contacts
    '''
    #return HttpResponse("About project")
    return render(request, 'main/contacts.html')

