import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from calc import process_calculation_logic  # 👉 ez a TE számítási függvényed


# -------------------------
# 🌍 NYELVI SZÖVEGEK
# -------------------------
TEXTS = {
    "hu": {
        "subject": "Számítás eredmény",
        "body": "Az eredményed:"
    },
    "en": {
        "subject": "Calculation result",
        "body": "Your result:"
    },
    "de": {
        "subject": "Berechnung Ergebnis",
        "body": "Dein Ergebnis:"
    }
}


# -------------------------
# 📧 EMAIL KÜLDÉS (BREVO)
# -------------------------
def send_email(to_email, subject, html_content):
    print("EMAIL FUNCTION STARTED")

    api_key = os.getenv("BREVO_API_KEY")

    if not api_key:
        print("HIBA: nincs BREVO_API_KEY beállítva")
        return

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"name": "DeepDraw", "email": "noreply@yourdomain.com"},  # 👉 ezt később saját domainre!
        subject=subject,
        html_content=html_content
    )

    try:
        response = api_instance.send_transac_email(send_smtp_email)
        print("EMAIL SENT:", response)

    except ApiException as e:
        print("EMAIL ERROR:", e)


# -------------------------
# 🚀 FŐ FÜGGVÉNY
# -------------------------
def process_calculation(email, d, h, f, k, lang="en"):
    try:
        print("PROCESS START")

        # 1. számítás (a TE calc.py-ból)
        result = process_calculation_logic(email, d, h, f, k)

        # ha string → hiba
        if isinstance(result, str):
            return result

        # 2. nyelv
        t = TEXTS.get(lang, TEXTS["en"])

        subject = t["subject"]

        html_content = f"""
        <h2>{t['body']}</h2>
        <p><b>D0:</b> {result['D0']}</p>
        <p><b>Dreal:</b> {result['Dreal']}</p>
        <p><b>Draw ratio:</b> {result['draw_ratio']}</p>
        """

        # 3. email küldés
        send_email(email, subject, html_content)

        # 4. visszatérés API felé
        return result

    except Exception as e:
        print("PROCESS ERROR:", e)
        return str(e)