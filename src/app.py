from fastapi import FastAPI
from src.users import router as users_router
from src.user_posts import router as posts_router

app = FastAPI(
    title="iConnect API",
    version="1.0.0"
)

# REGISTER ROUTERS
app.include_router(users_router)
app.include_router(posts_router)