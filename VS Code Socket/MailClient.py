"""
Program Name: MailClient.py
Description: This program implements a simple SMTP email client that sends an email
             from a specified sender to a specified receiver. It demonstrates basic
             email handling and SMTP communication in Python.

Author: Ryan Ellis
Date: 3/27/2025

Course: COSC 370 - Computer Networks
Instructor: Dr. Enyue Lu

Usage:
    1. Update the `senderEmail`, `receiverEmail`, and `password` variables with the appropriate values.
    2. Run this program to send an email.
    3. The program will establish a connection to the SMTP server, authenticate the sender, and send the email.

Requirements:
    - Python 3.x
    - The `smtplib` and `email` libraries for SMTP communication and email creation.
    - An active email account with SMTP access.

Notes:
    - Ensure that the SMTP server and port are correctly configured in the `smtpServer` and `smtpPort` variables.
    - For Gmail, you may need to enable "Allow less secure apps" or use an app-specific password.
    - This program is for educational purposes and is not intended for production use.
"""

import smtplib  # Import the smtplib library for SMTP communication
from email.mime.text import MIMEText    # Import the MIMEText class for creating email text
from email.mime.multipart import MIMEMultipart  # Import the MIMEMultipart class for creating multipart emails

# Define email sender and receiver

senderEmail = "re79380@gulls.salisbury.edu" # Sender's email address
receiverEmail = "frenchiery817@gmail.com"   # Receiver's email address
password = "password"   # Sender's email password (use app-specific password if using Gmail)

# Create the email
subject = "Test Email"
body = "Hello, this is a test email sent from my SMTP Client."

message = MIMEMultipart()   # Create a multipart email message
message["From"] = senderEmail
message["To"] = receiverEmail
message["Subject"] = subject

#add body to email
message.attach(MIMEText(body, "plain"))

# Set up the SMTP Server

smtpServer = "smtp.gmail.com"
smtpPort = 587

# Create a connection to the SMTP server
try:
    #Establish a connection to the SMTP server
    server = smtplib.SMTP(smtpServer, smtpPort)
    #Start TLS encryption
    server.starttls()
    #Login to the email server
    server.login(senderEmail, password)
    #Set message as string
    text = message.as_string()
    #Send the email
    server.sendmail(senderEmail, receiverEmail, text)
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
finally:
    #Close the connection to the SMTP server
    server.quit()
