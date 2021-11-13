from main import bot, dp

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import admin_id, start_text, help_text, about_text
from reader import search, search_for_brands

questions = []


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text='Bot started work')


async def send_to_admin_questions(dp, questions):
    text = "Was searching for:\n"
    for question in questions:
        text = text + str(question) + "\n"
    await bot.send_message(chat_id=admin_id, text=text)


async def send_error(dp, error):
    await bot.send_message(chat_id=admin_id, text="Bot make error with query - {}".format(error))


@dp.message_handler(commands=["start"])
async def start(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text=start_text)


@dp.message_handler(commands=["help"])
async def help_message(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text=help_text)


@dp.message_handler(commands=["about"])
async def help_message(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text=about_text, parse_mode='HTML')


@dp.callback_query_handler(lambda call: True)
async def callback_inline(call):
    if call.message:
        if "~" in call.data:
            text = "Вот что нам удалось найти:"
            answer = search_for_brands(call.data[1:])

            if answer:
                for product in answer[:57]:
                    text = text + "\n\n" + "📍 " + f"{product[0]}\n  {product[1]} К.\t{product[2]} б.\t{product[3]} ж.\t{product[4]} у."
            else:
                text = "Не удалось ничего найти по запросу '{}' 😢".format(call.data[1:])

            await bot.send_message(chat_id=call.message.chat.id, text=text)
        else:
            text = "Вот что нам удалось найти:"
            answer = search(call.data)[3:]
            if len(answer) < 54:
                if answer:
                    for product in answer:
                        if product[5] != "" and product[5] != "None":
                            text = text + "\n\n" + f"{product[5]} " + f"{product[0]}\n  {product[1]} Ккал.\t{product[2]} б.\t{product[3]} ж.\t{product[4]} у."
                        else:
                            text = text + "\n\n" + "📍 " + f"{product[0]}\n  {product[1]} Ккал.\t{product[2]} б.\t{product[3]} ж.\t{product[4]} у."
                else:
                    text = "Не удалось ничего найти по запросу '{}' 😢".format(call.data[1:])
            else:
                if answer:
                    for product in answer[:65]:
                        if product[5] != "" and product[5] != "None":
                            text = text + "\n\n" + f"{product[5]} " + f"{product[0]}\n  {product[1]} Ккал.\t{product[2]} б.\t{product[3]} ж.\t{product[4]} у."
                        else:
                            text = text + "\n\n" + "📍 " + f"{product[0]}\n  {product[1]} Ккал.\t{product[2]} б.\t{product[3]} ж.\t{product[4]} у."
                else:
                    text = "Не удалось ничего найти по запросу '{}' 😢".format(call.data[1:])
            await bot.send_message(chat_id=call.message.chat.id, text=text)


@dp.message_handler()
async def echo(message: Message):

    questions.append(message.text)
    if len(questions) >= 10:
        await send_to_admin_questions(dp, questions)
        questions.clear()

    text = "Данные указаны на 100г продукта\n\nВот что нам удалось найти:"

    answer = search(message.text)
    if not answer:
        brend_button = InlineKeyboardButton('Поиск по брендированным продуктам', callback_data="~" + message.text)
        keyboard = InlineKeyboardMarkup().add(brend_button)
        text = "Не удалось ничего найти по запросу '{}' 😢".format(message.text)
        await bot.send_message(chat_id=message.from_user.id, reply_markup=keyboard, text=text, parse_mode="HTML")
        await send_error(dp, message.text)
    else:
        first_answer = []

        if len(answer) > 3:
            more_button = InlineKeyboardButton('Ещё!', callback_data=message.text)
            brend_button = InlineKeyboardButton('Поиск по брендированной продукции', callback_data="~"+message.text)
            keyboard = InlineKeyboardMarkup().add(more_button).add(brend_button)
            for i in range(3):
                first_answer.append(answer[i])
            for product in first_answer:
                if product[5] != "" and product[5] != "None":
                    text = text + "\n\n" + f"{product[5]} " + f"{product[0]}\n  {product[1]} Ккал.\t{product[2]} б.\t{product[3]} ж.\t{product[4]} у."
                else:
                    text = text + "\n\n" + "📍 " + f"{product[0]}\n  {product[1]} Ккал.\t{product[2]} б.\t{product[3]} ж.\t{product[4]} у."
            text = text + "\n\n" + "Нажмите <u><b>'Ещё!'</b></u> чтобы увидеть больше"
            await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=keyboard, parse_mode="HTML")
        else:
            brend_button = InlineKeyboardButton('Поиск по брендированной продукции', callback_data="~" + message.text)
            keyboard = InlineKeyboardMarkup().add(brend_button)
            for product in answer:
                text = text + "\n\n" + "📍 " + f"{product[0]}\n  {product[1]} К.\t{product[2]} б.\t{product[3]} ж.\t{product[4]} у."
            await bot.send_message(chat_id=message.from_user.id, reply_markup=keyboard, text=text, parse_mode="HTML")

