from contextlib import asynccontextmanager
from fastapi import FastAPI


from src.auth.router import router as auth_router


app = FastAPI(
    title='Terrea'
)

app.include_router(auth_router)

@app.get('/')
async def hello(name: str = 'World') -> dict:
    return {
        'message': f'Hello {name}'
    }