import asyncio
import logging
import os
import random
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@kemergalan"
# кажите ваш Telegram ID (числом), чтобы получать сообщения от пользователей через бота (если нужно)
ADMIN_ID = 0  # ри желании сюда можно вписать ваш числовой ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# анк цитат для генератора мотивации (без повторений, с флагами 🇹🇷🇺🇸)
QUOTES = [
    "«исциплина — это мост между целями и достижениями.» 🇹🇷🇺🇸",
    "«вижение — это радость, а регулярность — это закон силы.» 🇹🇷🇺🇸",
    "«обеждай себя каждый день, а не кого-то другого.» 🇹🇷🇺🇸",
    "«озраст — это просто цифра, когда в теле есть стержень и режим.» 🇹🇷🇺🇸",
    "«Сила не приходит от побед. Силу куют преодоление и трудности.» 🇹🇷🇺🇸"
]

def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏋️‍♂️ алистеника и база", callback_data="ex_calisthenics")],
        [InlineKeyboardButton(text="🔄 Скакалка и выносливость", callback_data="ex_rope")],
        [InlineKeyboardButton(text="🦾 езинки и сопротивление", callback_data="ex_bands")],
        [InlineKeyboardButton(text="📋 ек-лист тренировки дня", callback_data="daily_check")],
        [InlineKeyboardButton(text="🔢 алькулятор нагрузки", callback_data="calc_start")],
        [InlineKeyboardButton(text="💡 удрость дисциплины", callback_data="random_quote")],
        [InlineKeyboardButton(text="✉️ аписать автору", callback_data="contact_author")]
    ])
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        "риветствую! Я официальный бот канала @kemergalan.\n\n"
        "десь вы найдете базу упражнений, программы тренировок, расчет нагрузки и мотивацию для ежедневной дисциплины.\n"
        "ыберите нужный раздел в меню ниже:"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu())

@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("лавное меню тренера:", reply_markup=get_main_menu())

@dp.callback_query(F.data == "ex_calisthenics")
async def cb_calisthenics(callback: CallbackQuery):
    text = (
        "🏋️‍♂️ **алистеника и базовые упражнения**\n\n"
        "• **Тайсон-отжимания:** ощная база для груди, плеч и трицепсов.\n"
        "• **Собственный вес:** снова силы, выносливости и суставного здоровья.\n"
        "исциплина и регулярность — залог результата на годы вперёд! 🇹🇷🇺🇸"
    )
    await callback.message.edit_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "ex_rope")
async def cb_rope(callback: CallbackQuery):
    text = (
        "🔄 **Скакалка и кардио**\n\n"
        "• рыжки на скакалке отлично развивают координацию, взрывную силу ног и дыхательную систему.\n"
        "• ержите темп, работайте стопами и выстраивайте ритм. 🇹🇷🇺🇸"
    )
    await callback.message.edit_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "ex_bands")
async def cb_bands(callback: CallbackQuery):
    text = (
        "🦾 **орцовские резинки**\n\n"
        "• Сопротивление под нагрузкой защищает суставы и прорабатывает стабилизаторы.\n"
        "• тлично подходит для функциональной подготовки и укрепления связок. 🇹🇷🇺🇸"
    )
    await callback.message.edit_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "daily_check")
async def cb_daily_check(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ а, тренировку выполнил!", callback_data="done_workout")],
        [InlineKeyboardButton(text="⬅️ азад в меню", callback_data="back_to_menu")]
    ])
    text = (
        "📋 **ек-лист на сегодня:**\n"
        "1. азминка и суставная гимнастика\n"
        "2. сновной блок (отжимания / скакалка)\n"
        "3. Травмобезопасность и умеренный темп\n\n"
        "ажмите кнопку ниже, чтобы зафиксировать выполнение:"
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "done_workout")
async def cb_done_workout(callback: CallbackQuery):
    text = (
        "🔥 **тличная работа!**\n\n"
        "Тренировка зафиксирована. исциплина — это делать то, что нужно, независимо от настроения.\n"
        "Так держать! 🇹🇷🇺🇸"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️  главное меню", callback_data="back_to_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer("ринято! тличный результат! 💪")

# --- Я  1: алькулятор нагрузки ---
@dp.callback_query(F.data == "calc_start")
async def cb_calc_start(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌱 азовый (Старт / азминка)", callback_data="calc_base")],
        [InlineKeyboardButton(text="⚡ Средний (веренный ритм)", callback_data="calc_mid")],
        [InlineKeyboardButton(text="🔥 родвинутый (есткая база)", callback_data="calc_hard")],
        [InlineKeyboardButton(text="⬅️ азад в меню", callback_data="back_to_menu")]
    ])
    text = (
        "🔢 **алькулятор персональной нормы**\n\n"
        "ыберите ваш текущий уровень подготовки, чтобы получить ориентир по нагрузке:"
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data.startswith("calc_"))
async def cb_calc_result(callback: CallbackQuery):
    level = callback.data.split("_")[1]
    if level == "base":
        rec = "• тжимания: 3 подхода по 15–20 раз\n• Скакалка: 300–500 прыжков\n• кцент на технику и суставы."
    elif level == "mid":
        rec = "• тжимания: 4 подхода по 25–35 раз\n• Скакалка: 1000 прыжков\n• веренный темп и контроль дыхания."
    else:
        rec = "• тжимания: 5+ подходов по 40+ раз (Тайсон-база)\n• Скакалка: 1500–2000 прыжков\n• есткая дисциплина и выносливость."

    text = f"📊 **аша рекомендация на тренировку:**\n\n{rec}\n\nлавное — слушать тело и избегать перегрузок! 🇹🇷🇺🇸"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️  главное меню", callback_data="back_to_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

# --- Я  2: енератор цитат / мудрости ---
@dp.callback_query(F.data == "random_quote")
async def cb_random_quote(callback: CallbackQuery):
    quote = random.choice(QUOTES)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 ще цитату", callback_data="random_quote")],
        [InlineKeyboardButton(text="⬅️ азад в меню", callback_data="back_to_menu")]
    ])
    text = f"💡 **удрость дня:**\n\n{quote}"
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

# --- Я  3: Связь с автором ---
@dp.callback_query(F.data == "contact_author")
async def cb_contact_author(callback: CallbackQuery):
    text = (
        "✉️ **Связь с автором**\n\n"
        "сть вопрос по технике, программе или предложению?\n"
        "ы можете написать напрямую в наш канал **@kemergalan** или оставить отзыв в комментариях к постам! 🇹🇷🇺🇸"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ азад в меню", callback_data="back_to_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "back_to_menu")
async def cb_back(callback: CallbackQuery):
    await callback.message.edit_text("лавное меню тренера:", reply_markup=get_main_menu())
    await callback.answer()

# --- оновый автопостинг в канал ---
async def scheduled_post_job():
    await asyncio.sleep(10)
    try:
        post_text = (
            "💪 **жедневная мотивация и дисциплина**\n\n"
            "«исциплина — это выбор между тем, чего ты хочешь сейчас, и тем, чего ты хочешь больше всего.»\n\n"
            "е пропускайте тренировки, укрепляйте тело и дух. 🇹🇷🇺🇸\n"
            "👉 агляните в нашего бота @isometrics_bot за программами тренировок!"
        )
        await bot.send_message(CHANNEL_ID, post_text, parse_mode="Markdown")
        print("втоматический пост успешно отправлен в канал!")
    except Exception as e:
        print(f"шибка при автопостинге в канал: {e}")

async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Health check server started on port {port}")

async def main():
    asyncio.create_task(start_web_server())
    asyncio.create_task(scheduled_post_job())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
