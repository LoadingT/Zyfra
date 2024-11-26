from fastapi import FastAPI, Depends, HTTPException, status
from uuid import uuid4
import redis.asyncio as redis

# redis клиент
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Конфигурация сессий
SESSION_EXPIRE_SECONDS = 3600  # Время жизни сессии (1 час)
COOKIE_NAME = "session_id"
SESSION_PREFIX = "session"


# при таком подходе сессию можно украсть, нужно дополнительно хранить информацию о устройстве пользователя
async def create_session(username: str) -> str:
    session_id = str(uuid4())  # Генерируем уникальный идентификатор
    await redis_client.setex(f"{SESSION_PREFIX}:{session_id}", SESSION_EXPIRE_SECONDS,
                             username)  # Сохраняем сессию в Redis
    return session_id


async def delete_current_session(session_id: str):
    await redis_client.delete(f"{SESSION_PREFIX}:{session_id}")  # Удаляем сессию из Redis


async def get_current_user_via_session_id(session_id: str) -> str:
    return await redis_client.get(f"{SESSION_PREFIX}:{session_id}")
