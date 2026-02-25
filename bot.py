import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# Беремо токен з Environment Variables Render
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Не знайдено BOT_TOKEN! Додай змінну середовища на Render.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Головне меню ---
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👷 Працівники")],
        [KeyboardButton(text="🏗 Об'єкти")],
        [KeyboardButton(text="💰 Витрати")],
        [KeyboardButton(text="🛑 Стоп")],  # Кнопка Стоп
    ],
    resize_keyboard=True
)

# --- Меню працівників ---
workers_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Додати працівника")],
        [KeyboardButton(text="📋 Список працівників")],
        [KeyboardButton(text="⬅ Назад")],
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Головне меню:", reply_markup=main_keyboard)

@dp.message(F.text == "👷 Працівники")
async def workers_menu(message: Message):
    await message.answer("Меню працівників:", reply_markup=workers_keyboard)

@dp.message(F.text == "⬅ Назад")
async def back_to_main(message: Message):
    await message.answer("Головне меню:", reply_markup=main_keyboard)

@dp.message(F.text == "➕ Додати працівника")
async def add_worker(message: Message):
    await message.answer("Функція додавання працівника скоро буде 👷")

@dp.message(F.text == "📋 Список працівників")
async def list_workers(message: Message):
    await message.answer("Список працівників скоро буде 📋")

@dp.message(F.text == "🛑 Стоп")
async def stop_bot(message: Message):
    await message.answer("Бот зупиняється... 🛑")
    await bot.session.close()
    # На Render бот не зупиниться повністю, але закриє сесію бота

async def main():
    print("Бот запущено...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())