from pydantic import BaseModel


# Pydantic models
class TodoCreate(BaseModel):
    title: str
    description: str
    completed: bool = False
    # token: str



class LoginUser(BaseModel):
    email: str
    password: str


# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: str
    password: str 

