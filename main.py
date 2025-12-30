import uvicorn

"""
tells uvicorn to run the api called app where src.app=app.py, src.app.app = app = FastAPI() in the src/app file on localhost. reload tells server to reload on changes saved
>>uv run .\main.py  #run in terminal with this command
visit url http://localhost:8000/docs or http://127.0.0.1:8000/docs only to test. /doc or /redoc
"""

#entry point of the app. click on the run button while on this page or use 'uv run .\main.py' command in terminal
if __name__ == "__main__":
    uvicorn.run(app="src.app:app", host="0.0.0.0", port=8000, reload=True)