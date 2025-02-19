"""Handlers"""

# @router.message(F.text == 'Каталог')
# async def catalog(message: Message):
#     await message.answer('Выберите категорию товара', reply_markup=kb.catalog)
#
#
# @router.callback_query(F.data == 't-shirt')
# async def t_shirt(callback: CallbackQuery):
#     await callback.answer('Вы выбрали категорию', show_alert=True)
#     await callback.message.edit_text('Вы выбрали категорию футболок', reply_markup=await kb.inline_t_shirt())
#
#
# @router.message(Command('register'))
# async def register(message: Message, state: FSMContext):
#     await state.set_state(Register.name)
#     await message.answer('Введите ваше имя')
#
#
# @router.message(Register.name)
# async def register_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(Register.age)
#     await message.answer('Введите возраст')
#
#
# @router.message(Register.age)
# async def register_age(message: Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await state.set_state(Register.number)
#     await message.answer('Введите номер телефона', reply_markup=kb.get_number)
#
#
# '''F.contact - отправить ответ через кнопку'''
#
#
# @router.message(Register.number, F.contact)
# async def register_number(message: Message, state: FSMContext):
#     await state.update_data(number=message.contact.phone_number)
#     data = await state.get_data()
#     await message.answer(
#         f'Ваше имя: {data["name"]}\n Ваш возраст: {data["age"]}\n Ваш номер телефона: {data["number"]}')
#     await state.clear()

# @router.message()
# async def simple_text(message: Message):
#     if message.text.lower() == 'привет':
#         await message.reply(f'Рад тебя видеть, {message.from_user.first_name}!')
#     else:
#         pass


# @router.message(Command('hello-world'))
# async def command_hello_world(message: Message):
#     await message.answer(f'И тебе привет, {message.from_user.first_name}!')


"""Keyboard"""


# main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
#                                      [KeyboardButton(text='Корзина')],
#                                      [KeyboardButton(text='Контакты'), KeyboardButton(text='О нас')]],
#                            resize_keyboard=True,
#                            input_field_placeholder='Выберите пункт меню')
#
# catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Футболки', callback_data='t-shirt')],
#                                                 [InlineKeyboardButton(text='Кроссовки', callback_data='sneakers')],
#                                                 [InlineKeyboardButton(text='Кепки', callback_data='cap')]])


#
# t_shirt = ['Свитера', 'Толстовки', 'Майки']
#
#
# async def inline_t_shirt():
#     keyboard = InlineKeyboardBuilder()
#     for i in t_shirt:
#         keyboard.add(InlineKeyboardButton(text=i, callback_data=f't_shirt_{i}'))
#     return keyboard.adjust(2).as_markup()


