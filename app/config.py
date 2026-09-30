import os

from dotenv import load_dotenv

load_dotenv()


# Настройки безопасности и JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = 'HS256'
REFRESH_TOKEN_EXPIRE_DAYS = 7
SECRET_KEY = os.getenv('SECRET_KEY')

# База данных
DATABASE_URL = os.getenv('DATABASE_URL')

# Администратор по умолчанию
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@myshop.com')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
