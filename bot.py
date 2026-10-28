import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏋️‍♂️ алистеника и база", callback_data="ex_calisthenics")],
        [InlineKeyboardButton(text="🔄 Скакалка и выносливость", callback_data="ex_rope")],
        [InlineKeyboardButton(text="🦾 езинки и сопротивление", callback_data="ex_bands")],
        [InlineKeyboardButton(text="📋 ек-лист тренировки дня", callback_data="daily_check")]
    ])
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        "риветствую! Я официальный бот канала @kemergalan.\n\n"
        "десь вы найдете базу упражнений, программы тренировок и мотивацию для ежедневной дисциплины.\n"
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
        "исциплина и регулярность — залог результата на годы вперёд!"
    )
    await callback.message.edit_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "ex_rope")
async def cb_rope(callback: CallbackQuery):
    text = (
        "🔄 **Скакалка и кардио**\n\n"
        "• рыжки на скакалке отлично развивают координацию, взрывную силу ног и дыхательную систему.\n"
        "• ержите темп, работайте стопами и выстраивайте ритм."
    )
    await callback.message.edit_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "ex_bands")
async def cb_bands(callback: CallbackQuery):
    text = (
        "🦾 **орцовские резинки**\n\n"
        "• Сопротивление под нагрузкой защищает суставы и прорабатывает стабилизаторы.\n"
        "• тлично подходит для функциональной подготовки и укрепления связок."
    )
    await callback.message.edit_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "daily_check")
async def cb_daily_check(callback: CallbackQuery):
    text = (
        "📋 **ек-лист на сегодня:**\n"
        "1. азминка и суставная гимнастика\n"
        "2. сновной блок (отжимания / скакалка)\n"
        "3. Травмобезопасность и умеренный темп\n\n"
        "ажали кнопку — зафиксировали настрой на победу! 💪"
    )
    await callback.message.edit_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")
    await callback.answer()

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
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
