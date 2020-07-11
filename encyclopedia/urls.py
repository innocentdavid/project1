from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path("wiki", views.index, name="index"),
    
    path('createNewPage', views.createNewPage, name="createNewPage"),
    
    path('search', views.search, name="search"),
    
    path("wiki/<str:title>", views.entry, name="entry"),
    
    path("edit_entry", views.edit_entry, name="edit_entry"),
    
    path("delete_entry/<str:title>", views.delete_entry, name="delete_entry"),
]
