import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import BaseModel
from typing import List, Optional

class PostCreate(BaseModel):
    userId: str
    title: str
    comment: str
    timeMade: datetime
    timeEdited: Optional[datetime] = None
    likes: int
    shares: int
    tags: List[str]


class PostResponse(BaseModel):
    postId: int
    userId: str
    title: str
    comment: str
    timeMade: datetime
    timeEdited: Optional[datetime] = None
    likes: int
    shares: int
    tags: List[str]

class PostUpdate(BaseModel):
    postId: int
    userId: str
    title: str
    comment: str
    timeMade: datetime
    timeEdited: Optional[datetime] = None
    likes: int
    shares: int
    tags: List[str]

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserCreate):
    pass
