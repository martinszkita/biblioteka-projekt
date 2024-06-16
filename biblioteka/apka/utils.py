
from django.db import connections, transaction

def read_operation(query, params=None):
    with transaction.atomic(using='slave'):
        with connections['slave'].cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

def write_operation(query, params=None):
    try:
        with transaction.atomic(using='default'):
            with connections['default'].cursor() as cursor:
                cursor.execute(query, params)
    except Exception as e:
        # Handle the exception (e.g., logging)
        print(f"Error during write operation: {e}")   
        raise          
