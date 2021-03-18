import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.handlers.common import cmd_start
from app.handlers.common import register_handlers_common
from app.handlers.arm_oper import register_handlers_arm_oper
#from app.handlers.arm_engin import register_handlers_arm_engin


logger = logging.getLogger(__name__)


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="<i>Начало работы с ботом</i>"),
        BotCommand(command="/cancel", description="<i>Отменить текущее действие</i>")
    ]
    await bot.set_my_commands(commands)

async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
    ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")

    bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_common(dp, ACCESS_ID)
    register_handlers_arm_oper(dp)
    #register_handlers_arm_engin(dp)

    # Парсинг файла конфигурации
    #config = load_config("config/bot.ini")

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())