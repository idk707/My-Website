from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

app = Flask(__name__)

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')

@app.route('/')
def home():
    return render_template('contact.html')

@app.route('/send-message', methods=['POST'])
def send_message():

    #Spam Trap
    if request.form.get('company'):
        return 'Spam detected', 400
    
    name = request. form.get('firstName') + ' ' + request.form.get('lastName')
    email = request.form.get('email')
    phoneNumber = request.form.get('phoneNumber')
    message = request.form.get('message')
    body = f"""
New Website Contact Form Submission:

Name: {name}
Email: {email}
Phone Number: {phoneNumber}
Message:
{message}
    """
    msg = MIMEText(body)
    msg['Subject'] = 'New Contact Form Submission'
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return '<h1>Message sent successfully!</h1>', 200
    except Exception as e:
        print(e)
        return f"""<h1>Failed to send message</h1>: {e}"""
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)