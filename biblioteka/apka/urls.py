from django.urls import path
from . import views

urlpatterns = [
    path("",views.tytuły,name="tytuły"),
    path('ksiazki/',views.display_ksiazki,name='display_ksiazki'),
]