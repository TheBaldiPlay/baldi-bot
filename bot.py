import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramAPIError

API_TOKEN = "8014951920:AAHXOjFxLttlKVUEd80pJtmTh9uWRGZyL4A"
ADMIN_ID = 8993340328  # Твой ID Директора Балди

logging.basicConfig(level=logging.INFO)
router = Router()

# Словари для защиты от спама
active_appeals = set()
shadow_banned = set()

class AppealForm(StatesGroup):
    waiting_for_id = State()
    waiting_for_appeal = State()

# Главное меню бота со всеми кнопками
def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Подать апелляцию", callback_data="start_appeal")],
        [InlineKeyboardButton(text="📚 База знаний (FAQ)", callback_data="knowledge_base")],
        [InlineKeyboardButton(text="🌐 Наши соцсети", callback_data="social_links")],
        [InlineKeyboardButton(text="📜 Правила использования бота", callback_data="bot_rules")],
        [InlineKeyboardButton(text="👤 Профиль бота", callback_data="bot_profile")]
    ])

# Кнопка возврата в базу знаний
def kb_back_faq():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад к базе знаний", callback_data="knowledge_base")]])

# Кнопка возврата в главное меню
def kb_back_main():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]])


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()

    if user_id in shadow_banned:
        await message.answer("🚫 Вы получили теневой бан на 7 дней за спам апелляциями! Директор Балди закрыл перед вами дверь. 📐💥")
        return

    await message.answer(
        "🔔 Добро пожаловать в официальный центр поддержки **Baldi Office**! 🏫\n\n"
        "Здесь вы можете подать жалобу на бан, изучить базу знаний, узнать правила или найти наши соцсети. Выберите нужный пункт меню ниже 👇",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )


# Главное меню базы знаний (список разделов)
@router.callback_query(F.data == "knowledge_base")
async def process_faq(callback: CallbackQuery):
    await callback.answer()
    faq_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Как определить рейджбайтера", callback_data="faq_ragebait")],
        [InlineKeyboardButton(text="💨 Кто такой воздухан?", callback_data="faq_airhead")],
        [InlineKeyboardButton(text="👶 Что делать, если обзывают школотой?", callback_data="faq_shkolota")],
        [InlineKeyboardButton(text="💻 Миф о сносах через Termux", callback_data="faq_termux_myth")],
        [InlineKeyboardButton(text="🕵️‍♂️ Что такое доксинг?", callback_data="faq_doxing")],
        [InlineKeyboardButton(text="🚀 Почему доксинг в 2026 не страшен?", callback_data="faq_doxing_2026")],
        [InlineKeyboardButton(text="🔒 Кибербезопасность", callback_data="faq_security")],
        [InlineKeyboardButton(text="📝 Как подать апелляцию", callback_data="faq_appeal_tips")],
        [InlineKeyboardButton(text="🌐 Интернет-этикет", callback_data="faq_etiquette")],
        [InlineKeyboardButton(text="❓ Общие вопросы по банам", callback_data="faq_general")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
    ])
    await callback.message.edit_text(
        "📚 **Энциклопедия Baldi Office (База знаний):**\n\n"
        "Выбирай любой раздел ниже, чтобы прокачать интернет-грамотность и не вестись на сказки! 👇",
        reply_markup=faq_keyboard,
        parse_mode="Markdown"
    )


# --- РАЗДЕЛЫ БАЗЫ ЗНАНИЙ ---

