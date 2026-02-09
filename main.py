import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq

# --- КЛЮЧИ ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# --- МЕНЮ ---
menu = ReplyKeyboardMarkup(
    [
        ["📉 Почему нет продаж", "🛍 Улучшить карточку"],
        ["📊 Анализ ниши", "💰 Расчёт прибыли"],
        ["💡 Идеи товаров"],
        ["❓ Как это работает", "💼 Тарифы"],
    ],
    resize_keyboard=True
)

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 MarketBoost запущен!\n\nВыбери функцию 👇",
        reply_markup=menu
    )

# --- AI ОТВЕТ ---
async def ai_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    await update.message.reply_text("⏳ Анализирую...")

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Ты эксперт по маркетплейсам Wildberries и Ozon. Отвечай как аналитик продавцов."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            temperature=0.7,
            max_tokens=800
        )

        answer = completion.choices[0].message.content

        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(f"Ошибка AI:\n{e}")

# --- MAIN ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_answer))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
