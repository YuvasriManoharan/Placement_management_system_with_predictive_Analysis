import json
from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
from models import User, Student,Tpo, TrainingEvent,placementEvent
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import tensorflow as tf
from pymongo import MongoClient
from bson import ObjectId
from datetime import date, datetime,timedelta
from flask import Blueprint
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from flask_mail import Mail, Message
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier






app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/stud')
db = client['stud']  # Replace 'your_database_name' with your actual database name
collection = db['students']  # Assuming you have a collection named 'students'
mongo=db['users']
tpo=db['tpos']
trainingEvent=db['trainingevents']
placement_Event=db['placementevents']



# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Define User model
class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({'_id': user_id})
    if user_data:
        user = User()
        user.id = user_data['_id']
        return user
    return None

# Load TensorFlow model
model = tf.keras.models.load_model('my_model_campus_placement.h5')

# Define routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/tsignin', methods=['POST'])
def tsignin():
    try:
        # Assuming Tpo is your model class for TPO users
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the database for the user
        found_user = tpo.find_one({'username': username})
     
        if not found_user:
            # User not found
            return "User not found"

        # Compare passwords (assuming plain text)
        if found_user['password']== password:
            # If password is correct, redirect to TPO dashboard
            return render_template("tpo_dashboard.html")
        else:
            # Incorrect password
            return "Incorrect password"

    except Exception as e:
        # Log the error for debugging
        print("Error in signin:", e)
        # Send an error response
        return "Internal Server Error", 500

@app.route('/signin', methods=['POST'])
def signin():
    try:
        # Get the username and password from the request form data
        username = request.form['username']
        password = request.form['password']

        print("Username:", username)  # Debugging statement

        # Find the user in the database by username
        user_data = mongo.find_one({'username': username})

        print("User data:", user_data)  # Debugging statement

        if not user_data:
            # User not found
            return "User not found"

        # Compare passwords
        if user_data['password'] == password:
            # Passwords match
             student_data = collection.find_one({'username': username})
             if student_data:
                 student_id = str(student_data.get('_id'))
                 print("student Dashboard",student_id)  # Convert ObjectId to string
                 return render_template('student_dashboard.html', student=student_data, student_id=student_id)
             else:
                # If not found in Student database, render register_student page
                return render_template("register_student.html", student=user_data)
        else:
            # Incorrect password
            return "Incorrect password"

    except Exception as e:
        # Log the error for debugging
        print("Error in signin:", e)
        # Send an error response
        return "Internal Server Error", 500

@app.route('/tpo_login', methods=['GET', 'POST'])
def tpo_login():
    if request.method == 'POST':
        # TPO login logic
        pass
    return render_template('tpo_login.html')

# Create SMTP connection
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "avcceplacementcell@gmail.com"
smtp_password = "tlfn egkv bput suay"

# Function to send email notification to students
def send_email_notification(recipients, subject, message):
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, recipients, msg.as_string())
# Route to get previous training events
@app.route('/student_previous')
def student_previous():
    try:
        # Find events whose date is before the current date
        current_date = datetime.now()
        print("Current Date:", current_date)
        
        # Convert string date from document to datetime object
        previous_training_events = list(trainingEvent.find({'date': {'$lt': current_date.strftime("%Y-%m-%d")}}))
        print("Previous Events:", previous_training_events)# Debugging statement
        
        return render_template('student_training.html', trainingEvents=previous_training_events, showFeedback=True)
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500
    
