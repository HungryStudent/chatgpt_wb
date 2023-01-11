import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from create_bot import dp, log
from states.admin import *
import keyboards as kb
from utils import db
from config import *


@dp.message_handler(content_types="document")
async def send_file_id(message: Message):
    await message.answer(message.document.file_id)


@dp.message_handler(lambda m: m.from_user.id in admin_id, text="Запустить рассылку")
@dp.message_handler(lambda m: m.from_user.id in admin_id, commands="send")
async def send_text(message: Message):
    await message.answer("Введите текст рассылки", reply_markup=kb.admin_cancel)
    await SendStates.enter_text.set()


@dp.message_handler(lambda m: m.from_user.id in admin_id, state="*", text="Отменить рассылку")
async def cancel_input(message: Message, state: FSMContext):
    await message.answer("Ввод остановлен")
    await state.finish()


@dp.message_handler(state=SendStates.enter_text)
async def start_send(message: Message, state: FSMContext):
    users = db.get_users()
    count = 0
    block_count = 0
    await message.answer("Начал рассылку", reply_markup=kb.ReplyKeyboardRemove())
    for bot_user in users:
        try:
            await message.bot.send_message(bot_user[0], message.text)
            count += 1
        except Exception as e:
            log.info(f"Error in broadcaster | {e}")
            block_count += 1
        await asyncio.sleep(0.1)
    await message.answer(
        f"Количество получивших сообщение: {count}/{len(users)}")

    await state.finish()
