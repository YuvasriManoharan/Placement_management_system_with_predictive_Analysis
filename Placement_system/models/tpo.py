from mongoengine import Document, StringField
from mongoengine import EmailField

class Tpo(Document):
    username = StringField()
    password = StringField()

# No need to explicitly call `passportLocalMongoose` as it's specific to Mongoose in Node.js

