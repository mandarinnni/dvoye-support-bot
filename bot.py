from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import os
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 295824298
user_messages = {}
admin_reply_mode = {}

from flask import Flask
import threading
import os

app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)


# --- Старт и приветствие ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    keyboard = [
        [InlineKeyboardButton("📚 Курсы и обучение", callback_data="courses")],
        [InlineKeyboardButton("💳 Оплата и возврат", callback_data="payment")],
        [InlineKeyboardButton("🛠 Технические вопросы", callback_data="tech")],
        [InlineKeyboardButton("🧠 Консультации психологов", callback_data="psych")],
        [InlineKeyboardButton("📢 Telegram и материалы", callback_data="tg")],
        [InlineKeyboardButton("✉️ Другое", callback_data="other")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "Здравствуйте.\n"
        "Это служба поддержки проекта «Двое».\n\n"
        "Выберите подходящую категорию вопроса или нажмите «Другое», "
        "чтобы описать ситуацию."
    )

    if user_id in user_messages:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=user_messages[user_id],
            text=text,
            reply_markup=reply_markup
        )
    else:
        msg = await update.message.reply_text(text, reply_markup=reply_markup)
        user_messages[user_id] = msg.message_id




# --- Обработчик кнопок ---
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    

    # --- НАЗАД В ГЛАВНОЕ МЕНЮ ---
    if query.data == "back":
        await start(update, context)

    # =========================
    # 1️⃣ КУРСЫ
    # =========================
    elif query.data == "courses":
        await query.edit_message_text(
            "🎓 Курсы и обучение\n\nВыберите вариант:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔹 Не пришёл доступ", callback_data="course_no_access")],
                [InlineKeyboardButton("🔹 Где найти курс", callback_data="course_where")],
                [InlineKeyboardButton("🔹 Зарегистрировался, но нет доступа", callback_data="course_registered")],
                [InlineKeyboardButton("✉️ Написать оператору", callback_data="operator")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
            ])
        )

    elif query.data == "course_no_access":
        await query.edit_message_text(
            "Доступ к курсам приходит автоматически на почту, указанную при регистрации на GetCourse.\n\n"
            "Пожалуйста, проверьте папки «Спам» и «Промоакции».\n\n"
            "Если письма нет, попробуйте войти в личный кабинет GetCourse по кнопке «Войти» на странице курса, используя ту же почту.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="courses")]])
        )

    elif query.data == "course_where":
        await query.edit_message_text(
            "Все ваши курсы (включая бесплатные мини-курсы) находятся в личном кабинете GetCourse.\n\n"
            "Войти можно по ссылке, которая приходила вам на почту после регистрации.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="courses")]])
        )

    elif query.data == "course_registered":
        await query.edit_message_text(
            "После регистрации на бесплатный курс доступ открывается сразу или в дату старта, если она указана.\n\n"
            "Проверьте письмо с подтверждением регистрации — в нём есть ссылка на вход.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="courses")]])
        )
        

    # =========================
    # 2️⃣ ОПЛАТА
    # =========================
    elif query.data == "payment":
        await query.edit_message_text(
            "💳 Оплата и возврат\n\nВыберите вариант:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔹 Не проходит оплата", callback_data="pay_error")],
                [InlineKeyboardButton("🔹 Оплатил(а), но нет доступа", callback_data="pay_no_access")],
                [InlineKeyboardButton("🔹 Вопрос по возврату", callback_data="refund")],
                [InlineKeyboardButton("✉️ Написать оператору", callback_data="operator")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
            ])
        )

    elif query.data == "pay_error":
        await query.edit_message_text(
            "Если оплата не проходит, попробуйте:\n"
            "– обновить страницу\n"
            "– использовать другой браузер или устройство\n"
            "– проверить лимиты карты\n\n"
            "Иногда помогает повторить попытку через несколько минут.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="payment")]])
        )

    elif query.data == "pay_no_access":
        await query.edit_message_text(
            "В большинстве случаев доступ открывается автоматически в течение нескольких минут.\n\n"
            "Пожалуйста, проверьте почту и личный кабинет GetCourse.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="payment")]])
        )

    elif query.data == "refund":
        await query.edit_message_text(
            "Условия возврата зависят от конкретного курса и указаны на странице продукта.\n\n"
            "Если вы не нашли нужную информацию, пожалуйста, опишите ситуацию — мы передадим запрос оператору.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="payment")]])
        )

    # =========================
    # 3️⃣ ТЕХНИЧЕСКИЕ
    # =========================
    elif query.data == "tech":
        await query.edit_message_text(
            "🛠 Технические вопросы\n\nВыберите вариант:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔹 Не открываются видео/материалы", callback_data="tech_video")],
                [InlineKeyboardButton("🔹 Ошибка входа в аккаунт", callback_data="tech_login")],
                [InlineKeyboardButton("✉️ Написать оператору", callback_data="operator")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
            ])
        )

    elif query.data == "tech_video":
        await query.edit_message_text(
            "Чаще всего проблема решается:\n"
            "– обновлением страницы\n"
            "– сменой браузера\n"
            "– проверкой интернет-соединения\n\n"
            "Рекомендуем использовать актуальную версию Chrome или Safari.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="tech")]])
        )

    elif query.data == "tech_login":
        await query.edit_message_text(
            "Проверьте, что вы используете ту же почту, с которой регистрировались на GetCourse.\n\n"
            "Если пароль не подходит, воспользуйтесь функцией восстановления пароля.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="tech")]])
        )

    # =========================
    # 4️⃣ ПСИХОЛОГИ
    # =========================
    elif query.data == "psych":
        await query.edit_message_text(
            "🧠 Консультации психологов\n\nВыберите вариант:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔹 Как записаться на консультацию", callback_data="psych_book")],
                [InlineKeyboardButton("🔹 Вопрос по психологу", callback_data="psych_question")],
                [InlineKeyboardButton("🔹 Перенос / отмена консультации", callback_data="psych_move")],
                [InlineKeyboardButton("✉️ Написать оператору", callback_data="operator")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
            ])
        )

    elif query.data == "psych_book":
        await query.edit_message_text(
            "Запись на консультацию происходит через каталог психологов на нашем сайте.\n\n"
            "Вы можете выбрать специалиста и оставить заявку напрямую.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="psych")]])
        )

    elif query.data == "psych_question":
        await query.edit_message_text(
            "Вся актуальная информация о специалистах указана в их карточках в каталоге.\n\n"
            "Если у вас остался вопрос — напишите подробнее через кнопку «Другое».",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="psych")]])
        )

    elif query.data == "psych_move":
        await query.edit_message_text(
            "Вопросы переноса или отмены консультации решаются напрямую с выбранным специалистом в личном кабинете записи.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="psych")]])
        )

    # =========================
    # 5️⃣ TELEGRAM
    # =========================
    elif query.data == "tg":
        await query.edit_message_text(
            "📢 Telegram-канал и материалы\n\nВыберите вариант:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔹 Где найти практики", callback_data="tg_where")],
                [InlineKeyboardButton("🔹 Не могу найти пост/упражнение", callback_data="tg_find")],
                [InlineKeyboardButton("✉️ Написать оператору", callback_data="operator")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
            ])
        )

    elif query.data == "tg_where":
        await query.edit_message_text(
            "Бесплатные упражнения и материалы публикуются в нашем Telegram-канале проекта «Двое».\n\n"
            "https://t.me/dvoe_life",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="tg")]])
        )

    elif query.data == "tg_find":
        await query.edit_message_text(
            "Попробуйте воспользоваться поиском по каналу по ключевым словам.\n\n"
            "Если не получается — напишите, что именно вы ищете через кнопку «Другое».",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="tg")]])
        )

    elif query.data == "other":
        await query.edit_message_text(
            "Пожалуйста, опишите ваш вопрос.\n\n"
            "Мы передадим его оператору.\n"
            "Ответ может занять некоторое время — благодарим за понимание."
        )
        
    elif query.data == "operator":
       await query.edit_message_text(
        "Пожалуйста, опишите ваш вопрос.\n\n"
        "Мы передадим его оператору.\n"
        "Ответ может занять некоторое время — благодарим за понимание."
    )


