
from django.db import connections, transaction

def read_operation(query, params=None):
    with transaction.atomic(using='slave'):
        with connections['slave'].cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

def write_operation(query, params=None):
    with transaction.atomic(using='default'):
        with connections['default'].cursor() as cursor:
            cursor.execute(query, params)
