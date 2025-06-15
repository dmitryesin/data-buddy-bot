import os
import json
import random
from pathlib import Path

from api_client import (
    get_user_settings,
    set_user_settings,
    set_user_question,
    ask_question,
    get_user_answers,
    get_user_questions,
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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

languages_path = PY_DIR / "languages.json"

with open(languages_path, "r", encoding="utf-8") as f:
    LANG_TEXTS = json.load(f)

MENU, ASK = range(2)

DEFAULT_LANGUAGE = "ru"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.edited_message:
        return MENU

    user_settings = await get_user_settings(
        update.effective_user.id,
        DEFAULT_LANGUAGE,
    )

    context.user_data["language"] = user_settings.get("language", DEFAULT_LANGUAGE)

    await set_user_settings(
        update.effective_user.id,
        context.user_data["language"],
    )

    current_language = context.user_data.get("language", DEFAULT_LANGUAGE)

    keyboard = [
        [
            InlineKeyboardButton(
                LANG_TEXTS[current_language]["ask"], callback_data="ask"
            ),
        ],
        [
            InlineKeyboardButton(
                LANG_TEXTS[current_language]["history"], callback_data="history"
            ),
        ],
        [
            InlineKeyboardButton(
                LANG_TEXTS[current_language]["settings"], callback_data="settings"
            ),
        ],
    ]

    texts = {}
    for lang_code in ["en", "ru"]:
        file_path = PY_DIR / "assets" / "texts" / f"START_{lang_code.upper()}.txt"
        with open(file_path, "r", encoding="utf-8") as file:
            texts[lang_code] = file.read()

    text_to_send = texts.get(current_language, texts["en"])

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


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    current_language = context.user_data.get("language", DEFAULT_LANGUAGE)

    keyboard = [
        [
            InlineKeyboardButton(
                LANG_TEXTS[current_language]["change_language"],
                callback_data="settings_language",
            )
        ],
        [
            InlineKeyboardButton(
                LANG_TEXTS[current_language]["back"], callback_data="back"
            )
        ],
    ]

    new_text = LANG_TEXTS[current_language]["settings_menu"]
    new_reply_markup = InlineKeyboardMarkup(keyboard)

    if query.message.text != new_text or query.message.reply_markup != new_reply_markup:
        await query.edit_message_text(new_text, reply_markup=new_reply_markup)

    return MENU


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    current_language = query.data
    context.user_data["language"] = current_language

    await set_user_settings(
        update.effective_user.id,
        context.user_data["language"],
    )

    await settings_language(update, context)


async def settings_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    current_language = context.user_data.get("language", DEFAULT_LANGUAGE)

    languages = [("en", "English"), ("ru", "Русский")]

    keyboard = []

    for language_callback, language in languages:
        text = f"→ {language} ←" if current_language == language_callback else language
        keyboard.append([InlineKeyboardButton(text, callback_data=language_callback)])

    keyboard.append(
        [
            InlineKeyboardButton(
                LANG_TEXTS[current_language]["back"], callback_data="settings_back"
            )
        ]
    )

    new_text = LANG_TEXTS[current_language]["settings_menu"]
    new_reply_markup = InlineKeyboardMarkup(keyboard)

    if query.message.text != new_text or query.message.reply_markup != new_reply_markup:
        await query.edit_message_text(new_text, reply_markup=new_reply_markup)

    return MENU


async def question_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    current_language = context.user_data.get("language", DEFAULT_LANGUAGE)
    recent_questions = await get_user_questions(update.effective_user.id)

    keyboard = []

    if not recent_questions:
        keyboard.append(
            [
                InlineKeyboardButton(
                    LANG_TEXTS[current_language]["back"], callback_data="back"
                )
            ]
        )

        await query.edit_message_text(
            LANG_TEXTS[current_language]["no_history"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return MENU

    for index, question in enumerate(recent_questions):
        question_text = question.get("question")
        display_text = (
            question_text if len(question_text) <= 50 else question_text[:47] + "..."
        )

        keyboard.append(
            [InlineKeyboardButton(display_text, callback_data=f"question_{index}")]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                LANG_TEXTS[current_language]["back"], callback_data="back"
            )
        ]
    )

    await query.edit_message_text(
        LANG_TEXTS[current_language]["history_menu"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    return MENU


async def question_history_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    current_language = context.user_data.get("language", DEFAULT_LANGUAGE)

    question_index = int(query.data.split("_")[1])

    recent_questions = await get_user_questions(update.effective_user.id)
    recent_answers = await get_user_answers(update.effective_user.id)

    if question_index >= len(recent_questions):
        await query.edit_message_text(
            LANG_TEXTS[current_language]["question_not_found"],
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            LANG_TEXTS[current_language]["back"],
                            callback_data="history",
                        )
                    ]
                ]
            ),
        )
        return MENU

    question = recent_questions[question_index]
    question_text = question.get("question", "")
    question_date = question.get("created_at", "")

    answer_text = ""
    if recent_answers and question_index < len(recent_answers):
        answer = recent_answers[question_index]
        answer_text = answer.get("answer", "")

    lang = LANG_TEXTS[current_language]
    details = [
        f"<b>{lang['question_question']}</b>{question_text}",
        f"<b>{lang['question_answer']}</b>{answer_text}",
    ]

    if question_date:
        date_part, time_part = question_date.split("T")
        details.append(f"<b>{lang['question_date']}</b>{date_part} {time_part[:8]}")

    details_text = "\n\n".join(details)

    keyboard = [
        [
            InlineKeyboardButton(
                LANG_TEXTS[current_language]["back"], callback_data="history"
            )
        ]
    ]

    await query.edit_message_text(
        details_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
    )

    return MENU


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    current_language = context.user_data.get("language", DEFAULT_LANGUAGE)

    text = LANG_TEXTS[current_language]["enter_question"]

    if update.message:
        await update.message.reply_text(text, parse_mode="HTML")
    else:
        query = update.callback_query
        await query.answer()
        if query.message and query.message.text:
            await query.edit_message_text(text, parse_mode="HTML")
        else:
            await query.message.reply_text(text, parse_mode="HTML")

    return ASK


