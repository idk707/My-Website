from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os
import gspread
from google.oauth2.service_account import Credentials
import json
from dotenv import load_dotenv

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

app = Flask(__name__)
CORS(app)

def send_email(firstName, lastName, phoneNumber, email, message):
    sender_email = EMAIL_USER
    sender_password = EMAIL_PASS
    receiver_email = sender_email

    subject = "New Contact Form Submission"

    body = f"""
    New contact form submission:

    First Name: {firstName}
    Last Name: {lastName}
    Phone Number: {phoneNumber}
    Email: {email}

    Message: 
    {message}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)

def save_to_sheets(firstName, lastName, phoneNumber, email, message):
    scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        "../credentials.json",
        scopes=scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("Contact Form Responses").sheet1

    sheet.append_row([
        firstName,
        lastName,
        phoneNumber,
        email,
        message
    ])

@app.route("/contact", methods=["POST", "OPTIONS"])

def contact():
    if request.method== "OPTIONS":
        return jsonify({"status" : "ok"}), 200

    data = request.json

    firstName = data.get("firstName")
    lastName = data.get("lastName")
    phoneNumber = data.get("phoneNumber")
    email = data.get("email")
    message = data.get("message")

    if not firstName:
        return jsonify({
            "status" : "error",
            "message" : "Missing required fields."
        }), 400
    
    try:
        send_email(firstName, lastName, phoneNumber, email, message)
        save_to_sheets(firstName, lastName, phoneNumber, email, message)

        return jsonify({
            "status" : "success",
            "message" : f"Thank You {firstName}! We will contact you at {email}."
        }), 200
    except Exception as e:
        print("Error", e)
        return jsonify({
            "status": "error",
            "message": "Something went wrong. Please try again."
        }), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)