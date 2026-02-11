import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from groq import Groq

# --- КЛЮЧИ ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# --- ЛИМИТЫ ---
FREE_LIMIT = 3
user_requests = {}
user_counts = {}

# --- МЕНЮ ---
menu = ReplyKeyboardMarkup(
    [
        ["📉 Почему нет продаж", "🛍 Улучшить карточку"],
        ["📊 Анализ ниши", "💰 Расчёт прибыли"],
        ["💡 Идеи товаров"],
        ["📂 Мои запросы"],
        ["❓ Как это работает", "💼 Тарифы"],
    ],
    resize_keyboard=True
)

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 MarketBoost запущен!\n\n"
        "🎁 Тебе доступно 3 бесплатных анализа\n\n"
        "Выбери функцию 👇",
        reply_markup=menu
    )

# --- ПОКАЗ ЗАПРОСОВ ---
async def show_requests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_requests:
        await update.message.reply_text("Запросов пока нет.")
        return

    text = "📂 Твои запросы:\n\n"

    for i, req in enumerate(user_requests[user_id][-5:], 1):
        text += f"{i}. {req}\n"

    await update.message.reply_text(text)

# --- ПРОВЕРКА ЛИМИТА ---
def check_limit(user_id):

    if user_id not in user_counts:
        user_counts[user_id] = 0

    if user_counts[user_id] >= FREE_LIMIT:
        return False

    user_counts[user_id] += 1
    return True

# --- AI ---
async def ai_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    text = update.message.text

    # Кнопка истории
    if text == "📂 Мои запросы":
        await show_requests(update, context)
        return

    # Проверка лимита
    if not check_limit(user_id):
        await update.message.reply_text(
            "❌ Лимит бесплатных анализов исчерпан.\n\n"
            "Чтобы продолжить пользоваться ботом — оформи тариф 💼"
        )
        return

    # Сохраняем запрос
    if user_id not in user_requests:
        user_requests[user_id] = []

    user_requests[user_id].append(text)

    await update.message.reply_text("⏳ Анализирую...")

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Ты эксперт по маркетплейсам Wildberries и Ozon."
                },
                {
                    "role": "user",
                    "content": text
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
