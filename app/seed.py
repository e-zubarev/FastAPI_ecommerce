from sqlalchemy import select

from app.config import ADMIN_EMAIL, ADMIN_PASSWORD
from app.database import async_session_maker
from app.models import User
from app.security import hash_password


async def create_first_admin():
    """
    Создать администратора при запуске сервера, если его еще нет в БД
    """
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        print('Admin email or password not set. Admin creation skipped.')

    async with async_session_maker() as db:
        admin = await db.scalar(select(User).where(User.email == ADMIN_EMAIL))
        if admin is None:
            print(f'Creating admin with email: {ADMIN_EMAIL}...')

            admin = User(
                email=ADMIN_EMAIL,
                hashed_password=hash_password(ADMIN_PASSWORD),
                role='admin',
                is_active=True
            )
            db.add(admin)
            await db.commit()
            print('Admin created successfully!')
        else:
            print('Admin user already exists in the database.')
