from calc import calculate
from email_service import send_email
from lang import get_text
from database import get_or_create_user, decrement_credit


# -------------------------
# 🚀 FŐ FÜGGVÉNY
# -------------------------
def process_calculation(email, d, h, f, k, lang="en"):
    """
    Teljes számítási folyamat:
    - user ellenőrzés (DB)
    - credit ellenőrzés
    - számítás
    - credit levonás
    - email küldés
    - visszatérés API felé
    """

    try:
        print("PROCESS START")

        # -------------------------
        # 1. USER + CREDIT (DB)
        # -------------------------
        user, is_new = get_or_create_user(email)
        credit = user["credit"]

        if credit <= 0:
            return {
                "status": "error",
                "message": get_text(lang, "no_credit")
            }

        # -------------------------
        # 2. SZÁMÍTÁS
        # -------------------------
        result = calculate(d, h, f, k)

        # -------------------------
        # 3. CREDIT LEVONÁS
        # -------------------------
        decrement_credit(email)

        # -------------------------
        # 4. EMAIL SZÖVEG
        # -------------------------
        subject = get_text(lang, "email_subject")

        html_content = f"""
        <h2>{get_text(lang, "result_header")}</h2>

        <p>{get_text(lang, "result_d", d=d)}</p>
        <p>{get_text(lang, "result_h", h=h)}</p>
        <p>{get_text(lang, "result_f", f=f)}</p>
        <p>{get_text(lang, "result_k", k=k)}</p>

        <hr>

        <p><b>D0:</b> {result['D0']}</p>
        <p><b>Dreal:</b> {result['Dreal']}</p>
        <p><b>Draw ratio:</b> {result['draw_ratio']}</p>
        """

        # -------------------------
        # 5. EMAIL KÜLDÉS
        # -------------------------
        send_email(email, subject, html_content)

        # -------------------------
        # 6. VISSZATÉRÉS
        # -------------------------
        return {
            "status": "success",
            "result": result,
            "credit_remaining": credit - 1
        }

    except Exception as e:
        print("APP ERROR:", e)
        return {
            "status": "error",
            "message": str(e)
        }