import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("سلام 👋\nخرید حساب کنم یا فروش؟\n(بنویس خرید یا فروش)")

@dp.message(F.text.in_(["خرید","فروش"]))
async def side(message: Message):
    user_data[message.chat.id] = {"side": message.text}
    await message.answer("نرخ هر گرم (تومان) رو بفرست:")

@dp.message()
async def calc(message: Message):
    data = user_data.get(message.chat.id)

    if not data.get("rate"):
        data["rate"] = float(message.text.replace(",",""))
        await message.answer("وزن (گرم) رو بفرست:")
        return

    if not data.get("weight"):
        data["weight"] = float(message.text)
        await message.answer("درصد کارمزد رو بفرست:")
        return

    if not data.get("fee"):
        data["fee"] = float(message.text)

        raw = data["rate"] * data["weight"]
        fee = raw * (data["fee"]/100)

        total = raw + fee if data["side"]=="فروش" else raw - fee

        await message.answer(
            f"💰 مبلغ نهایی:\n{total:,.0f} تومان"
        )

        user_data.pop(message.chat.id)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
