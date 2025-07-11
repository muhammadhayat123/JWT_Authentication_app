from fastapi import FastAPI
from dotenv import load_dotenv
from routes.todo_route import todo_router
from routes.user_route import user_router



load_dotenv()

app = FastAPI()

app.include_router(todo_router, prefix="/todo", tags=["todo"]) 
app.include_router(user_router, prefix="/user", tags=["user"])  







    