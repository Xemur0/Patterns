from datetime import date
from views import Home, About, Prices, Contact, SendInfo


def secret_front(request):
    request['data'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Home(),
    '/home/': Home(),
    '/about/': About(),
    '/prices/': Prices(),
    '/contact/': Contact(),
    '/send_info/': SendInfo(),

}