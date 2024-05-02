from mongoengine import Document, StringField, ListField, IntField

class Student(Document):
    username = StringField()
    name = StringField()
    email = StringField()
    phone = StringField()
    university = StringField()
    program = StringField()
    current_year=StringField()  
    cgpa = IntField()
    current_location = StringField()
    preferred_location = StringField()
    skills = ListField(StringField())
    interested_in_job = StringField()
    gender = StringField()
    blood_group = StringField()
    backlog = StringField()
    backlog_count = IntField()
    job_reason_text = StringField()
    tenth_percentage = IntField()
    twelfth_percentage = IntField()

meta = {'collection': 'students'}
    
