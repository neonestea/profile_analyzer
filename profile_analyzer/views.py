from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    #return HttpResponse("Hello, Django!")
    context={}
    return render(request, 'profile_analyzer/home.html', context)

# Create your views here.
