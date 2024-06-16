from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.conf import settings
from django.http import HttpResponse
from .utils import read_operation, write_operation
import time
import datetime

@login_required
def home(request):
    context={'username':request.user.username}
    return render(request, 'home.html',context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            time.sleep(1)
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            #print(request.user)
            response = HttpResponse('home')
        
            return response  # Redirect to home page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# czy to jest potrzebne ? \/
def tytuły(request):
    # Connect to database
    with connection.cursor() as cursor:
        # Execute SQL query
        cursor.execute("SELECT `tytul` id_tytulu FROM tytul")

        # Fetch all rows
        titles = cursor.fetchall()

    # Pass data to template
    return render(request, 'titles.html', {'titles': titles})
# czy to jest potrzebne ? /\


@login_required
def wykaz_ksiazek(request):
    id_autora=request.GET.get('autor_id', 'dowolne')
    id_gatunku= request.GET.get('gatunek_id', 'dowolne')
    print(id_autora)
    print(id_gatunku)

    query_autorzy = "SELECT imie, nazwisko, id_autora FROM autor"
    autorzy=read_operation(query_autorzy)

    query_gatunki = "SELECT nazwa, id_gatunku FROM gatunek"
    gatunki=read_operation(query_gatunki)

    d='dowolne'

    if id_autora !=d and id_gatunku != d:
         query_results = "SELECT autor.imie, autor.nazwisko, gatunek.nazwa FROM autor JOIN tytul ON tytul.id_autora=autor.id_autora JOIN gatunek on tytul.id_gatunku=gatunek.id_gatunku WHERE autor.id_autora=%s AND gatunek.id_gatunku = %s"
         params = [id_autora, id_gatunku]
         print(' case 1')
    elif id_autora == d and id_gatunku != d:
        query_results = "SELECT autor.imie, autor.nazwisko, gatunek.nazwa FROM autor JOIN tytul ON tytul.id_autora=autor.id_autora JOIN gatunek on tytul.id_gatunku=gatunek.id_gatunku WHERE gatunek.id_gatunku = %s"
        params = [id_gatunku]
        print("case 2")
    elif id_autora != d and id_gatunku == d:
        query_results = "SELECT autor.imie, autor.nazwisko, gatunek.nazwa FROM autor JOIN tytul ON tytul.id_autora=autor.id_autora JOIN gatunek on tytul.id_gatunku=gatunek.id_gatunku WHERE autor.id_autora=%s"
        params = [id_autora]
        print('case3')
    else : # oba dowolne
        query_results = "SELECT autor.imie, autor.nazwisko, gatunek.nazwa FROM autor JOIN tytul ON tytul.id_autora=autor.id_autora JOIN gatunek on tytul.id_gatunku=gatunek.id_gatunku"
        params = []
        print('case 4')

    #params=[]
    results = read_operation(query_results, params)
    print(results)
    return render(request, 'wykaz_ksiazek.html', {'ksiazki': results, 'autorzy' : autorzy, 'gatunki':gatunki})

@login_required
def wykaz_wypozyczen(request):
    query = "SELECT czytelnik.imie, czytelnik.nazwisko, tytul.tytul, autor.imie, autor.nazwisko, wypozyczenie.data_wypozyczenia, wypozyczenie.data_zwrotu from wypozyczenie JOIN czytelnik on czytelnik.id_czytelnika=wypozyczenie.id_czytelnika JOIN ksiazka on ksiazka.id_ksiazki=wypozyczenie.id_ksiazki JOIN tytul on tytul.id_tytulu=ksiazka.id_tytulu JOIN autor on autor.id_autora=tytul.id_autora"
    wypozyczenia = read_operation(query)
    return render(request, 'wykaz_wypozyczen.html', {'wypozyczenia': wypozyczenia})

@login_required
def dodaj_wypozyczenie(request):
    if request.method == 'POST':
        id_ksiazki = request.POST.get('id_ksiazki')
        data_wypozyczenia = request.POST.get('data_wypozyczenia')
        data_zwrotu = request.POST.get('data_zwrotu')
        id_czytelnika = request.POST.get('id_czytelnika')
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO wypozyczenie (id_ksiazki, data_wypozyczenia, data_zwrotu, id_czytelnika)
                VALUES (%s, %s, %s, %s)
            """, [id_ksiazki, data_wypozyczenia, data_zwrotu, id_czytelnika])
        
        return redirect(request.path_info)  # Redirect to a success URL or another view

    return render(request, 'dodaj_wypozyczenie.html')

@login_required
def usun_wypozyczenie(request):
    id_wypozyczenia = request.GET.get('wypozyczenie_id','')
    if id_wypozyczenia:
        query_delete = "DELETE from wypozyczenie WHERE wypozyczenie.id_wypozyczenia=%s"
        params = [id_wypozyczenia]
        wypozyczenia = write_operation(query_delete, params)

   
    query = "SELECT wypozyczenie.id_wypozyczenia, czytelnik.imie, czytelnik.nazwisko, tytul.tytul, autor.imie, autor.nazwisko, wypozyczenie.data_wypozyczenia, wypozyczenie.data_zwrotu from wypozyczenie JOIN czytelnik on czytelnik.id_czytelnika=wypozyczenie.id_czytelnika JOIN ksiazka on ksiazka.id_ksiazki=wypozyczenie.id_ksiazki JOIN tytul on tytul.id_tytulu=ksiazka.id_tytulu JOIN autor on autor.id_autora=tytul.id_autora"
    
    wypozyczenia = read_operation(query)

    print(wypozyczenia)

    return render(request, 'usun_wypozyczenie.html', {'wypozyczenia': wypozyczenia})


@login_required
def wyszukiwanie(request):
    query = request.GET.get('query', '')
    search_by = request.GET.get('search_by', 'tytul') #jeśli nie wyspecyfikowano inaczej to szukamy po tytule
    results = []

    if query:
        if search_by == 'tytul':
            sql_query = "SELECT tytul, autor.imie, autor.nazwisko, opis FROM tytul JOIN autor on autor.id_autora=tytul.id_autora WHERE tytul LIKE %s"
        elif search_by == 'opis':
            sql_query = "SELECT tytul , autor.imie, autor.nazwisko, opis FROM tytul JOIN autor on autor.id_autora=tytul.id_autora WHERE opis LIKE %s"
        elif search_by == 'autor':
            sql_query = "SELECT tytul, autor.imie, autor.nazwisko, opis  FROM tytul JOIN autor on autor.id_autora=tytul.id_autora WHERE autor.imie LIKE %s OR autor.nazwisko LIKE %s"
        params = ['%' + query + '%', '%' + query + '%'] if search_by == 'autor' else ['%' + query + '%']
        results = read_operation(sql_query, params)
    return render(request, 'wyszukiwanie.html', {'results': results})
