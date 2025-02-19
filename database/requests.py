import datetime
from datetime import datetime
from database.models import async_session
from database.models import User
from sqlalchemy import select


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper


@connection
async def set_user(session, tg_id: int):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
        return None
    else:
        return user


@connection
async def update_user(session, tg_id: int, name, contact):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if user:
        user.name = name
        user.phone_number = contact
        await session.commit()
        return user
    else:
        return None


@connection
async def update_subscribe(session, tg_id: int, subscribe: str):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if user:
        user.subscribe = subscribe
        await session.commit()
        return user
    else:
        return None


@connection
async def get_user_data(session, tg_id: int):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if user:
        return user
    else:
        return None


@connection
async def update_query(session, tg_id: int, query: str):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if user:
        if user.queries:
            user.queries += f', {query}'
        else:
            user.queries = f'{query}'
        await session.commit()
        return user
    else:
        return None


@connection
async def update_timestamp(session, tg_id: int):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if user:
        if user.timestamp:
            user.timestamp += f', {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}'
        else:
            user.timestamp = f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}'
        await session.commit()
        return user
    else:
        return None


async def merged_queries(datetime_str: str, query_str: str):
    timelist = [t.strip() for t in datetime_str.split(',')]
    querylist = [q.strip().split(':') for q in query_str.split(',')]
    query_info = sorted(zip(timelist, querylist), key=lambda x: x[0], reverse=True)
    result = ''
    for stamp, query in query_info:
        city, profession, schedule, salary = query
        salary = salary + ' руб'
        result += f'{stamp} - {city},  {profession}, {schedule}, {salary}\n'
    return result


async def put_last_query(query_str: str):
    querylist = [q.strip().split(':') for q in query_str.split(',')]
    if querylist:
        return querylist[0]
    return None


@connection
async def get_all_subscribers(session):
    res = await session.execute(select(User).where(User.subscribe != ''))
    users = res.scalars().all()
    subscribers = [{'tg_id': user.tg_id, 'subscribe': user.subscribe} for user in users]
    return subscribers
