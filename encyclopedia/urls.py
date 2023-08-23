from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>",views.entry , name="entry"),
    path("wiki/<str:entry>/edit",views.edit , name="edit"),
    path("random" , views.random_entry, name= "random_entry"),
    path("newEntry" , views.new_entry, name="new_entry"),
    path("search",views.search_entry, name="search_entry")
]
