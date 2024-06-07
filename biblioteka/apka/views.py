from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import connection
from .utils import read_operation, write_operation
import time


#def home(request):
#    return render(request, 'home.html')
#========================================
@login_required
def home(request):
    return render(request, 'home.html', {})

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
            return redirect('home')  # Redirect to home page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

#========================================

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
    query = "SELECT id_tytulu, tytul FROM tytul"
    ksiazki = read_operation(query)
    return render(request, 'wykaz_ksiazek.html', {'ksiazki': ksiazki})


@login_required
def wyszukiwanie(request):
    query = request.GET.get('query', '')
    results = []
    if query:
        sql_query = "SELECT tytul FROM tytul WHERE tytul LIKE %s OR opis LIKE %s"
        params = ['%' + query + '%', '%' + query + '%']
        results = read_operation(sql_query, params)
    return render(request, 'wyszukiwanie.html', {'results': results})