@router.callback_query(F.data == "faq_ragebait")
async def faq_ragebait_handler(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(
        "🔥 **Раздел: Как определить рейджбайтера?**\n\n"
        "Рейджбайтер — это человек, который специально пишет провокации и дичь исключительно ради того, чтобы вывести тебя из себя и заставить писать агрессивный ответ.\n\n"
        "🔎 **Признаки рейджбайтера:**\n"
        "1. Пишет абсурдное мнение, с которым никто не согласится.\n"
        "2. Игнорирует логику и переходит на личности.\n"
        "3. Питается твоими эмоциями.\n\n"
        "💡 *Совет:* Просто проигнорируй его, и он потеряет интерес.",
        reply_markup=kb_back_faq(), parse_mode="Markdown"
    )

@router.callback_query(F.data == "faq_airhead")
async def faq_airhead_handler(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(
        "💨 **Раздел: Кто такой воздухан?**\n\n"
        "Воздухан — это персонаж, который на словах «крутой хакер и босс всего интернета», а на деле придумывает аргументы на ходу и не может подтвердить свои слова фактами.\n\n"
        "🔎 **Признаки воздухана:**\n"
        "1. Громкие заявления без пруфов.\n"
        "2. Ссылки на опыт вроде «я в кибербезопасности с пеленок».\n"
        "3. Уход от темы при появлении фактов.",
        reply_markup=kb_back_faq(), parse_mode="Markdown"
    )

@router.callback_query(F.data == "faq_shkolota")
async def faq_shkolota_handler(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(
        "👶 **Раздел: Что делать, если обзывают «школотой»?**\n\n"
        "Это самый дешевый способ задеть человека. Главное правило: **НИКАКИХ ОПРАВДАНИЙ!**\n\n"
        "❌ **Список худших оправданий (никогда не пиши это!):**\n"
        "• «Мне вообще-то уже 14/16 лет!»\n"
        "• «Я учусь на одни пятёрки!»\n"
        "• «Я школу закончил 10 лет назад!»\n"
        "• «Я совершеннолетний!»\n"
        "• «Я работаю, в отличие от тебя!»\n"
        "• «Я учусь в институте / колледже!»\n\n"
        "Как только ты написал оправдание — ты проиграл. Уверенность и молчание — твой лучший щит.",
        reply_markup=kb_back_faq(), parse_mode="Markdown"
    )

@router.callback_query(F.data == "faq_termux_myth")
async def faq_termux_myth_handler(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(
        "💻 **Раздел: Миф о «сносах аккаунтов через Termux»**\n\n"
        "Среди школьных хакеров популярен миф, что можно скачать скрипт в Termux и снести чей-то аккаунт. Это полная чушь!\n\n"
        "🛡️ **Почему это не работает:**\n"
        "1. Архитектура Telegram неуязвима для скриптов с телефона.\n"
        "2. В 99% паблик-скриптов вшит стиллер, который ворует твои же сессии (в итоге сносят не жертву, а тебя).\n"
        "3. Спам-жалобы с авторегов алгоритмы Telegram мгновенно игнорируют.\n"
        "4. За реальные уязвимости платят миллионы профессионалам, а не создателям скриптов за 10 рублей.",
        reply_markup=kb_back_faq(), parse_mode="Markdown"
    )

@router.callback_query(F.data == "faq_doxing")
async def faq_doxing_handler(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(
        "🕵️‍♂️ **Раздел: Что делать, если тебя задоксили?**\n\n"
        "**Доксинг** — это сбор и публикация личной информации без согласия.\n\n"
        "🚨 **План действий:**\n"
        "1. Абсолютное спокойствие. Цель доксера — вызвать панику.\n"
        "2. Ни в коем случае не плати выкуп и не ведись на шантаж.\n"
        "3. Сделай скриншоты угроз.\n"
        "4. Пожалуйся на каналы/чаты, где слиты данные.\n"
        "5. Расскажи родителям или взрослым.",
        reply_markup=kb_back_faq(), parse_mode="Markdown"
    )

@router.callback_query(F.data == "faq_doxing_2026")
async def faq_doxing_2026_handler(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(
        "🚀 **Раздел: Почему доксинг в 2026 году — это пустой звук?**\n\n"
        "В реалиях 2026 года классический «доксинг» из подростковых пабликов потерял актуальность:\n"
        "1. Информация базового уровня (город, имя) дает ровным счетом ничего.\n"
        "2. Мессенджеры и соцсети имеют мощные настройки приватности.\n"
        "3. За кибербуллинг и слив данных теперь есть реальная ответственность.\n"
        "4. Общество выработало иммунитет к этим угрозам.",
        reply_markup=kb_back_faq(), parse_mode="Markdown"
    )

@router.callback_query(F.data == "faq_security")
async def faq_security_handler(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(
        "🔒 **Кибербезопасность:**\n\n"
        "Полностью защититься от утечек невозможно, но можно затруднить поиск данных:\n"
        "1. Используй сложные и разные пароли.\n"
        "2. Включи двухфакторную аутентификацию (2FA).\n"
        "3. Никому не сообщай коды из СМС и Telegram.\n"
        "4. Не переходи по подозрительным ссылкам.",
        reply_markup=kb_back_faq(), parse_mode="Markdown"
    )

@router.callback_query(F.data == "faq_appeal_tips")
async def faq_appeal_tips_handler(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(
        "📝 **Как правильно подать апелляцию:**\n\n"
        "1. Будь честным и признай вину.\n"
        "2. Пиши без мата и агрессии.\n"
        "3. Излагай суть кратко и по делу.\n"
        "Чистосердечное признание повышает шанс на разбан!",
        reply_markup=kb_back_faq(), parse_mode="Markdown"
    )

@router.callback_query(F.data == "faq_etiquette")
async def faq_etiquette_handler(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(
        "🌐 **Интернет-этикет:**\n\n"
        "1. Не вейся на бесплатные обещания и скам.\n"
        "2. Думай, прежде чем писать — интернет хранит всё.\n"
        "3. Уважай чужие границы.",
        reply_markup=kb_back_faq(), parse_mode="Markdown"
    )

@router.callback_query(F.data == "faq_general")
async def faq_general_handler(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(
        "❓ **Общие вопросы:**\n\n"
        "1. Бан выдается за нарушение правил чата.\n"
        "2. Апелляция рассматривается до 24 часов.\n"
        "3. Спам заявками карается теневым баном на 7 дней.",
        reply_markup=kb_back_faq(), parse_mode="Markdown"
    )


# --- СОЦСЕТИ И ПРОФИЛЬ ---

@router.callback_query(F.data == "social_links")
async def process_socials(callback: CallbackQuery):
    await callback.answer()
    social_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Discord", url="https://discord.gg/jqUjMQfAGB")],
        [InlineKeyboardButton(text="📺 YouTube", url="https://youtube.com/@TheBaldiPlay2010")],
        [InlineKeyboardButton(text="✖️ X (Twitter)", url="https://x.com/TheBaldiPlay716")],
        [InlineKeyboardButton(text="📸 Instagram", url="https://www.instagram.com/thebaldiplay981")],
        [InlineKeyboardButton(text="🎵 TikTok", url="https://www.tiktok.com/@thebaldiplay71")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
    ])
    await callback.message.edit_text(
        "🌐 **Наши официальные ресурсы и соцсети:**\n\n"
        "Следи за контентом и обновлениями на всех площадках! Выбирай удобную ниже 👇",
        reply_markup=social_keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "bot_rules")
async def process_bot_rules(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📜 **Правила использования бота Baldi Office:**\n\n"
        "1. **Одна апелляция** — подавать жалобу можно строго один раз.\n"
        "2. **Только свой ID** — попытка обмана сбрасывает заявку.\n"
        "3. **Адекватность** — мат и оскорбления гарантируют отказ.\n"
        "4. **Уважение к администрации** — не отвлекай по пустякам.",
        reply_markup=kb_back_main(), parse_mode="Markdown"
    )

@router.callback_query(F.data == "bot_profile")
async def process_bot_profile(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🤖 **Профиль системы: Baldi Office v2.0**\n\n"
        "🏫 **Учреждение:** Официальная Школа Поддержки\n"
        "⚡ **Статус хостинга:** 24/7 Cloud Active\n"
        "🛡️ **Система защиты:** Активна\n"
        "📚 **База знаний:** 10+ разделов энциклопедии",
        reply_markup=kb_back_main(), parse_mode="Markdown"
    )

@router.callback_query(F.data == "back_to_main")
async def process_back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🔔 Главное меню **Baldi Office**! Выберите нужный раздел 👇",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )


# --- СИСТЕМА АПЕЛЛЯЦИЙ И АДМИНКА ---

@router.callback_query(F.data == "start_appeal")
async def process_start_appeal(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if user_id in active_appeals or user_id in shadow_banned:
        await callback.answer("Ошибка: повторная подача запрещена!", show_alert=True)
        return

    await callback.answer()
    await state.set_state(AppealForm.waiting_for_id)
    back_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Отмена", callback_data="back_to_main")]])
    await callback.message.edit_text("🆔 **Шаг 1:** Введите ваш цифровой Telegram ID:", reply_markup=back_kb, parse_mode="Markdown")

@router.message(StateFilter(AppealForm.waiting_for_id))
async def process_id(message: Message, state: FSMContext):
    if message.text.strip() != str(message.from_user.id):
        await state.clear()
        await message.answer("❌ ВНИМАНИЕ! Попытка обмана! Вы ввели чужой Telegram ID!")
        return

    await state.update_data(user_id=message.from_user.id)
    await state.set_state(AppealForm.waiting_for_appeal)
    await message.answer("✍️ ID подтвержден! Отправьте текст вашей апелляции (шанс всего один):")

@router.message(StateFilter(AppealForm.waiting_for_appeal))
async def process_appeal_text(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    
    if user_id in active_appeals:
        await state.clear()
        await message.answer("⚠️ Ваша апелляция уже была отправлена ранее!")
        return

    appeal_text = message.text
    await state.clear()
    active_appeals.add(user_id)

    loading_msg = await message.answer("⏳ Отправка бланка Директору... 0%")
    for percent in [25, 50, 75, 100]:
        await asyncio.sleep(0.3)
        try:
            await loading_msg.edit_text(f"⏳ Отправка бланка Директору... {percent}%")
        except TelegramAPIError:
            pass

    await loading_msg.edit_text("✅ Бланк успешно отправлен Директору Балди! Ожидайте вердикта.")

    admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Одобрить (Разбан)", callback_data=f"approve_{user_id}")],
        [InlineKeyboardButton(text="🔴 Отклонить", callback_data=f"reject_{user_id}")]
    ])

    report_text = (
        f"🚨 НОВАЯ АПЕЛЛЯЦИЯ В BALDI OFFICE! 🚨\n"
        f"📊 Telegram ID: `{user_id}`\n"
        f"📝 ТЕКСТ:\n\"{appeal_text}\"\n\n"
        f"Какой вердикт, господин Директор? 👨‍🦲👇"
    )

    try:
        await bot.send_message(chat_id=ADMIN_ID, text=report_text, reply_markup=admin_keyboard, parse_mode="Markdown")
    except TelegramAPIError as e:
        logging.error(f"Ошибка отправки админу: {e}")

@router.callback_query(F.data.startswith("approve_") | F.data.startswith("reject_"))
async def process_admin_verdict(callback: CallbackQuery, bot: Bot):
    action, user_id_str = callback.data.split("_")
    target_user_id = int(user_id_str)
    original_text = callback.message.text
    
    if target_user_id in active_appeals:
        active_appeals.remove(target_user_id)

    try:
        if action == "approve":
            await bot.send_message(chat_id=target_user_id, text="🟢 Апелляция одобрена! Директор Балди дал тебе второй шанс. 🤝📐")
            new_text = original_text + "\n\n✅ ВЕРДИКТ: ОДОБРЕНО."
            await callback.answer("Помилован!")
        else:
            await bot.send_message(chat_id=target_user_id, text="🔴 Апелляция отклонена! Бан навсегда. 📐💥")
            new_text = original_text + "\n\n❌ ВЕРДИКТ: ОТКЛОНЕНО."
            await callback.answer("Отклонено!")

        await callback.message.edit_text(text=new_text, reply_markup=None)
    except TelegramAPIError:
        await callback.answer("Пользователь заблокировал бота.", show_alert=True)


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    logging.info("Многофункциональный бот Baldi Office запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
