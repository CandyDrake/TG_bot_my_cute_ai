from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
import keyboards.keyboards as kb
from database.requests import set_user, update_user, update_query, update_timestamp, merged_queries, update_subscribe
from states.states import WorkAI, Reg, JobSearch, Subscribe
from database.generator import generator
from database.users import *
from api.api import get_city_id, search_vacancies, send_vacancies_to_user

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    user = await set_user(message.from_user.id)
    if user and user.name:
        await message.answer(f'Привет, {user.name}! Список моих команд: /start, /info, /help, /find_job, /history и '
                             f'/subscribe.\nНабери /help чтобы узнать больше!\n'
                             f'Или можешь спросить меня о чем угодно кроме, постараюсь ответить на любой твой вопрос!')
        await state.clear()
    else:
        await message.answer(
            f'Привет, {message.from_user.first_name}! Я умею подбирать для тебя вакансии, основываясь на твоих '
            f'предпочтениях. Также я поддерживаю нейросеть и с удовольствием отвечу на все твои'
            f'вопросы или просто поболтаем!'
            f'Список моих команд: /start, /info, /help, /find_job, /history и /subscribe.\nНабери /help чтобы узнать больше!\n'
            f'Или можешь просто спросить меня о том, что тебя интересует помимо поиска работы '
            f'Зарегистрируйся, пожалуйста, если еще этого не сделал, и я смогу помогать тебе эффективнее'
            f':)\n\nИтак, напиши свое имя!')
        await state.set_state(Reg.name)


@router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.contact)
    await message.answer('Отправь свой номер телефона', reply_markup=kb.contact)


