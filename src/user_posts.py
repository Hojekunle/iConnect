from fastapi import APIRouter, HTTPException
from src.schemas import PostCreate, PostResponse, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])

#post is a python dictionary not list
posts = {
    1:{
    "postId": 1,
    "userId": "u102",
    "title": "Morning Motivation",
    "comment": "Starting the day with gratitude!",
    "timeMade": "2025-11-16T08:12:45Z",
    "timeEdited": None,
    "likes": 34,
    "shares": 2,
    "tags": ["motivation", "morning"]
  },
  2:{
    "postId": 2,
    "userId": "u212",
    "title": "New Coding Project",
    "comment": "Just started learning FastAPI. Loving it so far!",
    "timeMade": "2025-11-16T08:20:10Z",
    "timeEdited": "2025-11-16T08:23:55Z",
    "likes": 18,
    "shares": 1,
    "tags": ["coding", "python", "fastapi"]
  },
  3:{
    "postId": 3,
    "userId": "u045",
    "title": "Coffee Time",
    "comment": "Nothing like a hot latte on a cold morning.",
    "timeMade": "2025-11-16T08:27:50Z",
    "timeEdited": None,
    "likes": 22,
    "shares": 0,
    "tags": ["coffee", "morning"]
  },
  4:{
    "postId": 4,
    "userId": "u300",
    "title": "Gym Day",
    "comment": "Back to leg day. Pray for me 😩",
    "timeMade": "2025-11-16T08:35:42Z",
    "timeEdited": None,
    "likes": 67,
    "shares": 4,
    "tags": ["fitness", "gym"]
  }
}

@router.get("")
async def getPosts(limit: int = None) -> list[PostResponse]:
    if limit:
        return list(posts.values())[:limit]

    return list(posts.values())

@router.get("/{id}")
async def getPost(id: int) -> PostResponse:
    if id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")

    return posts.get(id)

@router.post("")
async def createPost(post: PostCreate) -> PostResponse:
  new_id = max(posts.keys()) + 1 if posts else 1
  new_post = {
        "postId": new_id,
        "userId": post.userId,
        "title": post.title,
        "comment": post.comment,
        "timeMade": post.timeMade,
        "timeEdited": post.timeEdited,
        "likes": post.likes,
        "shares": post.shares,
        "tags": post.tags
    }
  posts[new_id] = new_post
  return new_post

@router.delete("/{id}")
async def delete_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    
    deleted_post = posts.pop(post_id)
    return {"message": f"Post {post_id} deleted successfully", "post": deleted_post}

@router.put("/{id}")
async def update_post(post_id: int, post_update: PostUpdate):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    
    # Update only the fields that were provided
    for key, value in post_update.dict(exclude_unset=True).items():
        posts[post_id][key] = value
    
    return {"message": f"Post {post_id} updated successfully", "post": posts[post_id]}

