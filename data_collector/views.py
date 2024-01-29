from django.shortcuts import render, redirect
from .models import Search
from .forms import SearchForm, SearchFormUpdate
from datetime import datetime
from django.views.generic import DeleteView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
import requests

@login_required
def search_home(request):
    searches = Search.objects.filter(created_by = request.user).order_by('-date')[:5]
    #searches = Search.objects.order_by('-date')[:5]
    return render(request, 'data_collector/search_index.html', {'searches' : searches})

class SearchDetailView(DeleteView):
    model = Search
    template_name = 'data_collector/details_view.html'
    context_object_name = 'search'

class SearchUpdateView(UpdateView):
    model = Search
    template_name = 'data_collector/update.html'

    form_class = SearchFormUpdate

class SearchDeleteView(DeleteView):
    model = Search
    success_url = '/searches/'
    template_name = 'data_collector/delete.html'

def validate_name(request):
    user_searches = [el.name for el in Search.objects.filter(created_by = request.user)]
    return request.POST['name'] in user_searches

def validate_links(request):
    links = [el.strip() for el in request.POST['link'].split('\n')]
    invalid = []
    processed = []
    for link in links:
        if link in processed:
            invalid.append(link)
        if not link.startswith('https://vk.com/'):
            invalid.append(link)
        else:
            response = requests.get(link)
            if response.status_code != 200:
                invalid.append(link)
        processed.append(link)
    return invalid

@login_required
def create_search(request):
    error = ''
    form = SearchForm()
    if request.method == 'POST':
        invalid = validate_links(request)
        if validate_name(request):
            error += 'Such name already exists\n'
            form = SearchForm(data = request.POST.copy())
        elif invalid:
            for link in invalid:
                error += 'Check link: ' + link + '\n'
            form = SearchForm(data = request.POST.copy())
        else:
            form = SearchForm(data = request.POST, created_by = request.user)
            #form.user_id = user.id
            if form.is_valid():
                form.save()
                return redirect('search_home')
            else:
                error = 'Invalid request parameters'
    
    data = {
        'form' : form,
        'error': error
    }
    return render(request, 'data_collector/create.html', data)

@login_required
def update_search(request, pk):
    error = ''
    instance = Search.objects.get(id=pk)
    form = SearchFormUpdate(request.POST, instance=instance)
    if request.method == 'POST':
        if instance.name != request.POST['name'] and validate_name(request):
            error += 'Such name already exists\n'
            form = SearchFormUpdate(data = request.POST.copy())
        else:
            if form.is_valid():
                form.save()
                return redirect(instance.get_absolute_url())
            else:
                error = 'Invalid request parameters'
    
    data = {
        'form' : form,
        'error': error
    }
    return render(request, 'data_collector/update.html', data)