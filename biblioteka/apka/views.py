from django.shortcuts import render
from django.db import connection

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

def home(request):
    return render(request, 'home.html')

