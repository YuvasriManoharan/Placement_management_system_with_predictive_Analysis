from flask import Blueprint, render_template, request, redirect, url_for
from models.placementEvent import PlacementEvent
from models.student import Student
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

placement_blueprint = Blueprint('placement', __name__)

# Create a SMTP server instance for sending emails
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.starttls()
smtp_server.login('avcceplacementcell@gmail.com', 'tlfn egkv bput suay')

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
            message = MIMEMultipart()
            message['From'] = 'avcceplacementcell@gmail.com'
            message['To'] = ', '.join(student_emails)
            message['Subject'] = 'New Placement Notification'
            message.attach(MIMEText(f"A new placement opportunity for {data['role']} at {data['companyName']} has been posted. Application deadline: {data['dateOfProgram']}.", 'plain'))
            
            smtp_server.send_message(message)

        return redirect(url_for('tpo_dashboard'))
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# Route to add feedback for a placement event
@placement_blueprint.route('/feedback/<eventId>', methods=['POST'])
def add_feedback(eventId):
    try:
        feedback = request.form['feedback']
        placement_event = PlacementEvent.objects.get(id=eventId)
        placement_event.feedback.append(feedback)
        placement_event.save()
        return redirect(url_for('placement.previous_placements'))
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# Route to display previous placement notifications
@placement_blueprint.route('/previous', methods=['GET'])
def previous_placements():
    try:
        previous_placements = PlacementEvent.objects(dateOfProgram__lt=datetime.datetime.now())
        upcoming_placements = PlacementEvent.objects(dateOfProgram__gte=datetime.datetime.now())
        return render_template('placement.html', placements={'previous': previous_placements, 'upcoming': upcoming_placements})
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# Route to update placement details
@placement_blueprint.route('/update/<id>', methods=['POST'])
def update_placement(id):
    try:
        students_attended = request.form['studentsAttended']
        students_selected = request.form['studentsSelected']
        interview_process = request.form['interviewProcess']

        placement_event = PlacementEvent.objects.get(id=id)
        placement_event.update(studentsAttended=students_attended, studentsSelected=students_selected, interviewProcess=interview_process)

        previous_placements = PlacementEvent.objects(dateOfProgram__lt=datetime.datetime.now())
        return render_template('placement.html', placements={'previous': previous_placements, 'upcoming': []})
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# Route to display upcoming placement notifications
@placement_blueprint.route('/upcoming', methods=['GET'])
def upcoming_placements():
    try:
        upcoming_placements = PlacementEvent.objects(dateOfProgram__gte=datetime.datetime.now())
        return render_template('placement.html', placements={'previous': [], 'upcoming': upcoming_placements})
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500
