import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from models import TrainingEvent, Student
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

training_blueprint = Blueprint('training', __name__)

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
@training_blueprint.route('/previous')
def previous_training_events():
    try:
        previous_training_events = TrainingEvent.objects(date__lt=datetime.now())
        return render_template('training.html', trainingEvents=previous_training_events, showFeedback=True)
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# Route to get upcoming training events
@training_blueprint.route('/upcoming')
def upcoming_training_events():
    try:
        upcoming_training_events = TrainingEvent.objects(date__gte=datetime.now())
        return render_template('training.html', trainingEvents=upcoming_training_events, showFeedback=False)
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# Route to display form to add a new training event
@training_blueprint.route('/add', methods=['GET', 'POST'])
def add_training_event():
    if request.method == 'GET':
        return render_template('addTraining.html')
    elif request.method == 'POST':
        try:
            program_name = request.form['programName']
            resource_person = request.form['resourcePerson']
            date = request.form['date']
            description = request.form['description']
            departments = request.form.getlist('departments')

            new_training_event = TrainingEvent(programName=program_name, resourcePerson=resource_person, date=date, description=description, departments=departments)
            new_training_event.save()

            # Get email addresses of students belonging to the mentioned departments
            students = Student.objects(program__in=departments)
            student_emails = [student.email for student in students]

            # Send email notification to students
            subject = 'New Training Event Notification'
            message = f'A new training event on {program_name} has been scheduled for {date} by {resource_person}.'
            send_email_notification(student_emails, subject, message)

            return redirect(url_for('tpo.tpo_dashboard'))
        except Exception as e:
            print(e)
            return 'Internal Server Error', 500

# Route to handle feedback submission for a training event
@training_blueprint.route('/feedback/<event_id>', methods=['POST'])
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
