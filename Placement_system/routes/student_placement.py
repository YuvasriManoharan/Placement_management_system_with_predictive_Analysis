import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from models import PlacementEvent, Student
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

placement_blueprint = Blueprint('placement', __name__)

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

# Route to display form to add a new placement event
@placement_blueprint.route('/add', methods=['GET'])
def add_placement_form():
    return render_template('addPlacement.html')

# Route to add a new placement notification
@placement_blueprint.route('/add', methods=['POST'])
def add_placement():
    try:
        data = request.form
        new_placement_event = PlacementEvent(**data)
        new_placement_event.save()

        # Send email notification to students
        students = Student.objects(program__in=data['eligibleDepartments'])
        student_emails = [student.email for student in students]

        if student_emails:
            subject = 'New Placement Notification'
            message = f'A new placement opportunity for {data["role"]} at {data["companyName"]} has been posted. Application deadline: {data["dateOfProgram"]}.'
            send_email_notification(student_emails, subject, message)
        else:
            print('No student emails found for eligible departments')

        return redirect(url_for('tpo.tpo_dashboard'))
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# Route to handle feedback submission for a placement event
@placement_blueprint.route('/feedback/<event_id>', methods=['POST'])
def submit_feedback(event_id):
    try:
        feedback = request.form['feedback']
        placement_event = PlacementEvent.objects(id=event_id).first()

        if placement_event:
            if placement_event.feedback:
                placement_event.feedback.append(feedback)
            else:
                placement_event.feedback = [feedback]
            placement_event.save()
        else:
            print('Placement event not found')

        return redirect(url_for('placement.previous_placements'))
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# Route to display previous placement notifications
@placement_blueprint.route('/previous')
def previous_placements():
    try:
        previous_placements = PlacementEvent.objects(dateOfProgram__lt=datetime.now())
        return render_template('placement.html', placements={'previous': previous_placements, 'upcoming': []})
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# Route to display upcoming placement notifications
@placement_blueprint.route('/upcoming')
def upcoming_placements():
    try:
        upcoming_placements = PlacementEvent.objects(dateOfProgram__gte=datetime.now())
        return render_template('placement.html', placements={'previous': [], 'upcoming': upcoming_placements})
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