# Route to get student upcoming training events
@app.route('/student_upcoming')
def student_upcoming():
    try:
        # Find events whose date is before the current date
        current_date = datetime.now()
        print("Current Date:", current_date)
        
        # Convert string date from document to datetime object
        previous_training_events = list(trainingEvent.find({'date': {'$gte': current_date.strftime("%Y-%m-%d")}}))
        print("Previous Events:", previous_training_events)# Debugging statement
        
        return render_template('student_upcoming_training.html', trainingEvents=previous_training_events, showFeedback=True)
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# Route to get previous training events
@app.route('/previous')
def previous():
    try:
        # Find events whose date is before the current date
        current_date = datetime.now()
        print("Current Date:", current_date)
        
        # Convert string date from document to datetime object
        previous_training_events = list(trainingEvent.find({'date': {'$lt': current_date.strftime("%Y-%m-%d")}}))
        print("Previous Events:", previous_training_events)# Debugging statement
        
        return render_template('training.html', trainingEvents=previous_training_events, showFeedback=True)
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500
# Route to get upcoming training events
@app.route('/upcoming')
def upcoming():
    try:
        # Find events whose date is before the current date
        current_date = datetime.now()
        print("Current Date:", current_date)
        
        # Convert string date from document to datetime object
        previous_training_events = list(trainingEvent.find({'date': {'$gte': current_date.strftime("%Y-%m-%d")}}))
        print("Previous Events:", previous_training_events)# Debugging statement
        
        return render_template('upcomingTraining.html', trainingEvents=previous_training_events, showFeedback=True)
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500
# Route to display form to add a new training event
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,  
    MAIL_USE_TLS=True,
    MAIL_USERNAME='avcceplacementcell@gmail.com',
    MAIL_PASSWORD='tlfn egkv bput suay'
)
mail = Mail(app)

@app.route('/add_training_event', methods=['GET'])
def add_training_event():
    return render_template('addTraining.html')
def notify_students(training_event):
    try:
        # Get email addresses of students belonging to the mentioned departments and current year
        students = collection.find({
            'program': {'$in': training_event['departments']},
            'current_year': {'$in': training_event['currentYears']}
        })
        print(students)

        student_emails = [student['email'] for student in students]

        # Craft the email message
        subject = f'New Training Event: {training_event["programName"]}'
        message_body = f'A new training event on {training_event["programName"]} has been scheduled for {training_event["date"]} by {training_event["resourcePerson"]}.'

        # Send email notification to students
        send_email(subject, message_body, student_emails)
        print("Email sent successfully to:", student_emails)  # Add a print statement for debugging
    except Exception as e:
        print("Error notifying students:", e)

@app.route('/add_training_event2', methods=['POST'])
def add_training_event2():
    try:
        # Extract data from the form submission
        program_name = request.form['programName']
        resource_person = request.form['resourcePerson']
        date = request.form['date']
        description = request.form['description']
        departments = request.form.getlist('departments')
        current_years = request.form.getlist('currentYear')  # Use getlist() to retrieve multiple values

        # Save the new training event to the database
        training_event = {
            'programName': program_name,
            'resourcePerson': resource_person,
            'date': date,
            'description': description,
            'departments': departments,
            'currentYears': current_years  # Use a list for multiple current years
        }

        # Insert the training event data into the 'trainingEvents' collection
        trainingEvent.insert_one(training_event)
        notify_students(training_event)

        # Redirect to the TPO dashboard or any other desired page
        return render_template("tpo_dashboard.html")
    except Exception as e:
        # Handle any errors that may occur
        print("Error:", e)
        return "An error occurred while adding the training event", 500




def send_email(subject, body, recipients):
    try:
        msg = Message(subject, sender='your-email@example.com', recipients=recipients)
        msg.body = body
        mail.send(msg)
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", e)

# Route to handle feedback submission for a training event
@app.route('/feedback/<event_id>', methods=['POST'])
def submit_feedback(event_id):
    try:
        feedback = request.form['feedback']

        # Find the training event by its ID
        training_event = TrainingEvent.objects(id=event_id).first()

        # Append the new feedback to the existing feedback array or initialize it if it doesn't exist
        if training_event.feedback:
            training_event.feedback.append(feedback)
        else:
            training_event.feedback = [feedback]

        # Save the updated training event
        training_event.save()

        return redirect(url_for('training.previous_training_events'))
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500


