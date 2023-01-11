from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from config import channel_url

market = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(KeyboardButton("Озон"),
                                                                    KeyboardButton("Wildberries"))

limit = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(KeyboardButton("Ограничение в 5000 символов"),
                                                                   KeyboardButton("Ограничение в 1000 символов"))

symbols_count = {
    "Ограничение в 5000 символов": ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(KeyboardButton("500"),
                                                                                              KeyboardButton("1000"),
                                                                                              KeyboardButton("2500"),
                                                                                              KeyboardButton("5000")),
    "Ограничение в 1000 символов": ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(KeyboardButton("500"),
                                                                                              KeyboardButton("1000"))
}

channel = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Канал", url=channel_url),
                                                InlineKeyboardButton("Я подписался", callback_data="check_sub"))

ready_text = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton("Ещё вариант"),
                                                                        KeyboardButton("Начать заново"),
                                                                        KeyboardButton(
                                                                            "Получить PDF гайд как безопасно делать выкупы в 2023"))

admin_cancel = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(KeyboardButton("Отмена"))
