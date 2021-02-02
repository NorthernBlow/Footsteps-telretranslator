from os import environ
from dotenv import load_dotenv

# Загрузка значений переменных окружения
load_dotenv()

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
