from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.index, name="index"),
    path('createNewPage', views.createNewPage, name="createNewPage"),
    path('search', views.q_entry, name="q_entry"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("delete_entry/<str:title>", views.delete_entry, name="delete_entry")
]
