from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.wiki, name="wiki"),
    path("search/", views.search, name="search"),
    path("new/", views.newpage, name="newpage"),
    path("wiki/<str:entry>/edit/", views.edit, name="edit"),
    path("random/", views.randompage, name="random")
]
