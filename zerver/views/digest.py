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

def query(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return fetchall(cursor)

def ui(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<pre>Hello</pre>')

def digest(request: HttpRequest) -> HttpResponse:
    resp = []
    new_streams = query('''
       SELECT s.id, s.name, s.date_created::date FROM zerver_stream s
       WHERE date_created > now()  - INTERVAL '1 week'
       ORDER BY date_created desc
       LIMIT 10
    ''')

    resp.append({"title": "New Streams", "type": "streams", "items": new_streams})

    d_hot_topics = query('''
      SELECT *
      FROM zerver_message m
      WHERE m.pub_date > now()  - INTERVAL '1 day'
      LIMIT 10
    ''')

    resp.append({"title": "Topics of the week", "type": "topics", "items": d_hot_topics})

    w_hot_topics = query('''
      SELECT *
      FROM zerver_message m
      WHERE m.pub_date > now()  - INTERVAL '1 week'
      LIMIT 10
    ''')

    resp.append({"title": "Topics of the day", "type": "topics", "items": w_hot_topics})


    return HttpResponse(json.dumps(resp, indent=0, sort_keys=False, default=str), content_type="application/json")