@app.route('/student_login1', methods=['GET', 'POST'])
def student_login1():
    if request.method == 'POST':
        # Student login logic
        pass
    return render_template('student_login1.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Sign up logic
        pass
    return render_template('signup.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Registration logic
        pass
    return render_template('student_dashboard.html')

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    try:
        username = session.get('username')
        student_data = collection.find_one({'username': username})
        if student_data:
            student_id = str(student_data.get('_id'))
            print("student Dashboard",student_id)  # Convert ObjectId to string
            return render_template('student_dashboard.html', student=student_data, student_id=student_id)
        else:
            flash('Student data not found', 'error')
            return redirect(url_for('home'))
    except Exception as e:
        print("Error in student_dashboard route:", e)
        flash('An error occurred while retrieving student data', 'error')
        return redirect(url_for('home'))


# Route to render the registration form
@app.route("/edit_profile/<id>", methods=['GET'])
def edit_profile(id):
    try:
       # Retrieve the student document by its ObjectId
        student_id = ObjectId(id)
        # Retrieve the student document by its ObjectId
        student = collection.find_one({'_id': student_id})
        if student:
            return render_template("edit_profile.html", student=student)
        else:
            return "Student not found", 404  # Return a 404 Not Found error if student is not found
    except Exception as e:
        print("Error rendering edit profile:", e)
        return "Error rendering edit profile", 500


# Route to handle submission of registration form
@app.route("/update_profile", methods=['POST'])
def update_profile():
    try:
        username = request.form['username']
        student_data = collection.find_one({'username': username})
        if student_data:
            student_id = str(student_data.get('_id'))
        
        # Find the student by username
        stud = collection.find_one({'_id': ObjectId(student_id)})
        print(stud)
        
        if stud:
            # Update student's profile fields
            stud['name'] = request.form['name']
            stud['email'] = request.form['email']
            stud['phone'] = request.form['phone']
            stud['university'] = request.form['university']
            stud['program'] = request.form['program']
            stud['current_year'] = request.form['current_year']
            stud['cgpa'] = request.form['cgpa']
            stud['current_location'] = request.form['current_location']
            stud['preferred_location'] = request.form['preferred_location']
            stud['skills'] = request.form['skills']
            stud['interested_in_job'] = request.form['interested_in_job']
            stud['tenth_percentage']= request.form['tenth_percentage']  # New field for 10th percentage
            stud['twelfth_percentage']= request.form['twelfth_percentage']
            
            # Save the updated student document
            result = collection.update_one({'_id': ObjectId(student_id)}, {"$set": stud})
         

            print("result",result)
            
           
            
            # Redirect back to the profile page or any other page
            return render_template("student_dashboard.html",student=stud,student_id=student_id)
        else:
            flash('Student not found', 'error')
            return redirect(url_for('home'))
    except Exception as e:
        print("Error updating profile:", e)
        flash('Error updating profile', 'error')
        return redirect(url_for('home'))
    
@app.route('/register_student', methods=['POST'])
def register_student():
    try:
        # Retrieve data from the form including 10th and 12th percentage
        student_data = {
            'username': request.form['username'],
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'university': request.form['university'],
            'program': request.form['program'],
            'current_year': request.form['year'],
            'cgpa': request.form['cgpa'],
            'current_location': request.form['current_location'],
            'preferred_location': request.form['preferred_location'],
            'skills': request.form['skills'].split(','),  # Split the string into a list of skills
            'interested_in_job': request.form['interested_in_job'],
            'gender': request.form['gender'],
            'blood_group': request.form['blood_group'],
            'backlog': request.form['backlog'],
            'backlog_count': request.form.get('backlog_count', ''),  # Optional field
            'job_reason_text': request.form.get('job_reason_text', ''),  # Optional field
            'tenth_percentage': request.form['tenth_percentage'],  # New field for 10th percentage
            'twelfth_percentage': request.form['twelfth_percentage'] # New field for 12th percentage
            # Add other fields similarly
        }

        # Insert the student data into the collection
        result = collection.insert_one(student_data)

        # Get the inserted student document
        inserted_student = collection.find_one({'_id': result.inserted_id})
        username = request.form['username']
        student_data = collection.find_one({'username': username})
        if student_data:
            student_id = str(student_data.get('_id'))

        # Return the student dashboard template with the inserted student data
        return render_template("student_dashboard.html", student=inserted_student,student_id=student_id)
    except Exception as e:
        print("Error registering student:", e)
        return "Error registering student", 500

@app.route('/placement_add_event', methods=['GET'])
def placement_add_event():
    return render_template('addPlacement.html')

def pnotify_students(placement_event):
    try:
        print(placement_event['eligibleDepartments'])
        print(placement_event['minTenthPercentage'])
        print( placement_event['minTwelfthPercentage'])
        print(placement_event['minCGPA'])
        print(placement_event['maxBacklogCount'])
        
        # Get email addresses of students belonging to the mentioned departments and current year
        students = list(collection.find({
            'program': {'$in': placement_event['eligibleDepartments']},
            
            
        }))
        print("students",students)

        student_emails = [student['email'] for student in students]

        # Craft the email message
        subject = f'New Campus Drive: {placement_event["companyName"]}'
        message_body = f'A new campus Drive on {placement_event["companyName"]} has been scheduled for {placement_event["dateOfProgram"]} .'

        # Send email notification to students
        send_email_notification(subject, message_body, student_emails)
        print("Email sent successfully to:", student_emails)  # Add a print statement for debugging
    except Exception as e:
        print("Error notifying students:", e)


@app.route('/add_placement', methods=['POST'])
def add_placement():
    try:
        # Extract data from the form
        company_name = request.form.get('companyName', '')
        industry_type = request.form.get('industryType', '')
        role = request.form.get('role', '')
        eligible_departments = request.form.getlist('eligibleDepartments')
        date_of_program = request.form.get('dateOfProgram', '')
        contact_number = request.form.get('contactNumber', '')
        address = request.form.get('address', '')
        interview_round_details = request.form.get('interviewRoundDetails', '')
        min_tenth_percentage = int(request.form.get('minTenthPercentage', 0))
        min_twelfth_percentage =int(request.form.get('minTwelfthPercentage', 0))
        min_cgpa = int(request.form.get('minCGPA', 0))
        max_backlog_count = int(request.form.get('maxBacklogCount', 0))

        # Construct the placement event dictionary
        placement_event = {
            'companyName': company_name,
            'industryType': industry_type,
            'role': role,
            'eligibleDepartments': eligible_departments,
            'dateOfProgram': date_of_program,
            'contactNumber': contact_number,
            'address': address,
            'interviewRoundDetails': interview_round_details,
            'minTenthPercentage': min_tenth_percentage,
            'minTwelfthPercentage': min_twelfth_percentage,
            'minCGPA': min_cgpa,
            'maxBacklogCount': max_backlog_count
        }
        print(placement_Event)
        # Save the placement event to the database
        placement_Event.insert_one(placement_event)
        pnotify_students(placement_event)

      

        return render_template("tpo_dashboard.html")
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500
def send_email_notification(subject, body, recipients):
    try:
        msg = Message(subject, sender='your-email@example.com', recipients=recipients)
        msg.body = body
        mail.send(msg)
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", e)

# Usage example:
# send_email_notification(['recipient1@example.com', 'recipient2@example.com'], 'Subject', 'Hello, this is a test email!')
# Route to add feedback for a placement event
@app.route('/feedback/<eventId>', methods=['POST'])
def add_feedback(eventId):
    try:
        feedback = request.form['feedback']
        placement_event = placementEvent.find.get(id=eventId)
        placement_event.feedback.append(feedback)
        placement_event.save()
        return redirect(url_for('placement.previous_placements'))
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500
@app.route('/student_previous_placements', methods=['GET'])
def student_previous_placements():
    try:
        current_date = datetime.now()
        previous_training_events = list(placement_Event.find({'dateOfProgram': {'$lt': current_date.strftime("%Y-%m-%d")}}))
        print("Previous Events:", previous_training_events)  # Debugging statement
        
        # Convert dateOfProgram from string to datetime
        for event in previous_training_events:
            event['dateOfProgram'] = datetime.strptime(event['dateOfProgram'], '%Y-%m-%d')
        
        return render_template('student_placement.html', placements=previous_training_events)
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# Route to display previous placement notifications
@app.route('/placement_previous', methods=['GET'])
def previous_placements():
    try:
        current_date = datetime.now()
        previous_training_events = list(placement_Event.find({'dateOfProgram': {'$lt': current_date.strftime("%Y-%m-%d")}}))
        print("Previous Events:", previous_training_events)  # Debugging statement
        
        # Convert dateOfProgram from string to datetime
        for event in previous_training_events:
            event['dateOfProgram'] = datetime.strptime(event['dateOfProgram'], '%Y-%m-%d')
        
        return render_template('placement.html', placements=previous_training_events)
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# Route to update placement details
from bson import ObjectId

@app.route('/update/<id>', methods=['POST'])
def update(id):
    try:
        students_attended = request.form['studentsAttended']
        students_selected = request.form['studentsSelected']
        interview_process = request.form['interviewProcess']

        placement_Event.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'studentsAttended': students_attended, 'studentsSelected': students_selected, 'interviewProcess': interview_process}}
        )

        return previous_placements()  # Call the previous_placements function to render the updated data
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

       
# Route to display upcoming placement notifications
@app.route('/student_placement_upcoming/<id>', methods=['GET'])
def student_placement_upcoming(id):
    try:
         student_id = ObjectId(id)
    # Retrieve the student document by its ObjectId
    
         current_date = datetime.now()
         upcoming_events = list(placement_Event.find({'dateOfProgram': {'$gte': current_date.strftime("%Y-%m-%d")}}))
         print(" upcoming_events:",  upcoming_events)  # Debugging statement
        
        # Convert dateOfProgram from string to datetime
         for event in  upcoming_events:
            event['dateOfProgram'] = datetime.strptime(event['dateOfProgram'], '%Y-%m-%d')
         placement_id = event['_id'] 
         return render_template('upcoming_student_Placement.html', placements= upcoming_events,student_id=student_id,placement_id=placement_id)
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

