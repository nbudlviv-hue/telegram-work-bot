import asyncio
import os
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, Text

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Файли для збереження ---
WORKERS_FILE = "workers.json"
OBJECTS_FILE = "objects.json"
EXPENSES_FILE = "expenses.json"

# --- Завантаження даних ---
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# --- Збереження даних ---
def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- Дані ---
workers = load_data(WORKERS_FILE)
objects = load_data(OBJECTS_FILE)
expenses = load_data(EXPENSES_FILE)

# --- Меню ---
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👷 Працівники")],
        [KeyboardButton(text="🏗 Об'єкти")],
        [KeyboardButton(text="💰 Витрати")],
    ],
    resize_keyboard=True
)

workers_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Додати працівника")],
        [KeyboardButton(text="📋 Список працівників")],
        [KeyboardButton(text="⬅ Назад")],
    ],
    resize_keyboard=True
)

objects_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Додати об'єкт")],
        [KeyboardButton(text="📋 Список об'єктів")],
        [KeyboardButton(text="⬅ Назад")],
    ],
    resize_keyboard=True
)

expenses_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Додати витрату")],
        [KeyboardButton(text="📋 Список витрат")],
        [KeyboardButton(text="⬅ Назад")],
    ],
    resize_keyboard=True
)

# --- Стан додавання ---
adding_item = {}

# --- Хендлери ---
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Головне меню:", reply_markup=main_keyboard)

# --- Меню працівників ---
@dp.message(Text("👷 Працівники"))
async def workers_menu(message: Message):
    await message.answer("Меню працівників:", reply_markup=workers_keyboard)

@dp.message(Text("➕ Додати працівника"))
async def add_worker_start(message: Message):
    adding_item[message.from_user.id] = {"type": "worker"}
    await message.answer("Введіть ім'я нового працівника:")

@dp.message(Text("📋 Список працівників"))
async def list_workers(message: Message):
    if workers:
        text = "\n".join([f"{i+1}. {w}" for i, w in enumerate(workers)])
        await message.answer(f"Список працівників:\n{text}")
    else:
        await message.answer("Поки що працівників немає.")

# --- Меню об'єктів ---
@dp.message(Text("🏗 Об'єкти"))
async def objects_menu(message: Message):
    await message.answer("Меню об'єктів:", reply_markup=objects_keyboard)

@dp.message(Text("➕ Додати об'єкт"))
async def add_object_start(message: Message):
    adding_item[message.from_user.id] = {"type": "object"}
    await message.answer("Введіть назву нового об'єкта:")

@dp.message(Text("📋 Список об'єктів"))
async def list_objects(message: Message):
    if objects:
        text = "\n".join([f"{i+1}. {o}" for i, o in enumerate(objects)])
        await message.answer(f"Список об'єктів:\n{text}")
    else:
        await message.answer("Поки що об'єктів немає.")

# --- Меню витрат ---
@dp.message(Text("💰 Витрати"))
async def expenses_menu(message: Message):
    await message.answer("Меню витрат:", reply_markup=expenses_keyboard)

@dp.message(Text("➕ Додати витрату"))
async def add_expense_start(message: Message):
    adding_item[message.from_user.id] = {"type": "expense"}
    await message.answer("Введіть опис витрати:")

@dp.message(Text("📋 Список витрат"))
async def list_expenses(message: Message):
    if expenses:
        text = "\n".join([f"{i+1}. {e}" for i, e in enumerate(expenses)])
        await message.answer(f"Список витрат:\n{text}")
    else:
        await message.answer("Поки що витрат немає.")

# --- Повернення назад ---
@dp.message(Text("⬅ Назад"))
async def back_to_main(message: Message):
    await message.answer("Головне меню:", reply_markup=main_keyboard)

# --- Прийом введених даних ---
@dp.message()
async def add_item(message: Message):
    user_id = message.from_user.id
    if adding_item.get(user_id):
        item_type = adding_item[user_id]["type"]
        name = message.text.strip()
        if not name:
            await message.answer("❌ Поле не може бути порожнім. Спробуйте ще раз.")
            return

        if item_type == "worker":
            workers.append(name)
            save_data(WORKERS_FILE, workers)
            await message.answer(f"✅ Працівник '{name}' доданий!")
            await message.answer("Меню працівників:", reply_markup=workers_keyboard)
        elif item_type == "object":
            objects.append(name)
            save_data(OBJECTS_FILE, objects)
            await message.answer(f"✅ Об'єкт '{name}' доданий!")
            await message.answer("Меню об'єктів:", reply_markup=objects_keyboard)
        elif item_type == "expense":
            expenses.append(name)
            save_data(EXPENSES_FILE, expenses)
            await message.answer(f"✅ Витрата '{name}' додана!")
            await message.answer("Меню витрат:", reply_markup=expenses_keyboard)

        adding_item[user_id] = None

# --- Запуск ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())