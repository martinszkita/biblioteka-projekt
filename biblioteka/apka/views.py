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




#from django.shortcuts import render,HttpResponse
# Create your views here.
#def home(request):
#    return render(request,"base.html")