import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# --- GROQ ---
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# --- TELEGRAM ---
TOKEN = os.getenv("BOT_TOKEN")


# ---------- AI ФУНКЦИЯ ----------
def ai_answer(user_text: str) -> str:
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            model="llama3-70b-8192"
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Ошибка AI: {e}"


# ---------- МЕНЮ ----------
def get_main_menu():
    keyboard = [
        [
            KeyboardButton("Опиши идею"),
            KeyboardButton("Озвучить идею")
        ],
        [
            KeyboardButton("Как это работает"),
            KeyboardButton("Тарифы")
        ],
        [
            KeyboardButton("Мои идеи")
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🚀 Добро пожаловать в MarketBoost\n\n"
        "Я помогу проанализировать товар, нишу и идеи "
        "для заработка на маркетплейсах.\n\n"
        "Выберите действие в меню 👇"
    )

    await update.message.reply_text(
        text,
        reply_markup=get_main_menu()
    )


# ---------- ОБРАБОТКА КНОПОК ----------
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # --- ОПИСИ ИДЕЮ ---
    if user_text == "Опиши идею":
        await update.message.reply_text(
            "Опиши товар или идею текстом.\n\n"
            "Я сделаю краткий анализ ниши, спроса и рисков."
        )
        return

    # --- ОЗВУЧИТЬ ИДЕЮ ---
    if user_text == "Озвучить идею":
        await update.message.reply_text(
            "Отправь голосовое или текст.\n"
            "Я преобразую в бизнес-идею и анализ."
        )
        return

    # --- КАК ЭТО РАБОТАЕТ ---
    if user_text == "Как это работает":
        text = (
            "📊 Как работает сервис:\n\n"
            "1️⃣ Ты отправляешь товар / идею\n"
            "2️⃣ AI анализирует нишу\n"
            "3️⃣ Даёт спрос, конкуренцию и риски\n"
            "4️⃣ Предлагает улучшения\n\n"
            "Подходит для Wildberries, Ozon, Amazon."
        )

        await update.message.reply_text(text)
        return

    # --- ТАРИФЫ ---
    if user_text == "Тарифы":
        text = (
            "💰 Тарифы:\n\n"
            "Lite — 1 анализ\n"
            "Pro — 10 анализов\n"
            "Ultra — безлимит\n\n"
            "Оплата подключается позже."
        )

        await update.message.reply_text(text)
        return

    # --- МОИ ИДЕИ (AI генерит 3 идеи) ---
    if user_text == "Мои идеи":
        prompt = (
            "Предложи 3 простые идеи товара для продажи "
            "на маркетплейсах с кратким описанием спроса."
        )

        answer = ai_answer(prompt)

        await update.message.reply_text(answer)
        return

    # ---------- ЕСЛИ ПРИСЛАЛ ТЕКСТ ВНЕ КНОПОК ----------
    answer = ai_answer(user_text)

    await update.message.reply_text(answer)


# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons)
    )

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
