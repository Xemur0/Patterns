from concert_framework.templator import render_template
from helper.decorators import Routing, Debug
from pattern.creational_patterns import Engine, Logger

site = Engine()
routes = {}
logger = Logger('main')

#тестовая категория, внутри можно создать услуги
site.categories.append(site.create_category('ZVUK', 'test', 0))


@Routing(routes=routes, url='/home/')
class Home:
    """Основная странциа"""
    @Debug(name="Home")
    def __call__(self, request):
        return '200 OK', render_template('index.html')


@Routing(routes=routes, url='/about/')
class About:
    """Страница 'о нас' """

    @Debug(name="About")
    def __call__(self, request):
        return '200 OK', render_template('about.html')


@Routing(routes=routes, url='/contact/')
class Contact:
    """Страница контактов """

    @Debug(name="Contact")
    def __call__(self, request):
        return '200 OK', render_template('contact.html')


@Routing(routes=routes, url='/')
class Default_page:
    """Страница по-умолчанию"""

    @Debug(name="Home")
    def __call__(self, request):
        return '200 OK', render_template('index.html')


@Routing(routes=routes, url='/send_info/')
class SendInfo:
    """Форма обратной связи """

    @Debug(name="Send info")
    def __call__(self, request):
        return '200 OK', render_template('contact.html')


@Routing(routes=routes, url='/prices/')
class ServiceList:
    """Список услуг"""

    @Debug(name="Service List")
    def __call__(self, request):
        if request['request_params'] == {}:

            logger.log('Список услуг')
            return '200 OK', render_template('prices.html',
                                             objects_list=site.services)
        else:
            try:
                category = site.find_category_by_id(
                    int(request['request_params']['id']))
                return '200 OK', render_template('prices.html',
                                                 objects_list=category.services,
                                                 name=category.name,
                                                 id=category.id)
            except KeyError:
                return '200 OK', 'No courses have been added yet'


@Routing(routes=routes, url='/category_list/')
class CategoryList:
    """Список категорий"""

    @Debug(name="Category List")
    def __call__(self, request):
        logger.log('Список категорий')

        return '200 OK', render_template('category_list.html',
                                         objects_list=site.categories)


@Routing(routes=routes, url='/create_category/')
class CreateCategory:
    """Создать категорию"""

    @Debug(name="Create Category")
    def __call__(self, request):

        if request['method'] == 'POST':
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            description = data['description']
            description = site.decode_value(description)

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, description, category)

            site.categories.append(new_category)

            return '200 OK', render_template('index.html',
                                             objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render_template('create_category.html',
                                             categories=categories)


@Routing(routes=routes, url='/create_service/')
class CreateService:
    """Создание услуги"""
    category_id = -1

    @Debug(name="Create Service")
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            price = data['price']
            price = site.decode_value(price)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_service('active', name, category, price)
                site.services.append(course)

            return '200 OK', render_template('prices.html',
                                             objects_list=category.services,
                                             name=category.name,
                                             id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render_template('create_service.html',
                                                 name=category.name,
                                                 id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@Routing(routes=routes, url='/copy_service/')
class CopyService:
    """Скопировать услугу"""

    @Debug(name="Cope Service")
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.services.append(new_course)

            return '200 OK', render_template('prices.html',
                                             objects_list=site.services)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