@app.route('/submit_availability/<id>/<ids>', methods=['POST'])
def submit_availability(id,ids):
    if request.method == 'POST':
        # Get the form data
        student_id = ObjectId(id)
        placement_id=ObjectId(ids)
        print("id",placement_id)
        student = collection.find_one({'_id': student_id})
        user = student['username']
    # Retrieve the student document by its ObjectId
        selection = request.form["availability"]
        print("selection",selection)
       
        if(selection=='yes'):
            # Assuming there's only one document with the given _id
            
            lis=list(placement_Event.find({'_id': ObjectId(placement_id)}))
            index = None
            for i, item in enumerate(lis):
                if 'no' in item:
                    index = i
                    break
            if lis:
                document = lis[index]
                no_list = document.get('no', [])  # Get the 'no' array from the document, default to empty list if not present
                print(no_list)

            if user in no_list:
                print("hai")
                placement_Event.update_one({'_id': placement_id}, {'$pull': {'no': user}})

           
               

            placement_Event.update_one({'_id': ObjectId(placement_id)}, {'$addToSet': {'yes': user}})
        else:
            lis=list(placement_Event.find({'_id': ObjectId(placement_id)}))
            index = None
            for i, item in enumerate(lis):
                if 'yes' in item:
                    index = i
                    break
            if lis:
                document = lis[index]
                no_list = document.get('yes', [])  # Get the 'no' array from the document, default to empty list if not present
                print(no_list)

            if user in no_list:
                print("hai")
                placement_Event.update_one({'_id': placement_id}, {'$pull': {'yes': user}})
            placement_Event.update_one({'_id': ObjectId(placement_id)}, {'$addToSet': {'no': user}})

       
       
        # Redirect back to the page or any other page
        return redirect(url_for('student_placement_upcoming',id=student_id))
    else:
        # Handle invalid request method
        return "Method not allowed", 405
