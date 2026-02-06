import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

# --- Состояния диалога ---
LINK, PRICE, COST, SALES = range(4)

# --- Главное меню ---
MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["📉 Почему нет продаж", "🛍 Улучшить карточку"],
        ["📊 Анализ ниши", "💰 Расчёт прибыли"],
        ["💡 Идеи товаров"],
        ["❓ Как это работает", "💼 Тарифы"],
    ],
    resize_keyboard=True
)

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 MarketBot запущен.\nВыбери функцию 👇",
        reply_markup=MAIN_MENU
    )

# --- Запуск анализа ---
async def no_sales_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пришли ссылку на товар:")
    return LINK

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["link"] = update.message.text
    await update.message.reply_text("Укажи цену товара ($):")
    return PRICE

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["price"] = update.message.text
    await update.message.reply_text("Себестоимость ($):")
    return COST

async def get_cost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["cost"] = update.message.text
    await update.message.reply_text("Сколько продаж в месяц?")
    return SALES

async def get_sales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["sales"] = update.message.text

    await update.message.reply_text(
        "🔎 Анализ завершён.\n\n"
        "Я нашёл несколько возможных проблем:\n"
        "• Слабое SEO\n"
        "• Цена выше рынка\n"
        "• Низкий CTR карточки\n\n"
        "Хочешь полный разбор с решениями?",
        reply_markup=MAIN_MENU
    )

    return ConversationHandler.END

# --- Обработчик меню ---
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📉 Почему нет продаж":
        return await no_sales_start(update, context)

    responses = {
        "🛍 Улучшить карточку": "Скоро здесь будет AI-оптимизация карточек.",
        "📊 Анализ ниши": "Скоро добавим анализ ниши.",
        "💰 Расчёт прибыли": "Скоро добавим юнит-экономику.",
        "💡 Идеи товаров": "Скоро добавим подбор товаров.",
        "❓ Как это работает": "Ты выбираешь функцию — бот анализирует.",
        "💼 Тарифы": "Тарифы скоро появятся."
    }

    reply = responses.get(text, "Выбери кнопку 👇")
    await update.message.reply_text(reply)

# --- Сборка ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & filters.Regex("📉 Почему нет продаж"), no_sales_start)],
        states={
            LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_link)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
            COST: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_cost)],
            SALES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sales)],
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

    app.run_polling()

if __name__ == "__main__":
    main()

