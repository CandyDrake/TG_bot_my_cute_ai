import asyncio

import requests
from aiogram import Bot

from keyboards.keyboards import create_page_buttons
from aiogram.types import Message
from database.requests import *

URL = 'https://api.hh.ru/'


def get_city_id(city_name: str) -> str:
    if not isinstance(city_name, str):
        raise ValueError("city_name должно быть строкой")

    url = f'{URL}areas'

    response = requests.get(url)
    if response.status_code == 200:
        areas = response.json()
        for country in areas:
            for region in country['areas']:
                if region['name'].lower() == city_name.lower():
                    return region['id']

                for city in region['areas']:
                    if city['name'].lower() == city_name.lower():
                        return city['id']

    return None


def get_city_id(city_name: str) -> str:
    if not isinstance(city_name, str):
        raise ValueError("city_name должно быть строкой")

    url = f'{URL}areas'

    response = requests.get(url)
    if response.status_code == 200:
        areas = response.json()
        for country in areas:
            for region in country['areas']:
                if region['name'].lower() == city_name.lower():
                    return region['id']

                for city in region['areas']:
                    if city['name'].lower() == city_name.lower():
                        return city['id']

    return None


def search_vacancies(city_id, profession, schedule, salary, page=1, per_page=10):
    url = f'{URL}vacancies'

    per_page = min(per_page, 100)
    if page > 2000 // per_page:
        page = 2000 // per_page

    params = {
        'text': profession,
        'area': city_id,
        'schedule': schedule,
        'salary': salary,
        'per_page': per_page,
        'page': page
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


async def send_vacancies_to_user(vacancies, message: Message, current_page):
    for vacancy in vacancies['items']:
        vacancy_name = vacancy['name']
        salary = vacancy['salary']
        schedule = vacancy['schedule']
        if salary:
            salary_text = f'{salary["from"] or ""}-{salary["to"] or ""} {salary["currency"]}'
        else:
            salary_text = 'Зарплата не указана'
        vacancy_url = vacancy["alternate_url"]
        await message.answer(f'Вакансия: {vacancy_name}\nЗарплата: {salary_text}\nЗанятость: {schedule["name"]}\n'
                             f'Ссылка на вакансию: {vacancy_url}')

    total_pages = vacancies.get('pages', 0)
    if total_pages > 0:
        vacancy_buttons = create_page_buttons(current_page, total_pages)
        await message.answer('Выберите страницу', reply_markup=vacancy_buttons)
    else:
        await message.answer('Нет доступных страниц')


async def send_vacancies_for_subscribe(bot: Bot, vacancies, user_id):
    for vacancy in vacancies['items']:
        vacancy_name = vacancy['name']

        salary_text = f"{vacancy['salary']['from']} - {vacancy['salary']['to']} {vacancy['salary']['currency']}" \
            if vacancy['salary'] and vacancy['salary']['from'] is not None and vacancy['salary'][
            'to'] is not None else "Не указана"

        schedule = vacancy['schedule']

        await bot.send_message(user_id,
                               f'Вакансия: {vacancy_name}\n'
                               f'Зарплата: {salary_text}\n'
                               f'Занятость: {schedule["name"]}\n'
                               f'Ссылка: {vacancy["alternate_url"]}')


async def check_and_send(bot: Bot):
    while True:
        current_time = datetime.now().strftime('%H:%M')
        subscribers = await get_all_subscribers()

        for subscriber in subscribers:
            user_id = subscriber['tg_id']
            selected_time = subscriber['subscribe']

            if selected_time == current_time:
                user_data = await get_user_data(user_id)
                if user_data and user_data.queries:
                    last_query = await put_last_query(user_data.queries)
                    if last_query:
                        city, profession, schedule, salary = last_query
                        city_id = get_city_id(city)

                        if city_id:
                            vacancies = search_vacancies(city_id, profession, schedule, salary, page=1, per_page=10)

                            if 'items' in vacancies and isinstance(vacancies['items'], list):
                                await send_vacancies_for_subscribe(bot, vacancies, user_id)
                            else:
                                await bot.send_message(user_id, 'Ошибка при получении вакансий.')
                        else:
                            await bot.send_message(user_id, 'Город не найден')
        await asyncio.sleep(60)
