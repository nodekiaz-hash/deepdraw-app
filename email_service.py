import smtplib
from email.mime.text import MIMEText


def send_email(to_email, content):
    print("EMAIL FUNCTION STARTED")

    try:
        msg = MIMEText(content)
        msg['Subject'] = 'Deep Drawing Result'
        msg['From'] = 'deepdraw.newformcds@gmail.com'
        msg['To'] = to_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('deepdraw.newformcds@gmail.com', 'qnbpjvcbrwlwtgpj')
            server.send_message(msg)

        print("EMAIL SENT")

    except Exception as e:
        print("EMAIL ERROR:", e)