from flask import render_template

@app.route("/see/<id>")
def see(id):
    placement_id = ObjectId(id)
    lis = list(placement_Event.find({'_id': ObjectId(placement_id)}))
    index = None
    students = []

    for i, item in enumerate(lis):
        if 'yes' in item:
            index = i
            break

    if index is not None:
        document = lis[index]
        yes_list = document.get('yes', [])
        
        for username in yes_list:
            student = collection.find_one({'username': username})
            if student:
                students.append(student)

    return render_template("yes.html", students=students)
@app.route("/seeno/<id>")
def seeno(id):
    placement_id = ObjectId(id)
    lis = list(placement_Event.find({'_id': ObjectId(placement_id)}))
    index = None
    students = []

    for i, item in enumerate(lis):
        if 'no' in item:
            index = i
            break

    if index is not None:
        document = lis[index]
        yes_list = document.get('no', [])
        
        for username in yes_list:
            student = collection.find_one({'username': username})
            if student:
                students.append(student)

    return render_template("no.html", students=students)


# Route to display upcoming placement notifications
@app.route('/placement_upcoming', methods=['GET'])
def placement_upcoming():
    try:
         current_date = datetime.now()
         upcoming_events = list(placement_Event.find({'dateOfProgram': {'$gte': current_date.strftime("%Y-%m-%d")}}))
         print(" upcoming_events:",  upcoming_events)  # Debugging statement
        
        # Convert dateOfProgram from string to datetime
         for event in  upcoming_events:
            event['dateOfProgram'] = datetime.strptime(event['dateOfProgram'], '%Y-%m-%d')
        
         return render_template('upcomingPlacement.html', placements= upcoming_events)
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/prediction', methods=['GET', 'POST'])
@login_required
def prediction():
    if request.method == 'POST':
        # Prediction logic
        pass
    return render_template('prediction.html')

