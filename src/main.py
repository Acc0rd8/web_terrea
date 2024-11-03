from contextlib import asynccontextmanager
from fastapi import FastAPI


from src.database import create_db_and_tables


app = FastAPI(
    title='Terrea'
)
    
@app.get('/')
async def hello(name: str = 'World') -> dict:
    return {
        'message': f'Hello {name}'
    }