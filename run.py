from concert_framework.main import ConcertFramework
from wsgiref.simple_server import make_server
from views import routes
from helper import settings

application = ConcertFramework(settings, routes)

with make_server('', 8000, application) as server:
    print('Working!!')
    server.serve_forever()

