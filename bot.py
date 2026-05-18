import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "8892137618:AAF5j5Fgl2tn19R5ntEXMIZTMFTSni7LnUc")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── ТЕКСТИ ───────────────────────────────────────────────────────────────────

WELCOME_TEXT = (
    "\U0001f3d5 *Ласкаво просимо до Ранчо \u00abБакшала\u00bb!*\n\n"
    "Затишний куточок природи для відпочинку, риболовлі та незабутніх вечорів.\n\n"
    "Оберіть розділ нижче \U0001f447"
)

FISHING_TEXT = (
    "\U0001f3a3 *Риболовля*\n\n"
    "\U0001f4cc *Умови:*\n"
    "• Пірс на 2 особи — до 2 вудок на кожного\n"
    "• Дозволено забрати 2 риби загальною вагою до 10 кг\n"
    "• Додатковий вилов — узгоджується окремо\n"
    "• Заборонені методи лову — заборонено\n\n"
    "\U0001f6d2 *Оренда спорядження:*\n"
    "• На місці можна взяти вудки та придбати монтажі, наживку, корм, прикормку\n"
    "• Оформлення — за паспортом/документом та анкетою\n\n"
    "\U0001f41f *Хочете приготувати рибу?*\n"
    "Обов'язково попередьте адміністрацію або консультанта з риболовлі!\n\n"
    "\u260e\ufe0f *Бронювання:* +380 77 073 73 00"
)

HOUSE_TEXT = (
    "\U0001f3e1 *Будиночки — Умови проживання*\n\n"
    "\U0001f551 *Час заїзду/виїзду:*\n"
    "• Заїзд — з 15:00\n"
    "• Виїзд — до 11:00\n"
    "• Ранній/пізній заїзд — лише за попередньою домовленістю\n\n"
    "\U0001f4cb *Головні правила:*\n"
    "• Дбайливо ставтесь до майна — при пошкодженні відшкодування 100%\n"
    "• Куріння — лише у спеціально відведених місцях\n"
    "• Діти та тварини — лише під наглядом\n"
    "• Перед виїздом: зачиніть двері, перекрийте крани, вимкніть світло\n"
    "• Тиша з 23:00 до 08:00\n\n"
    "\U0001f6ab *Заборонено:*\n"
    "• Куріння в будинку (штраф 2500 грн)\n"
    "• Незареєстровані гості (штраф 50% вартості)\n"
    "• Тварини без погодження (штраф 2500 грн)\n"
    "• Феєрверки та салюти (штраф 5000 грн)\n"
    "• Наркотичні/заборонені речовини та зброя\n\n"
    "\U0001f43e *Тварини:*\n"
    "Дозволені за погодженням з адміністрацією. Потрібні: паспорт тварини + довідка від ветеринара.\n\n"
    "\U0001f4b0 *Знижки:*\n"
    "• 2+ доби — знижка 5%\n"
    "• Військовим — знижка 10%\n\n"
    "\u260e\ufe0f *Бронювання:* +380 77 073 73 00"
)

GAZEBO_TEXT = (
    "\U0001f333 *Альтанки — Умови оренди*\n\n"
    "\U0001f551 *Час:*\n"
    "• Заїзд — з 12:00\n"
    "• Виїзд — до 23:00\n\n"
    "\U0001f4cb *Головні правила:*\n"
    "• Після відпочинку залишити альтанку в охайному стані\n"
    "• Сміття — у спеціальні контейнери\n"
    "• Куріння — лише у спеціально відведених місцях\n"
    "• Тиша з 23:00 до 08:00 (штраф 1000 грн)\n\n"
    "\U0001f6ab *Заборонено:*\n"
    "• Свічки та недопалки на території\n"
    "• Стрибати у ставок, бігати та штовхатись біля води\n"
    "• Скляний посуд біля води\n"
    "• Вживати їжу/напої безпосередньо біля води\n"
    "• Гучні вечірки без погодження з адміністрацією\n"
    "• Феєрверки та салюти (штраф 5000 грн)\n\n"
    "\U0001f38a *Святкування:*\n"
    "Весілля або день народження — лише за погодженням з адміністрацією.\n\n"
    "\u260e\ufe0f *Бронювання:* +380 77 073 73 00"
)

BOOKING_TEXT = (
    "\U0001f4c5 *Бронювання*\n\n"
    "\U0001f4de Телефон / Telegram / Instagram:\n"
    "+380 77 073 73 00\n\n"
    "\U0001f4b3 *Умови:*\n"
    "• Підтвердження — після передоплати 50%\n"
    "• Оформлення — за паспортом/документом\n\n"
    "\U0001f519 *Повернення передоплати:*\n"
    "• Скасування менш ніж за 7 днів до заїзду — передоплата не повертається\n"
    "• Незаїзд у день заїзду — передоплата не повертається\n\n"
    "\u26a1 *Електрика:*\n"
    "При відключенні світла працюють генератори — електрика є завжди.\n\n"
    "\U0001f4cd *Написати в Telegram:* @brdkAN"
)

FALLBACK_TEXT = (
    "\U0001f44b Натисніть кнопку нижче, щоб розпочати!\n\n"
    "Або введіть команду /start"
)


# ─── КЛАВІАТУРИ ───────────────────────────────────────────────────────────────

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("\U0001f3a3 Риболовля",   callback_data="fishing")],
        [InlineKeyboardButton("\U0001f3e1 Будиночки",   callback_data="house")],
        [InlineKeyboardButton("\U0001f333 Альтанки",    callback_data="gazebo")],
        [InlineKeyboardButton("\U0001f4c5 Забронювати", callback_data="booking")],
    ])


def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("\u2b05 Назад до меню", callback_data="back")]
    ])


def booking_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("\U0001f4ac Написати адміністратору", url="https://t.me/brdkAN")],
        [InlineKeyboardButton("\u2b05 Назад до меню", callback_data="back")],
    ])


def start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("\U0001f680 Розпочати", callback_data="back")]
    ])


# ─── ХЕНДЛЕРИ ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )


async def fallback_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        FALLBACK_TEXT,
        reply_markup=start_keyboard(),
        parse_mode="Markdown"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    handlers = {
        "fishing": (FISHING_TEXT,  back_keyboard()),
        "house":   (HOUSE_TEXT,    back_keyboard()),
        "gazebo":  (GAZEBO_TEXT,   back_keyboard()),
        "booking": (BOOKING_TEXT,  booking_keyboard()),
        "back":    (WELCOME_TEXT,  main_menu_keyboard()),
    }

    if query.data in handlers:
        text, keyboard = handlers[query.data]
        await query.edit_message_text(
            text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )


# ─── ЗАПУСК ───────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.ALL, fallback_message))
    logger.info("Rancho Bakshala bot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
