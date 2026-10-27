import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Ваши данные
TOKEN = "7038413967:AAFltpzXST8J3qbn2b0zjYkI0p89Lsy5WqQ"
CHANNEL_USERNAME = "@kemergalan"
CHANNEL_URL = "https://t.me/kemergalan"

# Ссылка на ваш бонус (можете заменить на любую другую: на пост в канале, файл, сайт или видео)
BONUS_LINK = "https://t.me/kemergalan" 

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def check_user_subscription(user_id: int) -> bool:
  """Проверяет, подписан ли пользователь на канал."""
  try:
    member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
    if member.status in ["creator", "administrator", "member"]:
      return True
    return False
  except Exception as e:
    logging.error(f"Ошибка при проверке подписки: {e}")
    return False


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
  user_id = message.from_user.id
  user_name = message.from_user.first_name or "друг"

  # Проверяем подписку при старте
  is_subscribed = await check_user_subscription(user_id)

  if is_subscribed:
    # Если пользователь уже подписан
    await message.answer(
        f"Рад снова видеть вас, {user_name}! 💪\n\n"
        "Вы уже подписаны на наш канал. Как и обещал, вот доступ к материалу:\n\n"
        f"👉 **Забрать бонус:** {BONUS_LINK}",
        parse_mode="Markdown"
    )
  else:
    # Если не подписан — показываем приветствие и кнопку подписки
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Подписаться на @kemergalan",
                    url=CHANNEL_URL
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Я подписался, получить бонус",
                    callback_data="check_sub"
                )
            ],
        ]
    )
    await message.answer(
        f"Приветствую, {user_name}! 👋\n\n"
        "Добро пожаловать! Чтобы получить эксклюзивный материал и "
        "полезные практики для здоровья и физической формы, подпишитесь на канал:\n\n"
        f"📌 **{CHANNEL_USERNAME}**\n\n"
        "После подписки нажмите кнопку ниже, чтобы открыть доступ:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


@dp.callback_query(F.data == "check_sub")
async def process_check_sub(callback: types.CallbackQuery):
  user_id = callback.from_user.id
  is_subscribed = await check_user_subscription(user_id)

  if is_subscribed:
    await callback.message.edit_text(
        "🎉 **Отлично! Подписка успешно подтверждена.**\n\n"
        "Благодарим вас за то, что вы с нами! Вот ваш обещанный бонус:\n\n"
        f"👉 **Забрать материал:** {BONUS_LINK}",
        parse_mode="Markdown"
    )
  else:
    await callback.answer(
        "❌ Вы еще не подписались на канал! Пожалуйста, подпишитесь на "
        "@kemergalan и нажмите кнопку снова.",
        show_alert=True,
    )


if __name__ == "__main__":
  import asyncio
  asyncio.run(dp.start_polling(bot))
