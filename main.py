import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

# Главное меню
MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["✍️ Опиши идею", "🎤 Озвучить идею"],
        ["💡 Как это работает"],
        ["💰 Тарифы", "💎 Идеи для тебя"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Добро пожаловать в Idea2Cash\n\n"
        "Я помогаю превращать идеи в деньги.\n"
        "Выбери, с чего начнём 👇",
        reply_markup=MAIN_MENU
    )

async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "✍️ Опиши идею":
        await update.message.reply_text(
            "Опиши свою идею одним сообщением.\n"
            "Я посмотрю, есть ли в ней денежный потенциал 💸"
        )

    elif text == "🎤 Озвучить идею":
        await update.message.reply_text(
            "Запиши голосовое сообщение с идеей 🎙\n"
            "Я расшифрую и разберу её."
        )

    elif text == "💡 Как это работает":
        await update.message.reply_text(
            "Ты отправляешь идею — я показываю,\n"
            "есть ли спрос и как на ней заработать."
        )

    elif text == "💰 Тарифы":
        await update.message.reply_text(
            "🔓 Бесплатно — первичная оценка идеи\n"
            "💎 Pro — глубокий разбор + план монетизации\n\n"
            "Подробности скоро 🚀"
        )

    elif text == "💎 Идеи для тебя":
        await update.message.reply_text(
            "Напиши сферу или тему,\n"
            "и я предложу 2–3 идеи специально для тебя 💡"
        )

    else:
        await update.message.reply_text(
            "Пожалуйста, выбери действие через меню 👇",
            reply_markup=MAIN_MENU
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

    app.run_polling()

if __name__ == "__main__":
    main()
