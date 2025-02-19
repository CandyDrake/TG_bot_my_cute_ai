import os
from typing import List

from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from config_data.config import USER_IDS_FILE
import json
import asyncio
from aiogram.exceptions import TelegramRetryAfter
from aiogram import Bot



def load_user_ids():
    if os.path.exists(USER_IDS_FILE):
        with open(USER_IDS_FILE, 'r') as f:
            return json.load(f)
    return []


def save_user_ids(user_ids):
    with open(USER_IDS_FILE, 'w') as f:
        json.dump(user_ids, f)


def add_user_ids(user_id):
    user_ids = load_user_ids()
    if user_id not in user_ids:
        user_ids.append(user_id)
        save_user_ids(user_ids)
        print('User_id сохранен')


async def send_messages(bot: Bot, user_ids, text: str):
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, text)
            await asyncio.sleep(1)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except Exception as e:
            print(f'Не удалось отправить сообщения {user_id} по причине {e}')

