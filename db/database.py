# database.py

import os
import aiomysql

# Database connection configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'db': os.environ.get('DB_NAME'),
    'charset': 'utf8mb4',
    'cursorclass': aiomysql.DictCursor,
}

async def get_db_pool():
    return await aiomysql.create_pool(**DB_CONFIG)