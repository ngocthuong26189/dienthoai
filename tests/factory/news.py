import factory
from factory.mongoengine import MongoEngineFactory
from models import news
from tests.factory.news_category import NewsCategoryFactory
from tests.factory.user import UserFactory

class NewsBasicFactory(MongoEngineFactory):

    class Meta:
        model = news.News

    title = factory.Sequence(lambda n: 'news_title-{0}'.format(n))
    video = factory.Sequence(lambda n: 'news_video-{0}'.format(n))
    content = factory.Sequence(lambda n: 'news_content-{0}'.format(n))
    brief = factory.Sequence(lambda n: 'news_brief-{0}'.format(n))
    image = factory.Sequence(lambda n: 'news_img-{0}.png'.format(n))

class NewsFactory(NewsBasicFactory , NewsCategoryFactory, UserFactory):
    news_category = factory.SubFactory(NewsCategoryFactory)
    author = factory.SubFactory(UserFactory)