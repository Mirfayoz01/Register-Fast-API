import asyncio
import logging
import random
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from handlers import button


TOKEN = "7360891386:AAEF-0VE2YUHPRKZq0i_PGNDvNMtzix1z6I"
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Salom !", reply_markup=button)


@dp.message(F.contact)
async def telefon_raqam(message: Message):
    code = "".join([str(random.randint(0, 9)) for _ in range(6)])

    try:
        response = requests.post("http://127.0.0.1:8000/store-code", json={"code": code})
        response.raise_for_status()
    except Exception as e:
        await message.answer("Server bilan bog'lanishda xatolik.")
        return

    await message.answer(f"6 xonali kod: {code}")


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
