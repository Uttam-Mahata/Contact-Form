# routes.py
from flask import Blueprint, jsonify, request

from email_validator import validate_email, EmailNotValidError
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
from flask import render_template, make_response

from models import Contact
from extensions import db
from flask import current_app

api_bp = Blueprint('api', __name__)
CORS(api_bp)


@api_bp.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Flask backend is working"})


@api_bp.route('/contact', methods=['POST'])
def handle_contact():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    if not all([name, email, subject, message]):
        return jsonify({'error': 'All fields are required'}), 400

    try:
        # Validate email format
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        return jsonify({'error': 'Invalid email format'}), 400

    try:
        # Store data to database
        new_contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(new_contact)
        db.session.commit()

        # Send email using the method below
        send_contact_email(name, email, subject, message)
        return jsonify({'message': 'Message received successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error processing contact message: {str(e)}'}), 500


def send_contact_email(name, email, subject, message):
    msg = EmailMessage()
    msg['Subject'] = f'New Contact Form Submission: {subject}'
    msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']  # Access via current_app
    msg['To'] = current_app.config['MAIL_DEFAULT_SENDER']  # Access via current_app
    html = render_template('contact_email.html', name=name, email=email, subject=subject, message=message)
    msg.add_alternative(html, subtype='html')

    try:
        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as smtp:
            smtp.starttls()
            smtp.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            smtp.send_message(msg)
    except Exception as e:
        print(f'Error sending email: {str(e)}')


@api_bp.route('/contact-email', methods=['GET'])
def render_contact_email_template():
    # Generate sample data
    name = "John Doe"
    email = "john.doe@example.com"
    subject = "Sample Subject"
    message = "This is a sample message."

    # Render the HTML content from the template
    html_content = render_template('contact_email.html', name=name, email=email, subject=subject, message=message)

    response = make_response(html_content)
    # Set the Content-Type header to text/html
    response.headers['Content-Type'] = 'text/html'
    return response