from mongoengine import *
import md5

class User(Document):
    uid = SequenceField()
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = EmailField(required=True)
    permission = IntField(required=True, default=1)
    sid = StringField()
# The user services


def create(user_dict):
    username = user_dict.get('username', 'default_username')
    password = md5.new(user_dict.get('password','nopass')).hexdigest()
    email = user_dict.get('email', 'email@domain.com')
    return User(username=username, password=password, email=email).save()

def get(username):
    return User.objects(username=username).first()

def generate_encrypt_password(password):
    if len(password) > 5:
        return md5.new(password).hexdigest()
    else:
        raise ValidationError('Password\'s length should >= 6')
