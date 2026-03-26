import subprocess
import requests
import time
import configparser
import smtplib
from email.mime.text import MIMEText

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Gotify Configuration
GOTIFY_ENABLED = config['gotify']['enabled'].lower() == 'y'
GOTIFY_URL = config['gotify']['url']
GOTIFY_TOKEN = config['gotify']['token']

# Email Configuration
EMAIL_ENABLED = config['email']['enabled'].lower() == 'y'
SMTP_SERVER = config['email']['smtp_server']
SMTP_PORT = int(config['email']['smtp_port'])
SENDER_EMAIL = config['email']['sender_email']
SENDER_PASSWORD = config['email']['sender_password']
RECIPIENT_EMAIL = config['email']['recipient_email']

# ntfy Configuration
NTFY_ENABLED = config['ntfy']['enabled'].lower() == 'y'
NTFY_URL = config['ntfy']['url']
NTFY_TOPIC = config['ntfy']['topic']

last_failed_login = None

def check_failed_logins():
    global last_failed_login

    try:
        result = subprocess.run(['lastb', '-1'], capture_output=True, text=True)
        failed_login = result.stdout.strip()

        if failed_login and failed_login != last_failed_login:
            send_notification(failed_login)
            last_failed_login = failed_login

    except Exception as e:
        print(f"Error checking failed logins: {e}")

def send_notification(failed_login):
    if GOTIFY_ENABLED:
        send_gotify_notification(failed_login)
    if EMAIL_ENABLED:
        send_email_notification(failed_login)
    if NTFY_ENABLED:
        send_ntfy_notification(failed_login)

def send_gotify_notification(failed_login):
    data = {
        "title": "New Failed Login Attempt Detected",
        "message": failed_login,
        "priority": 10  # Set priority as needed (1-5)
    }
    headers = {
        "X-Gotify-Key": GOTIFY_TOKEN
    }

    try:
        response = requests.post(f"{GOTIFY_URL}/message", json=data, headers=headers)
        response.raise_for_status() 
    except Exception as e:
        print(f"Error sending Gotify notification: {e}")

def send_email_notification(failed_login):
    msg = MIMEText(failed_login)
    msg['Subject'] = 'New Failed Login Attempt Detected'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Error sending email notification: {e}")

def send_ntfy_notification(failed_login):
    data = {
        "title": "New Failed Login Attempt Detected",
        "message": failed_login,
        "priority": 8 
    }

    try:
        response = requests.post(f"{NTFY_URL}/{NTFY_TOPIC}", json=data)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.exceptions.ConnectionError):
            print(f"Error sending ntfy notification: Failed to connect to {NTFY_URL}. Check your network and ntfy URL configuration.")
        else:
            print(f"Error sending ntfy notification: {e}")

if __name__ == "__main__":
    while True:
        check_failed_logins()
        time.sleep(60)
