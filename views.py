from concert_framework.templator import render_template
from helper.decorators import Routing, Debug
from pattern.behavioral_patterns import BaseSerializer, ListView, \
    CreateView, SmsNotifier, EmailNotifier
from pattern.creational_patterns import Engine, Logger

site = Engine()
routes = {}
logger = Logger('main')
sms_notifier = SmsNotifier()
email_notifier = EmailNotifier()

# тестовая категория, внутри можно создать услуги
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

                service = site.create_service('active', name, category, price)
                category.observers.append(sms_notifier)
                category.observers.append(email_notifier)
                site.services.append(service)
                category.add_service_to_nt()

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

    @Debug(name="Copy Service")
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_service = site.get_service(name)
            if old_service:
                new_name = f'copy_{name}'
                new_service = old_service.clone()
                new_service.name = new_name
                site.services.append(new_service)

            return '200 OK', render_template('prices.html',
                                             objects_list=site.services)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@Routing(routes=routes, url='/category_list/')
class CategoryListView(ListView):
    queryset = site.categories
    template_name = 'category_list.html'


@Routing(routes=routes, url='/create_category/')
class CreateCategory(CreateView):
    template_name = 'create_category.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['category_list'] = site.categories
        context['service_list'] = site.services

        return context

    def create_obj(self, data):
        category_name = data['name']
        category_name = site.decode_value(category_name)

        description = data['description']
        description = site.decode_value(description)

        category = None

        if category_name:
            category = site.find_category_by_name(category_name)

        if category == None or category not in site.categories:
            new_category = site.create_category(category_name, description)
            site.categories.append(new_category)


@Routing(routes=routes, url='/api/')
class SoundApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.categories).save()


@Routing(routes=routes, url='/delete_service/')
class DeleteService:
    @Debug(name="Delete Service")
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            service_to_delete = site.get_service(name)
            site.services.remove(service_to_delete)

            return '200 OK', render_template('prices.html',
                                             objects_list=site.services)
        except KeyError:
            return '200 OK', 'No to delete'
