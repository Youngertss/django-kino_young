from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.main_page, name = "main_page"),
    
    path("contacts/", views.contacts, name = "contacts"),
    path("help/", views.help, name = "help"),
    path("help/<slug:clientname>", views.help_forsup, name="help_forsup"),
    
    path("login/", views.LoginUser.as_view(), name = "login"),
    path("logout/", views.logout_user, name = "logout"),
    path("register/", views.RegisterUser.as_view(), name = "register"),
]