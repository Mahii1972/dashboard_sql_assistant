# main.py

from typing import Union
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from db.database import get_db_pool

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.pool = await get_db_pool()

@app.on_event("shutdown")
async def shutdown():
    app.state.pool.close()
    await app.state.pool.wait_closed()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/{device_id}")
async def read_item(device_id: str, pool=Depends(get_db_pool)):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM inventory2 WHERE `Device ID` = %s", (device_id,))
            result = await cur.fetchone()
    
    if result:
        return result  # Return the entire result dictionary
    return {"error": "Item not found"}