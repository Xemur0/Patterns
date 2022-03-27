from concert_framework.templator import render_template
from helper.decorators import Routing

routes = {}

@Routing(routes=routes, url='/home/')
class Home:
    """Основная странциа"""
    def __call__(self, request):
        return '200 OK', render_template('index.html')

@Routing(routes=routes, url='/about/')
class About:
    """Страница 'о нас' """
    def __call__(self, request):
        return '200 OK', render_template('about.html')

@Routing(routes=routes, url='/contact/')
class Contact:
    """Страница контактов """
    def __call__(self, request):
        return '200 OK', render_template('contact.html')

@Routing(routes=routes, url='/prices/')
class Prices:
    """Страница цен"""
    def __call__(self, request):
        return '200 OK', render_template('prices.html')

@Routing(routes=routes, url='/')
class Default_page:
    """Страница по-умолчанию"""
    def __call__(self, request):
        return '200 OK', render_template('index.html')
