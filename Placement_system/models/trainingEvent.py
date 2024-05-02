from mongoengine import Document, StringField, DateTimeField, ListField

class TrainingEvent(Document):
    programName = StringField(required=True)
    resourcePerson = StringField(required=True)
    date = StringField(required=True)
    description = StringField(required=True)
    departments = ListField(StringField())

# No need to explicitly call `mongoose.model()` as it's specific to Mongoose in Node.js
