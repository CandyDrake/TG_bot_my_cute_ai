from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

inform = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Получить инфо', callback_data='get_info')],
                                               [InlineKeyboardButton(text='Не получать инфо',
                                                                     callback_data='skip_info')]])

contact = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]],
                              resize_keyboard=True, input_field_placeholder='Нажми кнопку "Отправить номер"')


def create_page_buttons(current_page: int, total_pages: int):
    buttons = []

    if current_page > 1:
        buttons.append(InlineKeyboardButton(text="Предыдущая", callback_data=f"prev_page:{current_page - 1}"))

    if current_page < total_pages:
        buttons.append(InlineKeyboardButton(text="Следующая", callback_data=f"next_page:{current_page + 1}"))

    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return keyboard


schedule = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Полный день", callback_data='fullDay')],
                                                 [InlineKeyboardButton(text='Сменный график',
                                                                       callback_data='shift')],
                                                 [InlineKeyboardButton(text='Гибкий график',
                                                                       callback_data='flexible')],
                                                 [InlineKeyboardButton(text='Удаленная работа',
                                                                       callback_data='remote')]])

subscribe = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Получить рассылку", callback_data='yes')],
                                                  [InlineKeyboardButton(text='Не подписываться', callback_data='no')]])


inline_subscribe = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text="9:00", callback_data='9:00'),
            types.InlineKeyboardButton(text='12:00', callback_data='12:00')
        ],
        [
            types.InlineKeyboardButton(text='16:00', callback_data='16:00'),
            types.InlineKeyboardButton(text='18:00', callback_data='18:00')
        ]
    ]
)
