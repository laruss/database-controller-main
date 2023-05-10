from mongoengine import Document, StringField


class User(Document):
    name = StringField()
    username = StringField(required=True, unique=True)