from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
import requests
import re

from database import Session, User

API_URL = "https://deepdraw-app-production.up.railway.app/calculate"

LANG, EMAIL, MENU_MAIN, D, H, F, K, END = range(8)


TEXTS = {
    "hu": {
        "welcome": "🔵 Üdvözöl a NewformCDS!",
        "ask_email": "📧 Add meg az email címed:",
        "invalid_email": "❌ Érvénytelen email.",
        "registered": "✅ Regisztráció +5 kredit",
        "menu": "⚙️ Főmenü",
        "calc": "📐 Számítás",
        "credits": "💳 Kreditek",
        "topup": "💰 Feltöltés",
        "exit": "❌ Kilépés",
        "topup_info": "Email: info@newformcds.com",
        "ask_d": "📏 d – külső átmérő (mm):",
        "ask_h": "📏 h – mélység (mm):",
        "ask_f": "📏 f – lemezvastagság (mm):",
        "ask_k": "📏 k – faktor:",
        "result": "📊 Eredmény",
        "no_credit": "❌ Nincs kredited!",
        "error": "⚠️ API nem fut!",
        "next": "Mi legyen a következő lépés?",
        "new_calc": "🔄 Új számítás",
        "back": "🏠 Főmenü"
    },
    "en": {
        "welcome": "🔵 Welcome!",
        "ask_email": "📧 Enter email:",
        "invalid_email": "❌ Invalid email.",
        "registered": "✅ +5 credits",
        "menu": "⚙️ Menu",
        "calc": "📐 Calculation",
        "credits": "💳 Credits",
        "topup": "💰 Top up",
        "exit": "❌ Exit",
        "topup_info": "Email: info@newformcds.com",
        "ask_d": "📏 d:",
        "ask_h": "📏 h:",
        "ask_f": "📏 f:",
        "ask_k": "📏 k:",
        "result": "📊 Result",
        "no_credit": "❌ No credits!",
        "error": "⚠️ API offline!",
        "next": "Next?",
        "new_calc": "🔄 New",
        "back": "🏠 Menu"
    },
    "de": {
        "welcome": "🔵 Willkommen!",
        "ask_email": "📧 E-Mail:",
        "invalid_email": "❌ Ungültig.",
        "registered": "✅ +5 Credits",
        "menu": "⚙️ Menü",
        "calc": "📐 Berechnung",
        "credits": "💳 Guthaben",
        "topup": "💰 Aufladen",
        "exit": "❌ Beenden",
        "topup_info": "Email: info@newformcds.com",
        "ask_d": "📏 d:",
        "ask_h": "📏 h:",
        "ask_f": "📏 f:",
        "ask_k": "📏 k:",
        "result": "📊 Ergebnis",
        "no_credit": "❌ Kein Guthaben!",
        "error": "⚠️ API offline!",
        "next": "Weiter?",
        "new_calc": "🔄 Neu",
        "back": "🏠 Menü"
    }
}


def t(lang, key):
    return TEXTS[lang][key]


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def safe_float(val):
    try:
        return float(val)
    except:
        return None


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "🌍 Language:",
        reply_markup=ReplyKeyboardMarkup(
            [["🇭🇺 Magyar", "🇬🇧 English", "🇩🇪 Deutsch"]],
            resize_keyboard=True
        )
    )
    return LANG


async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text

    if "Magyar" in txt:
        lang = "hu"
    elif "Deutsch" in txt:
        lang = "de"
    else:
        lang = "en"

    context.user_data["lang"] = lang

    await update.message.reply_text(t(lang, "welcome"))
    await update.message.reply_text(t(lang, "ask_email"))

    return EMAIL


# ---------------- EMAIL ----------------
async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]
    email = update.message.text.strip()

    if not is_valid_email(email):
        await update.message.reply_text(t(lang, "invalid_email"))
        return EMAIL

    session = Session()
    user = session.get(User, email)

    if not user:
        user = User(email=email, credits=5)
        session.add(user)
        session.commit()
        await update.message.reply_text(t(lang, "registered"))

    context.user_data["email"] = email

    await show_menu(update, context)
    return MENU_MAIN


# ---------------- MENU ----------------
async def show_menu(update, context):
    lang = context.user_data["lang"]
    session = Session()
    user = session.get(User, context.user_data["email"])

    await update.message.reply_text(
        f"{t(lang,'menu')}\n📧 {user.email}\n💳 {user.credits}",
        reply_markup=ReplyKeyboardMarkup(
            [
                [t(lang, "calc")],
                [t(lang, "credits"), t(lang, "topup")],
                [t(lang, "exit")]
            ],
            resize_keyboard=True
        )
    )


async def menu_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]
    text = update.message.text

    if text == t(lang, "calc"):
        await update.message.reply_text(t(lang, "ask_d"))
        return D

    if text == t(lang, "credits"):
        await show_menu(update, context)
        return MENU_MAIN

    if text == t(lang, "topup"):
        await update.message.reply_text(t(lang, "topup_info"))
        return MENU_MAIN

    if text == t(lang, "exit"):
        context.user_data.clear()
        await update.message.reply_text(
            "👋",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    return MENU_MAIN


# ---------------- CALC ----------------
async def get_d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    val = safe_float(update.message.text)
    if val is None:
        return D
    context.user_data["d"] = val
    await update.message.reply_text(t(context.user_data["lang"], "ask_h"))
    return H


async def get_h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    val = safe_float(update.message.text)
    if val is None:
        return H
    context.user_data["h"] = val
    await update.message.reply_text(t(context.user_data["lang"], "ask_f"))
    return F


async def get_f(update: Update, context: ContextTypes.DEFAULT_TYPE):
    val = safe_float(update.message.text)
    if val is None:
        return F
    context.user_data["f"] = val
    await update.message.reply_text(t(context.user_data["lang"], "ask_k"))
    return K


async def get_k(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]
    val = safe_float(update.message.text)

    if val is None:
        return K

    context.user_data["k"] = val

    session = Session()
    user = session.get(User, context.user_data["email"])

    if user.credits < 1:
        await update.message.reply_text(t(lang, "no_credit"))
        await show_menu(update, context)
        return MENU_MAIN

    user.credits -= 1
    session.commit()

    try:
        res = requests.post(API_URL, json={
            "email": user.email,
            "d": context.user_data["d"],
            "h": context.user_data["h"],
            "f": context.user_data["f"],
            "k": context.user_data["k"]
        })

        if res.status_code != 200:
            raise Exception()

        r = res.json()["data"]

        text = f"{t(lang,'result')}\n\nD0: {r['D0']}\nDreal: {r['Dreal']}\nDraw ratio: {r['draw_ratio']}"

    except:
        text = t(lang, "error")

    await update.message.reply_text(text)

    await show_menu(update, context)
    return MENU_MAIN


# ---------------- APP ----------------
import os

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_lang)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email)],
        MENU_MAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_main)],
        D: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_d)],
        H: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_h)],
        F: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_f)],
        K: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_k)],
    },
    fallbacks=[CommandHandler("start", start)]
)

app.add_handler(conv)
app.run_polling()