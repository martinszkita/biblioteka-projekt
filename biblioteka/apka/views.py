from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import connection

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
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')  # Redirect to home page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

#========================================


def tytuły(request):
    # Connect to database
    with connection.cursor() as cursor:
        # Execute SQL query
        cursor.execute("SELECT `tytul` id_tytulu FROM tytul")

        # Fetch all rows
        titles = cursor.fetchall()

    # Pass data to template
    return render(request, 'titles.html', {'titles': titles})

def wykaz_ksiazek(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_tytulu, tytul FROM tytul")
        ksiazki=cursor.fetchall()
    return render(request, 'wykaz_ksiazek.html', {'ksiazki': ksiazki})



def wyszukiwanie(request):
    query = request.GET.get('query', '')
    results = []
    if query:
        with connection.cursor() as cursor:
            # cursor.execute("SELECT tytul FROM tytul WHERE tytul LIKE %s", ['%' + query + '%'])
            cursor.execute("SELECT tytul FROM tytul WHERE tytul LIKE %s OR opis LIKE %s", ['%' + query + '%', '%' + query + '%']) # razem z szukaniem w opisie
            results = cursor.fetchall()
    return render(request, 'wyszukiwanie.html', {'results': results})
