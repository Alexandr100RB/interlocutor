import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import telegram_token, openai_api_key

token = telegram_token
openai.api_key = openai_api_key

bot = Bot(token)
dp = Dispatcher(bot)

# Здесь сохраняем историю сообщений
messages = []


async def start_bot(_):
    print('Бот запущен')


# Приветствие при запуске бота
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Привет! Я бот с ChatGPt, просто напиши мне сообщение и я что-нибудь тебе отвечу")


# Любое сообщение от пользователя обрабатываем с chatgpt
@dp.message_handler()
async def send(message: types.Message):
    try:
        messages.append({"role": "user", "content": message.text})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": response})

        await message.answer(completion.choices[0].message.content)
    except Exception:
        await bot.send_message(message.from_user.id, "что-то пошло не так, попробуй ещё")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_bot)
