import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import telegram_token, openai_api_key

token = telegram_token
openai.api_key = openai_api_key

bot = Bot(token)
dp = Dispatcher(bot)


async def start_bot(_):
    print('Бот запущен')

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет! Я бот с ChatGPt, просто напиши мне сообщение и я что-нибудь тебе отвечу")


@dp.message_handler()
async def send(message: types.Message):

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message.text}
        ]
    )

    await message.answer(completion.choices[0].message.content)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_bot)
