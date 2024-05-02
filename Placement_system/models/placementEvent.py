from mongoengine import Document, StringField, ListField, DateTimeField, IntField, FloatField

class PlacementEvent(Document):
    companyName = StringField()
    industryType = StringField()
    role = StringField()
    eligibleDepartments = ListField(StringField())
    dateOfProgram = StringField()
    contactNumber = StringField()
    address = StringField()
    interviewRoundDetails = StringField()
    minTenthPercentage = IntField()  # New field for minimum 10th percentage
    minTwelfthPercentage = IntField()  # New field for minimum 12th percentage
    minCGPA = IntField()  # New field for minimum CGPA
    maxBacklogCount = IntField()  # New field for maximum backlog count
    feedback = ListField(StringField())  # Feedback field updated to an array of strings
    studentsAttended = IntField()  # New field for the number of students attended
    studentsSelected = IntField()  # New field for the number of students selected
    interviewProcess = StringField()  # New field for details about the interview process
    yes = ListField(StringField())
    no = ListField(StringField())
