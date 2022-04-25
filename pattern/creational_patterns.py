import copy
import quopri
import sqlite3

from pattern.behavioral_patterns import Subject
from pattern.mappers import DbCommitException, DbUpdateException, \
    DbDeleteException, RecordNotFoundException

from pattern.unit_of_work import DomainObject

connection = sqlite3.connect('patterns.sqlite')

class User:
    def __init__(self, name):
        self.name = name


class Guest(User):
    def __init__(self, name):
        self.services = []
        super().__init__(name)


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



class Service(ServicePrototype, Subject):

    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price
        self.guests = []
        self.category.services.append(self)
        super().__init__()

    def __getitem__(self, item):
        return self.guests[item]

    def add_guest(self, guest: Guest):
        self.guests.append(guest)
        guest.services.append(self)
        self.notify()


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


class Category(Subject, DomainObject):
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


class CategoryMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'category'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, description, category = item
            category = Category(name, description, category)
            category.id = id
            result.append(category)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, description) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.name, obj.description))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)




class MapperRegistry:
    mappers = {
        'category': CategoryMapper,
    }

    @staticmethod
    def get_mapper(obj):
        print(f"{obj.__class__}")
        if isinstance(obj, Category):
            return CategoryMapper(connection)

        #if isinstance(obj, Category):
            #return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)

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
