import json
import os
import telegram
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

PY_DIR = Path(__file__).parent

MENU, ASK_QUESTION = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.edited_message:
        return MENU

    keyboard = [
        [
            InlineKeyboardButton(
                "Задать вопрос", callback_data="question"
            ),
            InlineKeyboardButton(
                "Помощь", callback_data="help"
            ),
        ]
    ]

    file_path = PY_DIR / "assets" / "texts" / "START.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        text_to_send = file.read()

    if update.message:
        await update.message.reply_text(
            text_to_send, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
        )
    else:
        query = update.callback_query
        await query.answer()
        if query.message and query.message.text:
            await query.edit_message_text(
                text_to_send,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="HTML",
            )
        else:
            await query.message.reply_text(
                text_to_send,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="HTML",
            )

    return MENU


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Start", callback_data="start")]
    ]
    await update.message.reply_text(
        "Нажмите кнопку Start, чтобы начать:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU


async def respond_to_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(f"Вы ввели: {user_text}. Вот мой ответ!")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("Диалог отменен. Напишите /start, чтобы начать заново.")
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("Диалог отменен. Напишите /start, чтобы начать заново.")
    return MENU


async def ask_question_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text("Пожалуйста, введите ваш вопрос:")
    else:
        await update.message.reply_text("Пожалуйста, введите ваш вопрос:")
    return ASK_QUESTION


async def handle_user_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    await update.message.reply_text(f"Ваш вопрос: {user_question}\nСпасибо, мы его получили!")
    return MENU


def main() -> None:
    application = Application.builder().token(os.getenv("CLIENT_API_KEY")).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_question)]
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond_to_text))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    if data == "question":
        return ask_question_prompt(update, context)
    elif data == "help":
        query.answer()
        query.edit_message_text("Вы выбрали: Помощь")
    else:
        query.answer()
        query.edit_message_text(f"Неизвестная команда: {data}")
