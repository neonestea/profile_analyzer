from django.shortcuts import render, redirect
from .models import Search, ProfileInfo, Result
from .forms import SearchForm, SearchFormUpdate
from datetime import datetime
from django.views.generic import DeleteView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
import requests
from .vk_api_processor import check_user, start_collecting_info, check_group
from threading import Thread

@login_required
def search_home(request):
    searches = Search.objects.filter(created_by = request.user).order_by('-date')
    #searches = Search.objects.order_by('-date')[:5]
    return render(request, 'data_collector/search_index.html', {'searches' : searches})

@login_required
def profile_info(request, pk):
    search = Search.objects.get(id=pk)
    info = ProfileInfo.objects.filter(connected_search = search)
    return render(request, 'data_collector/info_view.html', {'info' : info, 'search' : search})


@login_required
def result(request, pk):
    search = Search.objects.get(id=pk)
    info = Result.objects.filter(connected_search = search)
    return render(request, 'data_collector/results_view.html', {'info' : info, 'search' : search})


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
            elif check_user(link) is None and check_group(link) is None:
                invalid.append(link)
        processed.append(link)
    return invalid

@login_required
def create_search(request):
    error = ''
    form = SearchForm()
    if request.method == 'POST':
        invalid = validate_links(request)
        #if validate_name(request):
            #error += 'Such name already exists\n'
        #    form = SearchForm(data = request.POST.copy())
        if invalid:
            for link in invalid:
                error += 'Only links to groups or users allowed. Check: ' + link + '\n'
            form = SearchForm(data = request.POST.copy())
        else:
            form = SearchForm(data = request.POST, created_by = request.user)
            #form.user_id = user.id
            if form.is_valid():
                model_instance = form.save()
                th = Thread(target=start_collecting_info, args=(model_instance, form.cleaned_data['link'],))
                th.start()
                #start_collecting_info(model_instance, form.cleaned_data['link'])
                return redirect('search_home')
                
                #return redirect('search_home')
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