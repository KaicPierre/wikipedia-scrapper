from fastapi import FastAPI

from app.router.router import router

app = FastAPI(
    title='Summarization API',
    docs_url='/docs',
)

app.include_router(router)
