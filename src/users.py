from fastapi import FastAPI, HTTPException

app = FastAPI()

users = {1: {"firstName":"Jack", "lastName":"Daniels", "Email":"jDaniel@gmail.com" }, 2: {"firstName":"Ben", "lastName":"Thomas", "Email":"benThomas@gmail.com" }}

@app.get("/hello-world")
async def helloWorld():
    return {"message": "hello world"}

@app.get("/users")
async def getUsers():
    return users

@app.get("/users/{id}")
async def getUser(id: int):
    if id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    return users.get(id)

