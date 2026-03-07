import smtplib
from email.message import EmailMessage
import cv2

SENDER_EMAIL = "abeluke2004@gmail.com"
APP_PASSWORD = "debw lnoj fjvd elqg"
RECEIVER_EMAIL = "allenshajivarghese500@gmail.com"


def send_email_alert(subject, message, frame=None):

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content(message)

    if frame is not None:
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            msg.add_attachment(buffer.tobytes(), maintype='image', subtype='jpeg', filename='incident.jpg')

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

    print("Email alert sent")