data = pd.read_excel('PlacementDataset.xlsx')
data = data.rename(columns={' Placed': 'placed'})
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33,random_state=100)
regr = RandomForestRegressor(max_depth=4, random_state=0)
regr.fit(X_train, y_train)
score_rf = regr.score(X_test,y_test)
dt_classifier = DecisionTreeClassifier()
dt_classifier.fit(X_train, y_train)
dt_score = dt_classifier.score(X_test, y_test)
print("Decision Tree Classifier score = {}%".format(dt_score * 100))

# Logistic Regression
logistic_regression = LogisticRegression()
logistic_regression.fit(X_train, y_train)
logistic_score = logistic_regression.score(X_test, y_test)
print("Logistic Regression score = {}%".format(logistic_score * 100))

# K-Neighbor Classifier
knn_classifier = KNeighborsClassifier()
knn_classifier.fit(X_train, y_train)
knn_score = knn_classifier.score(X_test, y_test)
print("K-Neighbor Classifier score = {}%".format(knn_score * 100))

# Gradient Boosting Classifier
gb_classifier = GradientBoostingClassifier()
gb_classifier.fit(X_train, y_train)
gb_score = gb_classifier.score(X_test, y_test)
print("Gradient Boosting Classifier score = {}%".format(gb_score * 100))
print("random forest score = {}%".format(score_rf*100))
from pymongo import MongoClient
mongo_db = db['placement_db'] 

def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
        # Assuming you've established a connection to MongoDB
        # Assuming the collection name is 'student'

        # Retrieve user information from MongoDB
        user_data = collection.find_one({'uname': user})
        
        if user_data:
            user = user_data['fname']  # Assuming 'fname' holds the user's full name in MongoDB
        else:
            user = None  # User not found in MongoDB
        
    return user


def get_date():
    dt = None
    today = date.today()
    dt = today.strftime("%d/%m/%y")
    return dt
@app.route("/c_quiz/<id>", methods=['GET', 'POST'])
def c_quiz(id):
    student_id = ObjectId(id)
    # Retrieve the student document by its ObjectId
    student = collection.find_one({'_id': student_id})
    user = student['username']
    dt = get_date()
    
    if request.method == 'POST':
        ans1 = request.form['question1']
        ans2 = request.form['question2']
        ans3 = request.form['question3']
        ans4 = request.form['question4']
        ans5 = request.form['question5']
        ans6 = request.form['question6']
        ans7 = request.form['question7']
        ans8 = request.form['question8']
        ans9 = request.form['question9']
        ans10 = request.form['question10']
        
        count = 0
        if ans1 == "ans1":
            count += 1
        if ans2 == "ans2":
            count += 1
        if ans3 == "ans3":
            count += 1
        if ans4 == "ans4":
            count += 1
        if ans5 == "ans5":
            count += 1
        if ans6 == "ans6":
            count += 1
        if ans7 == "ans7":
            count += 1
        if ans8 == "ans8":
            count += 1
        if ans9 == "ans9":
            count += 1
        if ans10 == "ans10":
            count += 1
        
        percentage = (count / 10) * 100
        
        try:
            # Check if user data exists in the collection
            user_data = mongo_db['student_results'].find_one({'uname': user})
            if user_data:
                # Update existing document
                result = mongo_db['student_results'].update_one({'uname': user}, {'$set': {'c': percentage}})
            else:
                # Insert new document
                quiz_data = {
                    'date': dt,
                    'uname': user,
                    'c': percentage,
                    'python': None,  # You'll fill in these values later in 'python' and 'java' routes
                    'java': None,
                    'avg': None
                }
                mongo_db['student_results'].insert_one(quiz_data)
                flash('Quiz data recorded successfully')
            
            return redirect(url_for('python', id=student_id))
        except Exception as e:
            flash('Failed to record quiz data: {}'.format(str(e)), 'error')
            return render_template("student_dashboard.html", student_id=student_id)
            
    return render_template('c_quiz.html', student_id=student_id)


