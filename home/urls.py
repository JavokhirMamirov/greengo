from django.urls import path

from home.views import home_view

urlpatterns = [
    path('/home', home_view, name='home')
]