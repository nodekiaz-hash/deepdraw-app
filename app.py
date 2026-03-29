from database import Session, User
from calc import calculate
from email_service import send_email


def process_calculation(email, d, h, f, k):
    session = Session()

    user = session.get(User, email)

    # user check
    if not user:
        return "User not found"

    # credit check
    if user.credits <= 0:
        return "No credits left"

    # kredit levonás
    user.credits -= 1
    session.commit()

    # számítás
    result = calculate(d, h, f, k)

    # EMAIL TARTALOM
    content = f"""
Deep Drawing Calculation

Input:
d = {d}
h = {h}
f = {f}
k = {k}

Result:
D0 = {result['D0']}
Dreal = {result['Dreal']}
Draw ratio = {result['draw_ratio']}

---
Köszönjük, hogy használta szolgáltatásunkat.

Észrevételeit, javaslatait vagy fejlesztési igényeit kérjük küldje el az alábbi email címre:
info@newformcds.com

Newform CDS
"""

    # EMAIL KÜLDÉS
    send_email(email, content)

    return result


# TESZT FUTTATÁS
if __name__ == "__main__":
    output = process_calculation(
        "info@newformcds.com",
        100,
        50,
        10,
        0.05
    )

    print(output)