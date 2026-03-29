from telegram import Update, ReplyKeyboardMarkup
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

API_URL = "http://127.0.0.1:8000/calculate"

LANG, MENU_START, EMAIL, MENU_MAIN, D, H, F, K, END = range(9)


# ------------------ TEXTS ------------------
TEXTS = {
    "hu": {
        "welcome": "Üdvözöl a NewformCDS!",
        "choose_lang": "Válassz nyelvet:",
        "menu_start": "Válassz:\nEmail megadás / Regisztráció",
        "ask_email": "Add meg a regisztrált email címed:",
        "invalid_email": "Érvénytelen email.",
        "not_found": "Email nem található.",
        "registered_info": "Regisztrációhoz küldd el email címed az info@newformcds.com címre.\nKöszönjük együttműködésed.",
        "menu_main": "Válassz:",
        "calc": "Számítás",
        "topup": "Kredit feltöltés",
        "topup_info": "Kredit rendeléshez írj az info@newformcds.com email címre.\nA számlát elküldjük, befizetés után jóváírjuk a krediteket.",
        "ask_d": "Add meg a d (mm):",
        "ask_h": "Add meg a h (mm):",
        "ask_f": "Add meg az f (mm):",
        "ask_k": "Add meg a k értéket:",
        "result": "Eredmény:",
        "email_sent": "Az eredményt emailben elküldtük.",
        "thanks": "Köszönjük, hogy a NewformCDS alkalmazását használta.",
        "restart": "Restart",
        "close": "Close",
        "bye": "További szép napot kíván a NewformCDS csapata.\nA bot a /start paranccsal indítható újra."
    },
    "en": {
        "welcome": "Welcome to NewformCDS!",
        "choose_lang": "Choose language:",
        "menu_start": "Choose:\nEnter email / Register",
        "ask_email": "Enter your registered email:",
        "invalid_email": "Invalid email.",
        "not_found": "Email not found.",
        "registered_info": "To register, send your email to info@newformcds.com.\nThank you.",
        "menu_main": "Choose:",
        "calc": "Calculation",
        "topup": "Top up",
        "topup_info": "To order credits, email info@newformcds.com.\nInvoice will be sent.",
        "ask_d": "Enter d:",
        "ask_h": "Enter h:",
        "ask_f": "Enter f:",
        "ask_k": "Enter k:",
        "result": "Result:",
        "email_sent": "Results sent via email.",
        "thanks": "Thank you for using NewformCDS.",
        "restart": "Restart",
        "close": "Close",
        "bye": "Have a nice day from NewformCDS.\nUse /start to restart."
    }
}


def t(lang, key):
    return TEXTS[lang][key]


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


# ------------------ START ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Choose language / Válassz nyelvet:",
        reply_markup=ReplyKeyboardMarkup([["English", "Magyar"]], resize_keyboard=True)
    )
    return LANG


async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = "hu" if update.message.text == "Magyar" else "en"
    context.user_data["lang"] = lang

    await update.message.reply_text(t(lang, "welcome"))

    await update.message.reply_text(
        t(lang, "menu_start"),
        reply_markup=ReplyKeyboardMarkup(
            [["Email", "Register"]],
            resize_keyboard=True
        )
    )
    return MENU_START


# ------------------ MENU START ------------------
async def menu_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]

    if update.message.text.lower() == "register":
        await update.message.reply_text(t(lang, "registered_info"))
        return MENU_START

    await update.message.reply_text(t(lang, "ask_email"))
    return EMAIL


# ------------------ EMAIL ------------------
async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]
    email = update.message.text

    if not is_valid_email(email):
        await update.message.reply_text(t(lang, "invalid_email"))
        return MENU_START

    session = Session()
    user = session.get(User, email)

    if not user:
        await update.message.reply_text(t(lang, "not_found"))
        return MENU_START

    context.user_data["email"] = email

    await update.message.reply_text(
        f"{email}\nCredits: {user.credits}",
        reply_markup=ReplyKeyboardMarkup(
            [[t(lang, "calc"), t(lang, "topup")]],
            resize_keyboard=True
        )
    )

    return MENU_MAIN


# ------------------ MAIN MENU ------------------
async def menu_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]

    if update.message.text == t(lang, "topup"):
        await update.message.reply_text(t(lang, "topup_info"))
        return MENU_MAIN

    if update.message.text == t(lang, "calc"):
        await update.message.reply_text(t(lang, "ask_d"))
        return D

    return MENU_MAIN


# ------------------ CALC FLOW ------------------
async def get_d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["d"] = float(update.message.text)
    await update.message.reply_text(t(context.user_data["lang"], "ask_h"))
    return H


async def get_h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["h"] = float(update.message.text)
    await update.message.reply_text(t(context.user_data["lang"], "ask_f"))
    return F


async def get_f(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["f"] = float(update.message.text)
    await update.message.reply_text(t(context.user_data["lang"], "ask_k"))
    return K


async def get_k(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]
    context.user_data["k"] = float(update.message.text)

    response = requests.post(API_URL, json={
        "email": context.user_data["email"],
        "d": context.user_data["d"],
        "h": context.user_data["h"],
        "f": context.user_data["f"],
        "k": context.user_data["k"]
    })

    data = response.json()

    if data["status"] == "success":
        r = data["data"]
        text = (
            f"{t(lang,'result')}\n"
            f"D0: {r['D0']}\n"
            f"Dreal: {r['Dreal']}\n"
            f"Draw ratio: {r['draw_ratio']}\n\n"
            f"{t(lang,'email_sent')}\n\n"
            f"{t(lang,'thanks')}"
        )
    else:
        text = data["message"]

    await update.message.reply_text(text)

    await update.message.reply_text(
        "Restart / Close",
        reply_markup=ReplyKeyboardMarkup(
            [[t(lang, "restart"), t(lang, "close")]],
            resize_keyboard=True
        )
    )

    return END


# ------------------ END ------------------
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]

    if update.message.text == t(lang, "restart"):
        return await start(update, context)

    if update.message.text == t(lang, "close"):
        await update.message.reply_text(t(lang, "bye"))
        return ConversationHandler.END

    return END


# ------------------ APP ------------------
app = ApplicationBuilder().token("8504676341:AAFtYGKWSL6sWAv24TbB7ZR8vxxkq5vF75g").build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_lang)],
        MENU_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_start)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email)],
        MENU_MAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_main)],
        D: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_d)],
        H: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_h)],
        F: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_f)],
        K: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_k)],
        END: [MessageHandler(filters.TEXT & ~filters.COMMAND, end)],
    },
    fallbacks=[]
)

app.add_handler(conv)

app.run_polling()