from datetime import datetime
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