@app.route('/python/<id>', methods=['POST', 'GET'])
def python(id):
    student_id = ObjectId(id)
    # Retrieve the student document by its ObjectId
    student1 = collection.find_one({'_id': student_id})
    user = student1['username']
    dt = get_date()


    if request.method == 'POST':
        ans1 = request.form['question1']
        ans2 = request.form['question2']
        ans3 = request.form['question3']
        ans4 = request.form['question4']
        ans5 = request.form['question5']
        ans6 = request.form['question6']
        ans7 = request.form['question7']
        ans8 = request.form['question8']
        ans9 = request.form['question9']
        ans10 = request.form['question10']
        count = 0

        if ans1 == "ans1":
            count += 1
        if ans2 == "ans2":
            count += 1
        if ans3 == "ans3":
            count += 1
        if ans4 == "ans4":
            count += 1
        if ans5 == "ans5":
            count += 1
        if ans6 == "ans6":
            count += 1
        if ans7 == "ans7":
            count += 1
        if ans8 == "ans8":
            count += 1
        if ans9 == "ans9":
            count += 1
        if ans10 == "ans10":
            count += 1

        percentage = (count / 10) * 100
        output = int(percentage)

        try:
            # Check if user data exists in the collection
            user_data = mongo_db['student_results'].find_one({'uname': user})
            if user_data:
                # Update existing document
                result = mongo_db['student_results'].update_one({'uname': user}, {'$set': {'python': output}})
            else:
                # Insert new document
                quiz_data = {
                    'date': dt,
                    'uname': user,
                    'c': None,
                    'python': output,  # You'll fill in these values later in 'python' and 'java' routes
                    'java': None,
                    'avg': None
                }
                mongo_db['student_results'].insert_one(quiz_data)
                flash('Quiz data recorded successfully')

            return redirect(url_for('java', id=student_id))
        except Exception as e:
            flash('Failed to record quiz data: {}'.format(str(e)), 'error')
            return render_template("student_dashboard.html", student=student_id)

    return render_template('python.html')
@app.route('/java/<id>', methods=['POST', 'GET'])
def java(id):
    student_id = ObjectId(id)
    # Retrieve the student document by its ObjectId
    student1 = collection.find_one({'_id': student_id})
    user = student1['username']
    dt = get_date()

    if request.method == 'POST':
        ans1 = request.form['question1']
        ans2 = request.form['question2']
        ans3 = request.form['question3']
        ans4 = request.form['question4']
        ans5 = request.form['question5']
        ans6 = request.form['question6']
        ans7 = request.form['question7']
        ans8 = request.form['question8']
        ans9 = request.form['question9']
        ans10 = request.form['question10']
        
        count = 0
        if ans1 == "ans1":
            count += 1
        if ans2 == "ans2":
            count += 1
        if ans3 == "ans3":
            count += 1
        if ans4 == "ans4":
            count += 1
        if ans5 == "ans5":
            count += 1
        if ans6 == "ans6":
            count += 1
        if ans7 == "ans7":
            count += 1
        if ans8 == "ans8":
            count += 1
        if ans9 == "ans9":
            count += 1
        if ans10 == "ans10":
            count += 1
        
        percentage = (count / 10) * 100
        output = int(percentage)

        try:
            # Update Java score in the database
            mongo_db['student_results'].update_one({'uname': user, 'date': dt}, {'$set': {'java': output}})
            
            # Calculate average score
            quiz_data = mongo_db['student_results'].find_one({'uname': user, 'date': dt})
            c_score = quiz_data['c']
            pyt = quiz_data['python']
            jv = output
            avg = (c_score + pyt + jv) / 3
            
            # Update average score in the database
            mongo_db['student_results'].update_one({'uname': user, 'date': dt}, {'$set': {'avg': avg}})
            
            
            flash('Your scores have been recorded.')
            return redirect(url_for('scores', id=student_id))

        except Exception as e:
            flash('Failed to record scores: {}'.format(str(e)), 'error')
            return render_template("student_dashboard.html", student=student_id)

    return render_template('java.html')

