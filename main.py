from fastapi import FastAPI
from routers.mangadex_router import router as mangadex_router

app = FastAPI(title="MangaDex Proxy API")


# include router
app.include_router(mangadex_router)
