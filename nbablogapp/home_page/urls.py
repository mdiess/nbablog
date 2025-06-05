from os import name
from django.urls import re_path
from nbablogapp.home_page import views
from django.views.generic import RedirectView

app_name = 'home_page'
urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^interact_post/$', views.interact_post, name='interact_post'),
]