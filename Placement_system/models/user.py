from mongoengine import Document, StringField
from flask_login import UserMixin

class User(Document, UserMixin):
    username = StringField(required=True)
    password = StringField(required=True)

    meta = {'collection': 'users'}  # Optional: specify the collection name

# No need to explicitly call `mongoose.model()` as it's specific to Mongoose in Node.js
