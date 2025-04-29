import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import uvicorn
from fastapi import FastAPI
import os

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token='')
storage = MemoryStorage()
dp = Dispatcher()

# Инициализация FastAPI
app = FastAPI()

# Состояния для FSM
class KnittingStates(StatesGroup):
    waiting_for_yarn_type = State()
    waiting_for_needle_size = State()
    waiting_for_gauge = State()

# Клавиатура с веб-приложением
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Открыть калькулятор', web_app=WebAppInfo(url='https://your-webapp-url.com')))
    keyboard.add(KeyboardButton('Настройки'))
    return keyboard

# Обработчик команды /start
@dp.message(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать в калькулятор для вязания!\n\n"
        "Нажмите кнопку ниже, чтобы открыть калькулятор мерок.",
        reply_markup=get_main_keyboard()
    )

# Обработчик кнопки настроек
@dp.message(text='Настройки')
async def settings_handler(message: types.Message):
    await message.answer("Введите тип пряжи:")
    await KnittingStates.waiting_for_yarn_type.set()

# Обработчик ввода типа пряжи
@dp.message(state=KnittingStates.waiting_for_yarn_type)
async def process_yarn_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['yarn_type'] = message.text
    
    await message.answer("Введите размер спиц/крючка:")
    await KnittingStates.waiting_for_needle_size.set()

# Обработчик ввода размера инструмента
@dp.message(state=KnittingStates.waiting_for_needle_size)
async def process_needle_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['needle_size'] = message.text
    
    await message.answer("Введите плотность вязания (петель на 10 см):")
    await KnittingStates.waiting_for_gauge.set()

# Обработчик ввода плотности
@dp.message(state=KnittingStates.waiting_for_gauge)
async def process_gauge(message: types.Message, state: FSMContext):
    try:
        gauge = int(message.text)
        async with state.proxy() as data:
            data['gauge'] = gauge
        
        await message.answer(
            f"Настройки сохранены:\n"
            f"Пряжа: {data['yarn_type']}\n"
            f"Инструмент: {data['needle_size']}\n"
            f"Плотность: {gauge} п./10 см",
            reply_markup=get_main_keyboard()
        )
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите число для плотности вязания.")

# Веб-хук для FastAPI
@app.post('/webhook')
async def process_webhook_update(update: dict):
    telegram_update = types.Update(**update)
    await dp.process_update(telegram_update)
    return {"status": "ok"}

# Запуск бота
async def on_startup(dp):
    await bot.set_webhook('https://your-webapp-url.com/webhook')

if __name__ == '__main__':
    from aiogram import executor
    import threading
    
    # Запуск FastAPI в отдельном потоке
    def run_fastapi():
        uvicorn.run(app, host="0.0.0.0", port=8000)
    
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.start()
    
    # Запуск бота
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)