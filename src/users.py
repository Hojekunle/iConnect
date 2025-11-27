from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/users", tags=["users"])

users = {1: {"firstName":"Jack", "lastName":"Daniels", "Email":"jDaniel@gmail.com" }, 2: {"firstName":"Ben", "lastName":"Thomas", "Email":"benThomas@gmail.com" }}

"""
@router.get("/hello-world")
async def helloWorld():
    return {"message": "hello world"}
"""

@router.get("")
async def getUsers():
    return users

@router.get("/{id}")
async def getUser(id: int):
    if id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    return users.get(id)

