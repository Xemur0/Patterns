import copy
import quopri

from pattern.behavioral_patterns import Subject


class User:
    """Абстрактный пользователь"""
    pass


class Guest(User):
    """Класс Гостя"""
    pass


class Admin(User):
    """Класс Админа"""
    pass


class UserFactory:
    """Порождающий паттерн Абстрактная фабрика - фабрика пользователей"""
    types = {
        'guest': Guest,
        'admin': Admin
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class ServicePrototype:
    """Порождающий паттерн Прототип - услуга"""

    def clone(self):
        return copy.deepcopy(self)



class Service(ServicePrototype):

    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price
        self.category.services.append(self)


class ActiveService(Service):
    """Активная услуга"""
    pass


class ProgressService(Service):
    """Услуга в разработке"""
    pass


class ServiceFactory:
    """Порождающий паттерн Абстрактная фабрика - фабрика услуг"""
    types = {
        'active': ActiveService,
        'progress': ProgressService
    }

    @classmethod
    def create(cls, type_, name, category, price):
        return cls.types[type_](name, category, price)


class Category(Subject):
    """Категория"""
    auto_id = 0

    def __init__(self, name, description, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.description = description
        self.services = []
        self.observers = []
        super().__init__()


    def add_service_to_nt(self):
        self.notify()

    def service_count(self):
        result = len(self.services)
        if self.category:
            result += self.category.service_count()
        return result


class Engine:
    """Основной интерфейс проекта"""

    def __init__(self):
        self.guests = []
        self.admins = []
        self.services = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, description, category=None):
        return Category(name, description, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    def find_category_by_name(self, name):
        for category in self.categories:
            if category.name == name:
                return category
        return None

    @staticmethod
    def create_service(type_, name, category, price):
        return ServiceFactory.create(type_, name, category, price)

    def get_service(self, name):
        for item in self.services:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
