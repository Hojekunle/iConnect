from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from src.db import Post, create_db_and_tables, get_async_session
from src.schemas import PostCreate, PostResponse, PostUpdate
from src.db import Post, create_db_and_tables, get_async_session
from sqlalchemy import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(
    lifespan=lifespan, #makes the call to create the db every time app starts
    title="iConnect API",
    version="1.0.0"
)


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session) #dependency injection
):
    post = Post(
        caption = caption,
        url = "dummy Url",
        file_type = "photo",
        file_name = "dummy name"
    )

    session.add(post)
    await session.commit()
    await session.refresh(post) #adds a value for the auto-generated id and created_at fields
    return post

@app.router.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc())) #search sqlalchemy fastapi online to see other methods
    posts = [row[0] for row in result.all()] #result is a cursor object and we convert it to list

    post_data = []
    for post in posts:
        post_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "createdAt": post.created_at.isoformat()
            }
        )

    return {"posts": post_data}


