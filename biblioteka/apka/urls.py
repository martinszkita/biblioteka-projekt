from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('wykaz_ksiazek/',views.wykaz_ksiazek,name='wykaz_ksiazek'),
    path('wyszukiwanie/',views.wyszukiwanie,name='wyszukiwanie'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("wykaz_wypozyczen/", views.wykaz_wypozyczen, name="wykaz_wypozyczen"),
    path("dodaj_wypozyczenie/", views.dodaj_wypozyczenie, name="dodaj_wypozyczenie"),
]