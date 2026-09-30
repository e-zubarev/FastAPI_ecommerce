from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import routers
from app.seed import create_first_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    При старте приложения создает администратора, если его еще нет в БД
    """
    await create_first_admin()
    yield


app = FastAPI(
    title='Интернет магазин на FastAPI',
    version='0.1.0',
    lifespan=lifespan
)

app.include_router(routers.categories)
app.include_router(routers.products)
app.include_router(routers.users)
app.include_router(routers.reviews)


@app.get('/')
async def root() -> dict:
    """
    Корневой маршрут для проверки работы API
    """
    return {'message': 'Добро пожаловать в API интернет-магазина!'}
