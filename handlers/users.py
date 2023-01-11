from enum import Enum

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from aiogram.types import Message, CallbackQuery, ChatMember
from aiogram import Dispatcher
from aiogram.utils.exceptions import BotKicked

from create_bot import dp
from datetime import date, timedelta
import keyboards as kb
from handlers import texts
from utils import db, chatgpt
from states import user as states
from config import channel_id, pdf_id


@dp.message_handler(commands='start', state="*")
async def start_message(message: Message, state: FSMContext):
    await state.finish()
    user = db.get_user(message.from_user.id)
    if user is None:
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.answer(texts.hello)
    await message.answer(texts.choose_market, reply_markup=kb.market)


@dp.message_handler(text="Начать заново")
async def start_again(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(texts.choose_market, reply_markup=kb.market)


@dp.message_handler(text="Озон")
@dp.message_handler(text="Wildberries")
async def limit_page(message: Message):
    await message.answer(texts.choose_limit, reply_markup=kb.limit)


@dp.message_handler(text="Ограничение в 5000 символов")
@dp.message_handler(text="Ограничение в 1000 символов")
async def choose_symbols_count(message: Message):
    await message.answer(texts.choose_symbols_count, reply_markup=kb.symbols_count[message.text])
    await states.DataStates.enter_symbols_count.set()


@dp.message_handler(state=states.DataStates.enter_symbols_count)
async def enter_name(message: Message, state: FSMContext):
    try:
        symbols_count = int(message.text)
    except ValueError:
        await message.answer("Введите целое число")
        return
    if not 500 < symbols_count < 5000:
        await message.answer("Введите целое число в пределах от 500 до 5000")
    await state.update_data(symbols_count=symbols_count)
    await message.answer(texts.enter_name, reply_markup=kb.ReplyKeyboardRemove())
    await states.DataStates.next()


@dp.message_handler(state=states.DataStates.enter_name)
async def enter_keys(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(texts.enter_keys)
    await states.DataStates.next()


@dp.message_handler(state=states.DataStates.enter_keys, text="Ещё вариант")
async def repeat_generate_description(message: Message, state: FSMContext):
    text_data = await state.get_data()
    await message.answer(texts.load_api)
    ready_text = await chatgpt.gen_text(text_data)
    await message.answer(ready_text, reply_markup=kb.ready_text)


@dp.message_handler(state="*", text="Получить PDF гайд как безопасно делать выкупы в 2023")
async def pdf(message: Message):
    await message.answer_document(pdf_id)


@dp.message_handler(state=states.DataStates.enter_keys)
async def generate_description(message: Message, state: FSMContext):
    await state.update_data(keys=message.text)

    status: ChatMember = await message.bot.get_chat_member(channel_id, message.from_user.id)
    if status.status == "left":
        await message.answer(texts.error_sub, reply_markup=kb.channel)
        return

    text_data = await state.get_data()
    await message.answer(texts.load_api)
    ready_text = await chatgpt.gen_text(text_data)
    await message.answer(ready_text, reply_markup=kb.ready_text)


@dp.callback_query_handler(state=states.DataStates.enter_keys, text="check_sub")
async def check_sub(call: CallbackQuery, state: FSMContext):
    status: ChatMember = await call.bot.get_chat_member(channel_id, call.from_user.id)
    if status.status == "left":
        await call.answer("Подпишитесь!")
        return

    text_data = await state.get_data()
    await call.message.answer(texts.load_api)
    ready_text = await chatgpt.gen_text(text_data)
    await call.message.answer(ready_text, reply_markup=kb.ready_text)
    await call.answer()