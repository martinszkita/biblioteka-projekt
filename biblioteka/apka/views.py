from django.shortcuts import render
from django.db import connection

def tytuły(request):
    # Connect to database
    with connection.cursor() as cursor:
        # Execute SQL query
        cursor.execute("SELECT title, title_id FROM tytuły")

        # Fetch all rows
        titles = cursor.fetchall()

    # Pass data to template
    return render(request, 'titles.html', {'titles': titles})



def display_ksiazki(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_ksiazki, tytul FROM ksiazka")
        ksiazki=cursor.fetchall()
    return render(request, 'myapp/display_ksiazki.html', {'ksiazki': ksiazki})

    