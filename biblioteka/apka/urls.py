from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('wykaz_ksiazek/',views.wykaz_ksiazek,name='wykaz_ksiazek'),
    path('wyszukiwanie/',views.wyszukiwanie,name='wyszukiwanie'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
]