import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Вставьте сюда ваш токен от BotFather
TOKEN = "7038413967:AAFltpzXST8J3qbn2b0zjYkI0p89Lsy5WqQ"
# Ваш канал с символом @
CHANNEL_USERNAME = "@kemergalan"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def check_user_subscription(user_id: int) -> bool:
  """Проверяет, подписан ли пользователь на канал."""
  try:
    member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
    # Статусы, при которых считается, что пользователь подписан
    if member.status in [
        "creator",
        "administrator",
        "member",
    ]:
      return True
    return False
  except Exception as e:
    logging.error(f"Ошибка при проверке подписки: {e}")
    return False


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
  user_id = message.from_user.id

  # Проверяем подписку при старте
  is_subscribed = await check_user_subscription(user_id)

  if is_subscribed:
    # Если уже подписан — сразу выдаем бонус
    await message.answer(
        "🎉 Рады снова видеть вас! Спасибо, что подписаны на наш канал.\n\n"
        "Вот ваш обещанный бесплатный бонус:\n👉 [Ссылка на ваш подарок, файл"
        " или материал]"
    )
  else:
    # Если не подписан — просим подписаться и даем кнопку проверки
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Подписаться на канал",
                    url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Я подписался, проверить", callback_data="check_sub"
                )
            ],
        ]
    )
    await message.answer(
        "Привет! 👋 Чтобы получить бесплатный материал/бонус, подпишитесь на наш"
        f" канал:\n\n{CHANNEL_USERNAME}\n\nПосле подписки нажмите кнопку ниже:",
        reply_markup=keyboard,
    )


@dp.callback_query(F.data == "check_sub")
async def process_check_sub(callback: types.CallbackQuery):
  user_id = callback.from_user.id
  is_subscribed = await check_user_subscription(user_id)

  if is_subscribed:
    await callback.message.edit_text(
        "✅ Отлично! Подписка подтверждена.\n\n"
        "Вот ваш бесплатный бонус:\n👉 [Ссылка на ваш подарок, файл или"
        " материал]"
    )
  else:
    await callback.answer(
        "❌ Вы еще не подписались на канал! Пожалуйста, подпишитесь и нажмите"
        " кнопку снова.",
        show_alert=True,
    )


if __name__ == "__main__":
  import asyncio

  asyncio.run(dp.start_polling(bot))