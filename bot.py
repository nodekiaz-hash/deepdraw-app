import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from lang import get_text

API_URL = os.getenv("API_URL")  # pl: https://your-api.up.railway.app/calculate
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

# -------------------------
# 🧠 USER STATE
# -------------------------
user_data_store = {}


def get_user(user_id):
    if user_id not in user_data_store:
        user_data_store[user_id] = {
            "state": "LANG_SELECT",
            "lang": "en",
            "data": {}
        }
    return user_data_store[user_id]


# -------------------------
# 🌍 START
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    user["state"] = "LANG_SELECT"

    keyboard = [
        [InlineKeyboardButton("🇭🇺 Magyar", callback_data="lang_hu")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de")],
    ]

    await update.message.reply_text(
        "Válassz nyelvet / Choose language:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# -------------------------
# 🔘 BUTTON KEZELÉS
# -------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = get_user(query.from_user.id)

    # --- NYELV ---
    if query.data.startswith("lang_"):
        lang = query.data.split("_")[1]
        user["lang"] = lang
        user["state"] = "WELCOME"

        keyboard = [[InlineKeyboardButton(get_text(lang, "continue"), callback_data="continue")]]

        await query.edit_message_text(
            get_text(lang, "welcome"),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # --- CONTINUE ---
    elif query.data == "continue":
        user["state"] = "EMAIL_MENU"

        lang = user["lang"]

        keyboard = [
            [InlineKeyboardButton(get_text(lang, "menu_email"), callback_data="email")],
            [InlineKeyboardButton(get_text(lang, "menu_exit"), callback_data="exit")]
        ]

        await query.edit_message_text(
            "📧",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # --- EMAIL ---
    elif query.data == "email":
        user["state"] = "EMAIL_INPUT"

        await query.edit_message_text(
            get_text(user["lang"], "ask_email")
        )

    # --- EXIT ---
    elif query.data == "exit":
        user["state"] = "LANG_SELECT"

        keyboard = [
            [InlineKeyboardButton("🇭🇺 Magyar", callback_data="lang_hu")],
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de")],
        ]

        await query.edit_message_text(
            "Restarting...",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # --- MAIN MENU ---
    elif query.data == "calc":
        user["state"] = "CALC_D"
        await query.edit_message_text(get_text(user["lang"], "ask_d"))

    elif query.data == "credit":
        from credit import get_credit_info
        msg = get_credit_info(user["data"].get("email"), user["lang"])

        keyboard = get_main_menu(user["lang"])

        await query.edit_message_text(msg, reply_markup=keyboard)

    elif query.data == "new_calc":
        user["state"] = "CALC_D"
        await query.edit_message_text(get_text(user["lang"], "ask_d"))


# -------------------------
# 📋 MENÜ
# -------------------------
def get_main_menu(lang):
    keyboard = [
        [InlineKeyboardButton(get_text(lang, "menu_calculation"), callback_data="calc")],
        [InlineKeyboardButton(get_text(lang, "menu_credit"), callback_data="credit")],
        [InlineKeyboardButton(get_text(lang, "menu_exit"), callback_data="exit")]
    ]
    return InlineKeyboardMarkup(keyboard)


# -------------------------
# ✉️ MESSAGE KEZELÉS
# -------------------------
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    text = update.message.text
    lang = user["lang"]

    # --- EMAIL ---
    if user["state"] == "EMAIL_INPUT":
        user["data"]["email"] = text

        # TODO: database check (most dummy)
        credit = 3

        user["state"] = "MAIN_MENU"

        await update.message.reply_text(
            get_text(lang, "email_status", email=text, credit=credit),
            reply_markup=get_main_menu(lang)
        )

    # --- CALC INPUTOK ---
    elif user["state"] in ["CALC_D", "CALC_H", "CALC_F", "CALC_K"]:
        try:
            value = float(text)
        except:
            await update.message.reply_text(get_text(lang, "invalid_number"))
            return

        if user["state"] == "CALC_D":
            user["data"]["d"] = value
            user["state"] = "CALC_H"
            await update.message.reply_text(get_text(lang, "ask_h"))

        elif user["state"] == "CALC_H":
            user["data"]["h"] = value
            user["state"] = "CALC_F"
            await update.message.reply_text(get_text(lang, "ask_f"))

        elif user["state"] == "CALC_F":
            user["data"]["f"] = value
            user["state"] = "CALC_K"
            await update.message.reply_text(get_text(lang, "ask_k"))

        elif user["state"] == "CALC_K":
            user["data"]["k"] = value

            # API CALL
            payload = {
                "email": user["data"]["email"],
                "d": user["data"]["d"],
                "h": user["data"]["h"],
                "f": user["data"]["f"],
                "k": user["data"]["k"],
                "lang": lang
            }

            try:
                requests.post(API_URL, json=payload)
            except Exception as e:
                print("API ERROR:", e)

            # RESULT DISPLAY
            msg = "\n".join([
                get_text(lang, "result_header"),
                get_text(lang, "result_d", d=user["data"]["d"]),
                get_text(lang, "result_h", h=user["data"]["h"]),
                get_text(lang, "result_f", f=user["data"]["f"]),
                get_text(lang, "result_k", k=user["data"]["k"]),
                "",
                get_text(lang, "result_sent")
            ])

            user["state"] = "MAIN_MENU"

            keyboard = [
                [InlineKeyboardButton(get_text(lang, "menu_new_calculation"), callback_data="new_calc")],
                [InlineKeyboardButton(get_text(lang, "menu_credit"), callback_data="credit")],
                [InlineKeyboardButton(get_text(lang, "menu_exit"), callback_data="exit")]
            ]

            await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))


# -------------------------
# 🚀 APP INDÍTÁS
# -------------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("BOT RUNNING...")
    app.run_polling()


if __name__ == "__main__":
    main()