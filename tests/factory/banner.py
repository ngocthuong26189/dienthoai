import factory
from factory.mongoengine import MongoEngineFactory
from models import banner
from tests.factory.slider import SliderFactory

class BannerFactory(MongoEngineFactory):

    class Meta:
        model = banner.Banner

    name = factory.Sequence(lambda n: 'banner_name-{0}'.format(n))
    image = factory.Sequence(lambda n: 'banner_image-{0}'.format(n))
    html = factory.Sequence(lambda n: 'banner_html-{0}'.format(n))