async def process_ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["user_question"] = update.message.text

    await set_user_question(update.effective_user.id, update.message.text)

    current_language = context.user_data.get("language", DEFAULT_LANGUAGE)

    processing_key = f"answering{random.randint(1, 4)}"
    processing_message = await update.message.reply_text(
        LANG_TEXTS[current_language][processing_key]
    )

    keyboard = [
        [
            InlineKeyboardButton(
                LANG_TEXTS[current_language]["ask_over"], callback_data="ask"
            )
        ],
        [
            InlineKeyboardButton(
                LANG_TEXTS[current_language]["menu"], callback_data="menu"
            )
        ],
    ]

    new_reply_markup = InlineKeyboardMarkup(keyboard)
    question = update.message.text
    answer = await ask_question(update.effective_user.id, question, current_language)

    await processing_message.edit_text(
        answer, reply_markup=new_reply_markup, parse_mode="HTML"
    )

    return MENU


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_language = context.user_data.get("language", DEFAULT_LANGUAGE)

    keyboard = [
        [
            InlineKeyboardButton(
                LANG_TEXTS[current_language]["menu"], callback_data="menu"
            )
        ]
    ]

    new_reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        LANG_TEXTS[current_language]["cancel"], reply_markup=new_reply_markup
    )
    return MENU


def main() -> None:
    application = Application.builder().token(os.getenv("CLIENT_API_KEY")).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [
                CallbackQueryHandler(start, pattern="^back$"),
                CallbackQueryHandler(start, pattern="^menu$"),
                CallbackQueryHandler(settings, pattern="^settings$"),
                CallbackQueryHandler(settings, pattern="^settings_back$"),
                CallbackQueryHandler(settings_language, pattern="^settings_language$"),
                CallbackQueryHandler(ask, pattern="^ask$"),
                CallbackQueryHandler(language, pattern="^(en|ru)$"),
                CallbackQueryHandler(question_history, pattern="^history$"),
                CallbackQueryHandler(
                    question_history_details, pattern=r"^question_\d+$"
                ),
            ],
            ASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_ask)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
        per_message=False,
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
