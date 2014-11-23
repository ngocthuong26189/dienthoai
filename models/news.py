from mongoengine import *
from services.image import image_url, image_original_url
from datetime import datetime

class News(Document):
    image = StringField()
    video = StringField()
    title = StringField(required=True)
    content = StringField(required=True)
    brief = StringField(required=True)
    author = ReferenceField('User',required=True)
    show_in_index = BooleanField(default=False)
    news_category = ReferenceField('News_Category', reverse_delete_rule=NULLIFY)
    created_at = DateTimeField(required=True, default=datetime.utcnow)
    updated_at = DateTimeField(required=True, default=datetime.utcnow)

    @property
    def image_url(self):
        if self.image is None:
            return ""
        return image_url(self.image)

    @property
    def image_original_url(self):
        if self.image is None:
            return ""
        return image_original_url(self.image)
