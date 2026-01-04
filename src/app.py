from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from src.db import Post, create_db_and_tables, get_async_session, User
from src.schemas import PostCreate, PostResponse, PostUpdate, UserCreate, UserRead, UserUpdate
from src.db import Post, create_db_and_tables, get_async_session
from sqlalchemy import select
from src.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import os
import shutil
import tempfile
import uuid
from src.users import auth_backend, fastapi_users, current_active_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(
    lifespan=lifespan, #makes the call to create the db every time app starts
    title="iConnect API",
    version="1.0.0"
)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=["auth"]) #include all auth endpoints provided by Fastapi_users project (library) - login, logout
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix='/auth', tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix='/auth', tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix='/auth', tags=["auth"])

#create user with the fastapi_users' register endpoint and login using Authorize button from localhost:8080/docs. A token/clientSecret is generated after signin and included in subsequent requests
app.include_router(fastapi_users.get_users_router(UserRead, UserCreate), prefix='/users', tags=["users"])

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(current_active_user), #enforces authenticated request. current_active_user only has a value if authenticated
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session) #dependency injection
):
    
    temp_file_path = None

    #store the image uploade from the frontend into a temfile, upload the tempfile into imagekit, get image_url from imagekit and save in db
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file: #suffix gets the file extension
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file) #copy the uploaded file into the temp_file

        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"), #upload to imagekit, rb- read-byte
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )

        if upload_result.response_metadata.http_status_code == 200:
            post = Post(
                user_id=user.id,
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name
            )

            session.add(post)
            await session.commit()
            await session.refresh(post) #adds a value for the auto-generated id and created_at fields
            return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close() #clean up the file object

    

@app.router.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user), #enforces authenticated request. current_active_user only has a value if authenticated
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc())) #queries db. search sqlalchemy fastapi online to see other methods
    posts = [row[0] for row in result.all()] #result is a cursor object and we convert it to list

    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    user_dict = {u.id: u.email for u in users} #create a dictionary of userID and their email

    post_data = []
    for post in posts:
        post_data.append(
            {
                "id": str(post.id),
                "user_id": post.user_id,
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "createdAt": post.created_at.isoformat(),
                "is_Owner": post.user_id == user.id,
                #"email": post.user.email,
                "email": user_dict.get(post.user_id, "Unknown"),
            }
        )

    return {"posts": post_data}

@app.router.delete("/post/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    try:
        post_uuid = uuid.UUID(post_id) #generates random id

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first() #Extracts only the model objects, not full rows i.e Post(...) not (Row(Post(...)),)

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.user_id != user.id:
            raise HTTPException(status_code=404, detail="You dont have permission to delete this post")

        await session.delete(post)
        await session.commit()

        return {"success":True, "message":"Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

