import asyncio
from aiogram import Bot, Dispatcher, executor, types
from config import token_my, user_id
from aiogram.dispatcher.filters import Text
import json
from main import check_new_art, get_first_art

bot = Bot(token = token_my)
dp = Dispatcher(bot)

@dp.message_handler(commands = "start")
async def start(message: types.Message):
    start_buttons = ["Все объявления" , "Новые","Обновить бд"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("куфар LETS_GO",reply_markup=keyboard)

@dp.message_handler(Text(equals="Обновить бд"))
async def update_bd(message: types.Message):
    get_first_art()
    await message.answer("БД обновилась ")

@dp.message_handler(Text(equals="Все объявления"))
async def get_all(message: types.Message):
    with open("dataBase.json") as file:
        new_dict = json.load(file)

    for k, v in new_dict.items():
        art = f"{v['Название: ']}\n" \
                f"{v['Ссылка: ']}\n" \
                f"{v['Цена: ']}\n"

        await message.answer(art)

@dp.message_handler(Text(equals="Новые"))
async def new_art(message: types.Message):
    new_art = check_new_art()

    if len(new_art) >= 1:
        for k, v in new_art.items():
            art = f"{v['Название: ']}\n" \
                  f"{v['Ссылка: ']}\n" \
                  f"{v['Цена: ']}\n"
        await message.answer(art)
    else:
        await message.answer("Нет новых")

async def new_art_hour():
    while True:
        new_art_HOUR = check_new_art()

        if len(new_art_HOUR) >= 1:
            for k, v in new_art.items():
                art = f"{v['Название: ']}\n" \
                      f"{v['Цена: ']}\n"

                await bot.send_message(user_id, art)

        else:
            await bot.send_message(user_id, "Новых объявлений не было!")

        await asyncio.sleep(3600)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(new_art_hour())
    executor.start_polling(dp)