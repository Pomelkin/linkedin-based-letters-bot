from aiogram import F, Bot
from aiogram.types import Message, VideoNote, CallbackQuery
from core.loader import dp
from core.help_functions import MP4ToMP3, get_keyboard, update_text
from core.loader import model
from core.database import async_session_maker
import random
import string

from core.operations.models import texts
from core.placeholders import Placeholder
from deep_translator import GoogleTranslator
from sqlalchemy import insert
import os


@dp.message(F.content_type.func(lambda content_type: content_type != 'video_note'))
async def check_video(message: Message):
    await message.answer(f'Извините, {message.from_user.full_name}. Я умею работать только с видеосообщениями.')


@dp.message(F.content_type == 'video_note')
async def check_video(message: VideoNote, bot: Bot):
    async with Placeholder(bot, message.chat.id):
        filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
        path_mp4 = fr'data\{filename}.mp4'
        path_mp3 = fr'data\{filename}.mp3'
        await bot.download(message.video_note, path_mp4)
        await MP4ToMP3(path_mp4, path_mp3)

        result, info = model.transcribe(path_mp3, vad_filter=True)
        is_en = False
        try:
            if info.language == 'en':
                is_en = True

            result = list(result)[0]
            text = result[4]
            os.remove(path_mp4)
            os.remove(path_mp3)
            async with async_session_maker() as session:
                await session.scalars(insert(texts).values(
                    user_id=message.from_user.id,
                    user_name=message.from_user.full_name,
                    text_from_video=text
                ))
                await session.commit()
        except IndexError:
            os.remove(path_mp4)
            os.remove(path_mp3)
            is_en = False
            text = "Не удалось распознать текст из видеосообщения."

    if not is_en:
        await message.reply(f'{text}', reply_markup=get_keyboard())
    else:
        await message.reply(f'{text}')


@dp.callback_query(F.data == 'translate')
async def translate(callback: CallbackQuery):
    text = callback.message.text
    translated_text_eu = GoogleTranslator(source='auto', target='english').translate(text=text)
    await update_text(callback.message, translated_text_eu)
    await callback.answer()