from telegram.ext import MessageHandler, filters

# --- Пересылка сообщений админу ---
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if update.message and update.message.text:
        text = update.message.text

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✏️ Ответить", callback_data=f"reply_{user.id}")]
        ])

        message_to_admin = (
            f"📩 Новый запрос поддержки\n\n"
            f"👤 Пользователь: {user.full_name}\n"
            f"🆔 ID: {user.id}\n\n"
            f"Сообщение:\n{text}"
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=message_to_admin,
            reply_markup=keyboard
        )

        await update.message.reply_text(
            "Спасибо. Ваше сообщение передано оператору."
        )

        context.user_data["waiting_for_message"] = False

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        message = " ".join(context.args[1:])

        await context.bot.send_message(chat_id=user_id, text=message)
        await update.message.reply_text("Ответ отправлен пользователю.")

    except (IndexError, ValueError):
        await update.message.reply_text(
            "Используйте формат:\n/reply USER_ID текст сообщения"
        )

# --- Нажатие кнопки "Ответить" ---
async def admin_reply_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if update.effective_user.id != ADMIN_ID:
        return

    user_id = int(query.data.split("_")[1])
    admin_reply_mode[ADMIN_ID] = user_id

    await query.message.reply_text(
        f"Введите сообщение для пользователя {user_id}:"
    )

# --- Универсальный обработчик сообщений ---
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Если это админ и он в режиме ответа
    if user_id == ADMIN_ID and user_id in admin_reply_mode:
        target_user_id = admin_reply_mode[user_id]

        await context.bot.send_message(
            chat_id=target_user_id,
            text=update.message.text
        )

        await update.message.reply_text("Ответ отправлен пользователю.")

        del admin_reply_mode[user_id]
        return

    # Если это обычный пользователь
    await forward_to_admin(update, context)


# --- Запуск приложения ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(admin_reply_button, pattern="^reply_"))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("Бот запущен")

    threading.Thread(target=run_web).start()

    app.run_polling()



if __name__ == "__main__":
    main()

