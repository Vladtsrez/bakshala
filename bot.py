import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "8892137618:AAF5j5Fgl2tn19R5ntEXMIZTMFTSni7LnUc")
BOOKING_USERNAME = "@brdkAN"

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

WELCOME_TEXT = (
    "\U0001f3d5 *Ласкаво просимо до Ранчо Бакшала!*\n\n"
    "Ми раді вітати вас у нашому затишному куточку природи.\n"
    "Тут ви знайдете відпочинок для душі та тіла — риболовля, "
    "комфортне проживання та незабутні вечори в альтанці.\n\n"
    "Оберіть розділ нижче \U0001f447"
)

FISHING_TEXT = (
    "\U0001f3a3 *Риболовля — Умови та Правила*\n\n"
    "\U0001f420 *Що є на ставку:*\n"
    "• Короп, карась, щука, окунь\n"
    "• Ставок площею ~2 га, глибина до 4 м\n\n"
    "\U0001f4cb *Правила:*\n"
    "• Риболовля дозволена з 5:00 до 22:00\n"
    "• Дозволено не більше 2 вудок на особу\n"
    "• Принцип «Спіймав — відпустив» вітається\n"
    "• Вивіз риби — до 5 кг на особу на добу\n"
    "• Забороняється ловля сітками та електровудками\n\n"
    "\U0001f4b0 *Вартість:*\n"
    "• День (5:00-22:00) — 200 грн / особа\n"
    "• Ніч (22:00-5:00) — 150 грн / особа\n"
    "• Добова — 300 грн / особа\n\n"
    "Рибальське спорядження можна взяти в оренду на місці.\n\n"
    "Питання? Пишіть -> @brdkAN"
)

HOUSE_TEXT = (
    "\U0001f3e1 *Будинок — Умови Проживання*\n\n"
    "\U0001f6cf *Що включено:*\n"
    "• 3 спальні (до 6 осіб)\n"
    "• Повністю обладнана кухня\n"
    "• Гаряча вода, душ, санвузол\n"
    "• Wi-Fi, телевізор\n"
    "• Мангал та зона барбекю\n"
    "• Парковка на території\n\n"
    "\U0001f4cb *Правила:*\n"
    "• Заселення з 14:00, виселення до 12:00\n"
    "• Тварини — за попереднім погодженням\n"
    "• Не палити всередині будинку\n"
    "• Підтримуйте чистоту\n\n"
    "\U0001f4b0 *Вартість:*\n"
    "• Будні (Пн-Чт) — 1500 грн / ніч\n"
    "• Вихідні (Пт-Нд) — 2000 грн / ніч\n"
    "• Свята — за запитом\n\n"
    "Постільна білизна та рушники включені.\n\n"
    "Питання? Пишіть -> @brdkAN"
)

GAZEBO_TEXT = (
    "\U0001f333 *Альтанка — Умови Оренди*\n\n"
    "\U0001f3d5 *Опис:*\n"
    "• Простора альтанка на 12-15 осіб\n"
    "• Розташована біля ставка з чудовим краєвидом\n"
    "• Вбудований мангал та стіл зі лавками\n"
    "• Вечірнє освітлення\n"
    "• Розетки для зарядки\n\n"
    "\U0001f4cb *Правила:*\n"
    "• Оренда з 10:00 до 22:00\n"
    "• Прибирання після себе обов'язкове\n"
    "• Гучна музика — до 21:00\n"
    "• Власні напої та їжа — дозволені\n\n"
    "\U0001f4b0 *Вартість:*\n"
    "• До 4 годин — 500 грн\n"
    "• Повний день — 900 грн\n"
    "• Вечірня оренда (17:00-22:00) — 600 грн\n\n"
    "Дрова для мангалу надаються безкоштовно!\n\n"
    "Питання? Пишіть -> @brdkAN"
)


def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("\U0001f3a3 Риболовля", callback_data="fishing")],
        [InlineKeyboardButton("\U0001f3e1 Будинок",   callback_data="house")],
        [InlineKeyboardButton("\U0001f333 Альтанка",  callback_data="gazebo")],
        [InlineKeyboardButton("\U0001f4c5 Забронювати", url="https://t.me/brdkAN")],
    ])


def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("\u2b05 Назад до меню", callback_data="back")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    handlers = {
        "fishing": (FISHING_TEXT, back_keyboard()),
        "house":   (HOUSE_TEXT,   back_keyboard()),
        "gazebo":  (GAZEBO_TEXT,  back_keyboard()),
        "back":    (WELCOME_TEXT, main_menu_keyboard()),
    }

    if query.data in handlers:
        text, keyboard = handlers[query.data]
        await query.edit_message_text(
            text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Bot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
