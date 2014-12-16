import factory
from factory.mongoengine import MongoEngineFactory
from models import slider


class SliderFactory(MongoEngineFactory):

    class Meta:
        model = slider.Slider

    name = factory.Sequence(lambda n: 'slider-name-{0}'.format(n))
    description = factory.Sequence(lambda n: 'slider_description-{0}'.format(n))

