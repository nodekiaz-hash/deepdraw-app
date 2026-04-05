import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


def send_email(to_email, subject, html_content):
    print("EMAIL SERVICE START")

    # -------------------------
    # 🔐 API KEY
    # -------------------------
    api_key = os.getenv("BREVO_API_KEY")

    if not api_key:
        print("ERROR: BREVO_API_KEY missing")
        return False

    # -------------------------
    # ⚙️ CONFIG
    # -------------------------
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    # -------------------------
    # 📩 EMAIL OBJEKTUM
    # -------------------------
    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={
            "name": "DeepDraw",
            "email": "deepdraw.newformcds@gmail.com"  # ⚠️ FONTOS: legyen hitelesítve Brevo-ban!
        },
        subject=subject,
        html_content=html_content
    )

    # -------------------------
    # 🚀 KÜLDÉS
    # -------------------------
    try:
        response = api_instance.send_transac_email(email)
        print("EMAIL SENT SUCCESS:", response)
        return True

    except ApiException as e:
        print("EMAIL ERROR:", e)
        return False