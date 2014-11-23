import factory
from factory.mongoengine import MongoEngineFactory
from models import user

class UserFactory(MongoEngineFactory):

    class Meta:
        model = user.User

    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    password = "khongbiet"
    email = factory.LazyAttribute(lambda u: '{0}@domain.com'.format(u.username))
