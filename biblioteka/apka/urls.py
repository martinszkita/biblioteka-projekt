from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('wykaz_ksiazek/',views.wykaz_ksiazek,name='wykaz_ksiazek'),
]