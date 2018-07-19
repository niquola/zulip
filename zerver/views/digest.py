from django.http import HttpResponseBadRequest, HttpRequest, HttpResponse
from django.db import connection
import json

def fetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def digest(request: HttpRequest) -> HttpResponse:
   with connection.cursor() as cursor:
     cursor.execute('''
       SELECT s.id, s.name, count(*) as num_messages
       FROM zerver_stream s
       JOIN zerver_recipient r ON r.type=2 and  r.type_id=s.id
       JOIN zerver_message m ON m.recipient_id = r.id
       GROUP BY s.id, s.name
       ORDER BY count(*) desc
     ''')
     rows = fetchall(cursor)

   return HttpResponse('<pre>%s</pre>' % json.dumps(rows, indent=0, sort_keys=False))
