from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from config.db import get_db
from models.todo_model import User
from validations.validation import UserCreate, LoginUser
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.util_helper import create_access_token

user_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)


@user_router.post("/register")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_hash_password = hash_password(user.password)
        print(user_hash_password)
        new_user = User(
        name=user.name, 
        email=user.email,
        password=user_hash_password
    )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db_user= db.query(User).filter(User.email == new_user.email).first()
        token = create_access_token(data={"email": new_user.email, "name": new_user.name, "user_id": db_user.id})
        return {
            "data": {
                "name": new_user.name,
                "email": new_user.email,
                "token": token
            },
            "message": "User created successfully",
            "status": "success"
        }
    except Exception as e:
        print("An error occurred:", e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }
    

@user_router.post("/login")
def login_user(user: LoginUser, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        is_valid_password = verify_password(user.password, db_user.password)
        if is_valid_password == False:
            raise HTTPException(status_code=401, detail="Invalid password")
        #token is required on user want to registered also with the login 
        token = create_access_token(data={"email": db_user.email, "name": db_user.name, "user_id": db_user.id})
        user_data = {
            "name": db_user.name,
            "email": db_user.email, 
            "token": token
              }
        return {
            "data": user_data,
            "message": "User logged in successfully",
            "status": "success"
        }
    except Exception as e:
        print("An error occurred:", e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }
