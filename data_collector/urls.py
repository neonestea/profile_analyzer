from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_home, name='search_home'),
    path('create', views.create_search, name='create_search'),
    path('<uuid:pk>', views.SearchDetailView.as_view(), name='search_detail'),
    path('<uuid:pk>/delete', views.SearchDeleteView.as_view(), name='search_delete'),
    path('<uuid:pk>/update', views.update_search, name='search_update')
]