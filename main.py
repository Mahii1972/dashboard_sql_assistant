# main.py

from fastapi import FastAPI, Depends, Query
from dotenv import load_dotenv
from db.database import get_db_pool
from models.groq import get_chat_completion
from contextlib import asynccontextmanager
load_dotenv()  # Load environment variables from .env file

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await get_db_pool()
    yield
    app.state.pool.close()
    await app.state.pool.wait_closed()

app = FastAPI(lifespan=lifespan)

@app.get("/chat")
async def chat(user_input: str, pool=Depends(get_db_pool)):
    response = get_chat_completion(user_input)
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(response)
            result = await cur.fetchall()
    return {"response": result}

# @app.get("/{device_id}")
# async def read_item(device_id: str, pool=Depends(get_db_pool)):
#     async with pool.acquire() as conn:
#         async with conn.cursor() as cur:
#             await cur.execute("SELECT * FROM inventory2 WHERE `Device ID` = %s", (device_id,))
#             result = await cur.fetchone()
    
#     if result:
#         return result  # Return the entire result dictionary
#     return {"error": "Item not found"}