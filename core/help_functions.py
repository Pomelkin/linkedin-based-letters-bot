from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Translate to English", callback_data="translate")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def update_text(message: Message, new_value: str):
    with suppress(TelegramBadRequest):
        await message.edit_text(new_value)
