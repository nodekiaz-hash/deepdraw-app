# -------------------------
# 🌍 NYELVI SZÖVEGEK
# -------------------------

TEXTS = {
    "hu": {
        # --- általános ---
        "welcome": """Üdvözöllek a NewformCDS Mélyhúzás teríték számítás bot-ban.

A bot megadott alap méretek alapján lemez teríték méretet számol a mélyhúzáshoz, ami nagy segítség árajánlat kalkulációhoz.

A jelenlegi verzió egylépéses mélyhúzás demo verzió, amely igény esetén tovább fejleszthető komplett folyamattá.""",

        "continue": "Tovább",

        # --- menük ---
        "menu_email": "Email megadása",
        "menu_calculation": "Számítás indítása",
        "menu_credit": "Credit feltöltés",
        "menu_exit": "Kilépés",
        "menu_new_calculation": "Új számítás",

        # --- email ---
        "ask_email": "📧 Add meg az email címed:",
        "email_status": "Email: {email}\nCredit: {credit}",

        # --- credit ---
        "credit_info": """Kredit feltöltéshez írj az alábbi email címre:

info@newformcds.com

Kérlek add meg a regisztrált email címed a levélben.""",

        # --- számítás ---
        "ask_d": "📐 Add meg a külső átmérőt d (mm):",
        "ask_h": "📏 Add meg a mélységet h (mm):",
        "ask_f": "📄 Add meg a lemezvastagságot f (mm):",
        "ask_k": "⚙️ Add meg a k faktort:",

        "invalid_number": "❌ Hibás érték! Kérlek számot adj meg.",

        # --- eredmény ---
        "result_header": "📊 Mélyhúzás számítási adatok:",
        "result_d": "Külső átmérő d (mm): {d}",
        "result_h": "Mélység h (mm): {h}",
        "result_f": "Lemezvastagság f (mm): {f}",
        "result_k": "k faktor: {k}",

        "result_sent": """📧 Az eredményeket elküldtük az email címedre.

Köszönjük, hogy a NewformCDS-t választottad!""",
    },

    "en": {
        # --- általános ---
        "welcome": """Welcome to the NewformCDS Deep Drawing Blank Calculation Bot.

This tool calculates sheet metal blank size based on input parameters, supporting quotation and planning processes.

This is a demo version for single-step deep drawing.""",

        "continue": "Continue",

        # --- menük ---
        "menu_email": "Enter email",
        "menu_calculation": "Start calculation",
        "menu_credit": "Top up credit",
        "menu_exit": "Exit",
        "menu_new_calculation": "New calculation",

        # --- email ---
        "ask_email": "📧 Enter your email address:",
        "email_status": "Email: {email}\nCredit: {credit}",

        # --- credit ---
        "credit_info": """To top up your credits, please contact:

info@newformcds.com

Include your registered email address in the message.""",

        # --- számítás ---
        "ask_d": "📐 Enter outer diameter d (mm):",
        "ask_h": "📏 Enter depth h (mm):",
        "ask_f": "📄 Enter sheet thickness f (mm):",
        "ask_k": "⚙️ Enter k factor:",

        "invalid_number": "❌ Invalid value! Please enter a number.",

        # --- eredmény ---
        "result_header": "📊 Deep drawing calculation data:",
        "result_d": "Outer diameter d (mm): {d}",
        "result_h": "Depth h (mm): {h}",
        "result_f": "Sheet thickness f (mm): {f}",
        "result_k": "k factor: {k}",

        "result_sent": """📧 The results have been sent to your email.

Thank you for choosing NewformCDS!""",
    },

    "de": {
        # --- általános ---
        "welcome": """Willkommen beim NewformCDS Tiefzieh-Zuschnittsberechnungs-Bot.

Dieses Tool berechnet die Blechzuschnittgröße basierend auf Eingabedaten und unterstützt Angebotskalkulationen.

Dies ist eine Demo-Version für einstufiges Tiefziehen.""",

        "continue": "Weiter",

        # --- menük ---
        "menu_email": "E-Mail eingeben",
        "menu_calculation": "Berechnung starten",
        "menu_credit": "Credits aufladen",
        "menu_exit": "Beenden",
        "menu_new_calculation": "Neue Berechnung",

        # --- email ---
        "ask_email": "📧 E-Mail-Adresse eingeben:",
        "email_status": "E-Mail: {email}\nCredits: {credit}",

        # --- credit ---
        "credit_info": """Zum Aufladen der Credits kontaktieren Sie bitte:

info@newformcds.com

Bitte geben Sie Ihre registrierte E-Mail-Adresse an.""",

        # --- számítás ---
        "ask_d": "📐 Außendurchmesser d (mm):",
        "ask_h": "📏 Tiefe h (mm):",
        "ask_f": "📄 Blechdicke f (mm):",
        "ask_k": "⚙️ k-Faktor eingeben:",

        "invalid_number": "❌ Ungültiger Wert! Bitte Zahl eingeben.",

        # --- eredmény ---
        "result_header": "📊 Tiefzieh-Berechnungsdaten:",
        "result_d": "Außendurchmesser d (mm): {d}",
        "result_h": "Tiefe h (mm): {h}",
        "result_f": "Blechdicke f (mm): {f}",
        "result_k": "k-Faktor: {k}",

        "result_sent": """📧 Die Ergebnisse wurden per E-Mail gesendet.

Vielen Dank für die Nutzung von NewformCDS!""",
    }
}


# -------------------------
# 🔧 SEGÉD FÜGGVÉNY
# -------------------------

def get_text(lang: str, key: str, **kwargs) -> str:
    """
    Szöveg lekérése nyelv alapján.
    Ha nincs kulcs → visszaadja a key-t.
    """
    text = TEXTS.get(lang, TEXTS["en"]).get(key, key)
    return text.format(**kwargs)