@app.route('/student_dashboard2/<id>')
def student_dashboard2(id):
    try:
        student_id = ObjectId(id)
    # Retrieve the student document by its ObjectId
        student1 = collection.find_one({'_id': student_id})
        user = student1['username']
        student_data = collection.find_one({'username': user})
        if student_data:
            student_id = str(student_data.get('_id'))
            print("student Dashboard",student_id)  # Convert ObjectId to string
            return render_template('student_dashboard.html', student=student_data, student_id=student_id)
        else:
            flash('Student data not found', 'error')
            return redirect(url_for('home'))
    except Exception as e:
        print("Error in student_dashboard route:", e)
        flash('An error occurred while retrieving student data', 'error')
        return redirect(url_for('home'))
    
from bson.objectid import ObjectId

@app.route('/scores/<id>',methods=['GET'])
def scores(id):
    try:
        student_id = ObjectId(id)
    # Retrieve the student document by its ObjectId
        student1 = collection.find_one({'_id': student_id})
        user = student1['username']
        dt = get_date()
        
        # Retrieve user's quiz data from MongoDB
        user_data = mongo_db['student_results'].find_one({'uname': user})
        
        # Check if user data exists
        if user_data:
            # Extract necessary fields
            total = [(user_data['date'], user_data['uname'], user_data['c'], user_data['python'], user_data['java'], user_data['avg'])]
            return render_template('scores.html', total=total,student_id=student_id)
        else:
            flash('No scores found for the current user', 'warning')
            return render_template('scores.html', total=[])
    except Exception as e:
        flash('An error occurred while fetching scores: {}'.format(str(e)), 'error')
        return render_template('scores.html', total=[])
@app.route('/details/<id>', methods=['POST', 'GET'])
def details(id):
    student_id = ObjectId(id)
    # Retrieve the student document by its ObjectId
    student1 = collection.find_one({'_id': student_id})
    user = student1['username']
    dt = get_date()
        
        # Retrieve user's quiz data from MongoDB
    user_data = mongo_db['student_results'].find_one({'uname': user})
        
    try:
        if request.method == 'POST':
         coding = request.form['Coding']
         aptitude = request.form['aptitude']
         Technical = request.form['Technical']
         Communication = request.form['Communication']
         Core = request.form['Core']
         Puzzle = request.form['Puzzle']
         English = request.form['English']
         Management = request.form['Management']
         Presentation = request.form['Presentation']
         Academic = request.form['Academic']
         Projects = request.form['Projects']
         Internships = request.form['Internships']
         Training = request.form['Training']
         Backlog = request.form['Backlog']
        
        # Predict placement using the model
         res = regr.predict([[coding, aptitude, Technical, Communication, Core, Puzzle, English, Management, Presentation, Academic, Projects, Internships, Training, Backlog]])
         print('Prediction:', res)
         
        # Store the predicted place ment in the session
         session['user'] = res[0]
        
        # Redirect to the predict route
         return redirect(url_for('predict',res=res))
    except Exception as e:
        flash('An error occurred while fetching scores: {}'.format(str(e)), 'error')
        
    return render_template('details.html', user=user)

@app.route('/predict/<res>')
def predict(res):
    
    
    return render_template('predict.html',res=res)


if __name__ == '__main__':
    app.run(debug=True, port=8000) 
