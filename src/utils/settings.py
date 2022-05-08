import os

CURRENT_YEAR = os.getenv('CURRENT_YEAR', 2022)
CURRENT_PERIOD = os.getenv('CURRENT_PERIOD', 1)

MONGO_USER = os.getenv('MONGO_USER', 'root')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'root')
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