@router.message(Reg.contact, F.contact)
async def reg_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    contact = message.contact.phone_number
    user = await update_user(message.from_user.id, name, contact)
    if user:
        await message.answer(f'Спасибо, {data["name"]}, записал тебя!', reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer('Ошибка регистрации')
        await state.clear()


@router.message(Command('history'))
async def command_history(message: Message):
    user = await set_user(message.from_user.id)
    if user and user.queries:
        history_text = "Вот твоя история запросов по поиску вакансий:\n"
        query = user.queries
        stamp = user.timestamp
        history_text += await merged_queries(stamp, query)
        await message.answer(history_text)
    else:
        await message.answer('Ты не зарегистрирован или твоя история запросов пуста. Нажми /start чтобы '
                             'зарегистрироваться или набери /find_job чтобы начать поиски работы своей мечты!')


@router.message(Command('help'))
async def command_help(message: Message):
    await message.answer(
        'Ты можешь использовать команды:\n'
        '/start - для регистрации\n'
        '/info - для получения информации о моем появлении онлайн\n'
        '/history - для просмотра истории запросов\n'
        '/find_job - чтобы начать поиск работы\n'
        '/subscribe - чтобы подписаться на ежедневную рассылку свежих вакансий на основе твоего последнего запроса\n'
        'Или можешь просто задать мне свой вопрос, и я постараюсь ответить :)')


@router.message(Command('info'))
async def command_info(message: Message):
    await message.answer('Иногда я могу уходить на доработку. Если такое случилось, то я могу предупредить тебя, '
                         'когда снова стану доступен. Если хочешь получать информацию, нажмите на кнопку "Получить '
                         'инфо"', reply_markup=kb.inform)


@router.message(Command('subscribe'))
async def command_subscribe(message: Message, state: FSMContext):
    await message.answer('Здесь ты можешь подписаться на ежедневную рассылку вакансий на основе твоего последнего '
                         'запроса! Если хочешь подписаться, нажми на кнопку "Получить рассылку"',
                         reply_markup=kb.subscribe)
    await state.set_state(Subscribe.ask_subscribe)


@router.callback_query(Subscribe.ask_subscribe, F.data == 'yes')
async def get_subscribe(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Подписываю...', show_alert=False)
    await state.set_state(Subscribe.time_choose)

    await callback.message.edit_text('Выбери время получения рассылки', reply_markup=kb.inline_subscribe)


@router.callback_query(Subscribe.time_choose, lambda c: c.data in ['9:00', '12:00', '16:00', '18:00'])
async def ask_time(callback_query: CallbackQuery, state: FSMContext):
    selected_time = callback_query.data
    await state.update_data(schedule=selected_time)
    await update_subscribe(callback_query.from_user.id, selected_time)
    await callback_query.message.edit_text('Подписал тебя!', reply_markup=None)

    await state.clear()


@router.callback_query(Subscribe.ask_subscribe, F.data == 'no')
async def cancel_subscription(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Подписка отменена.', show_alert=False)
    await callback.message.edit_text('Подписка отменена', reply_markup=None)
    await state.clear()


@router.message(Command('find_job'))
async def command_find_job(message: Message, state: FSMContext):
    await message.answer('Для начала ответь на несколько вопросов, чтобы я мог помочь тебе с поиском:\n\n'
                         'В каком городе будем искать вакансии?')
    await state.set_state(JobSearch.city)


@router.message(JobSearch.city)
async def ask_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer('Отлично, по какой специальности ищем?')
    await state.set_state(JobSearch.profession)


@router.message(JobSearch.profession)
async def ask_profession(message: Message, state: FSMContext):
    await state.update_data(profession=message.text)
    await message.answer('Понял. Теперь выбери график работы:', reply_markup=kb.schedule)
    await state.set_state(JobSearch.schedule)


@router.callback_query(lambda c: c.data in ['fullDay', 'shift', 'flexible', 'remote'])
async def ask_schedule(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Окей!', reply_markup=ReplyKeyboardRemove())
    selected_schedule = callback_query.data
    await state.update_data(schedule=selected_schedule)
    await callback_query.message.answer('Сколько хочешь получать в рублях?')
    await state.set_state(JobSearch.salary)


@router.message(JobSearch.salary)
async def ask_salary_min(message: Message, state: FSMContext):
    await state.update_data(salary=message.text)
    user_data = await state.get_data()
    city = user_data['city']
    profession = user_data['profession'].lower()
    schedule = user_data['schedule']
    salary = user_data['salary'].replace(' ', '')
    user_query = f'{city}:{profession}:{schedule}:{salary}'
    await update_query(message.from_user.id, user_query)
    await update_timestamp(message.from_user.id)

    if salary.isdigit():
        salary = int(salary)
        city_id = get_city_id(city)
        if city_id:
            current_page = 1
            vacancies = search_vacancies(city_id, profession, schedule, salary, page=current_page, per_page=10)
            if vacancies:
                await send_vacancies_to_user(vacancies, message, current_page)
            else:
                await message.answer('Вакансий не найдено.')
        else:
            await message.answer('Город не найден, попробуй заново!')

    else:
        await message.answer('Неверный формат зарплаты, попробуй еще раз!')


@router.callback_query(lambda c: c.data.startswith('prev_page') or c.data.startswith('next_page'))
async def paginate_vacancies(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    page = int(callback_query.data.split(':')[1])
    user_data = await state.get_data()
    city = user_data['city']
    profession = user_data['profession'].lower()
    salary = user_data['salary'].replace(' ', '')
    schedule = user_data['schedule']
    salary = int(salary) if salary.isdigit() else None
    city_id = get_city_id(city)

    if city_id and salary is not None:
        vacancies = search_vacancies(city_id, profession, schedule, salary, page=page, per_page=10)

        if vacancies:
            await send_vacancies_to_user(vacancies, callback_query.message, page)
        else:
            await callback_query.message.answer("Вакансий не найдено.")
    else:
        await callback_query.message.answer('Город не найден или зарплата неверного формата!')
        await state.clear()


@router.callback_query(F.data == 'get_info')
async def get_info(callback: CallbackQuery):
    await callback.message.edit_text('Спасибо!')
    user_id = callback.from_user.id
    add_user_ids(user_id)


@router.callback_query(F.data == 'skip_info')
async def skip_info(callback: CallbackQuery):
    await callback.message.edit_text('Спасибо!')


@router.message(WorkAI.process)
async def stop(message: Message):
    await message.answer('Пожалуйста, подождите немного, я не могу думать быстрее :)')


@router.message()
async def ai(message: Message, state: FSMContext):
    try:
        await state.set_state(WorkAI.process)
        res = await generator(message.text)
        await message.answer(res.choices[0].message.content)
        await state.clear()
    except Exception:
        await message.answer('Пожалуйста, обращайся ко мне только текстовыми сообщениями, я по-другому не умею :(')
        await state.clear()
