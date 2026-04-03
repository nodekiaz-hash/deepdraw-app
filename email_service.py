import os
import requests


def send_email(to_email, content):
    print("EMAIL FUNCTION STARTED")

    try:
        api_key = os.getenv("BREVO_API_KEY")

        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }

        data = {
            "sender": {
                "name": "DeepDraw",
                "email": "deepdraw.newformcds@gmail.com"
            },
            "to": [
                {
                    "email": to_email
                }
            ],
            "subject": "Deep Drawing Result",
            "htmlContent": f"<html><body><pre>{content}</pre></body></html>"
        }

        response = requests.post(url, json=data, headers=headers)

        print("EMAIL RESPONSE:", response.status_code, response.text)

    except Exception as e:
        print("EMAIL ERROR:", e)