from datetime import date
from views import Home, About, Contact, SendInfo, ServiceList, \
    CategoryList, CreateCategory, CreateService, CopyService


def secret_front(request):
    request['data'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Home(),
    '/home/': Home(),
    '/about/': About(),
    '/prices/': ServiceList(),
    '/contact/': Contact(),
    '/send_info/': SendInfo(),
    '/category_list/': CategoryList(),
    '/create_category/': CreateCategory(),
    '/create_service/': CreateService(),
    '/copy_service/': CopyService(),

}
