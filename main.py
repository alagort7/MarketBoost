import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

# ---------- КНОПКИ ----------
def main_menu():
    keyboard = [
        ["✍️ Опиши идею", "🎤 Озвучить идею"],
        ["💡 Как это работает"],
        ["💰 Тарифы", "💎 Идеи для тебя"]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 *Idea2Cash*\n\n"
        "Я превращаю идеи в деньги.\n"
        "Опиши идею — я покажу потенциал 💸",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# ---------- ОБРАБОТКА КНОПОК ----------
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "✍️ Опиши идею":
        await update.message.reply_text(
            "Напиши свою идею одним сообщением 👇"
        )

    elif text == "🎤 Озвучить идею":
        await update.message.reply_text(
            "Запиши голосовое сообщение с идеей 🎙"
        )

    elif text == "💡 Как это работает":
        await update.message.reply_text(
            "Ты отправляешь идею — я анализирую её и показываю,\n"
            "как на ней можно заработать 💡"
        )

    elif text == "💰 Тарифы":
        await update.message.reply_text(
            "🔓 Бесплатно — первичная оценка\n"
            "💎 Pro — глубокий разбор и план монетизации\n\n"
            "Скоро 🚀"
        )

    elif text == "💎 Идеи для тебя":
        await update.message.reply_text(
            "Я подберу 2–3 идеи под твою нишу 💎\n"
            "Глубокий разбор — по запросу"
        )

    else:
        await update.message.reply_text(
            "Выбери действие с помощью кнопок ⬇️",
            reply_markup=main_menu()
        )

# ---------- ЗАПУСК ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    app.run_polling()

if __name__ == "__main__":
    main()
