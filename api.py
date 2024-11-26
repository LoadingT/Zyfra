from functools import wraps

from fastapi import FastAPI, HTTPException, Response, Request, Depends

from relacion_db import *
from redis_client import *

app = FastAPI()


async def valid_session(request: Request, response: Response) -> bool:
    session_id = request.cookies.get(COOKIE_NAME)  # Получаем session_id из cookies
    if session_id:
        username = await get_current_user_via_session_id(session_id)  # Проверяем сессию
        if username:
            # Если сессия валидна, вызываем основную функцию
            return True
    return False


def check_session(func):
    @wraps(func)  # Сохраняем оригинальные метаданные функции
    async def wrapper(request: Request, response: Response, *args, **kwargs):
        if valid_session(request, response):
            return await func(request, response, *args, **kwargs)

        # Если сессия не найдена или не валидна, возвращаем ошибку
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    return wrapper


# Маршрут создания сесссии
@app.post("/login")
async def login(request: Request, response: Response):
    if valid_session(request, response):
        return {'message': f'Hello!'}

    username, password = request.get('username'), request.get('password')

    if username and password:
        if user_exists(username, password):
            session_id = await create_session(username)
            if session_id:
                response.set_cookie(COOKIE_NAME, session_id)
                return {"message": f"Welcome, {username}, session created!"}
        else:
            return {"message": "not registered"}

    return {"message": f"bad request"}


@app.post("/logout")
@check_session
async def logout(request: Request, response: Response):
    session_id = request.get(COOKIE_NAME)
    await delete_current_session(session_id)
    response.delete_cookie(COOKIE_NAME)
    return {'message': 'logout!'}


@app.post("/do_something")
@check_session
async def do_something():
    print('Abrakadabra')
