from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer     
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))  # ✅ Convert to int

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        to_encode = data.copy()

        # ✅ Use custom expiration or default from env
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print("An error occurred:", e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded_token:
            return decoded_token
        else:
            return None
    except Exception as e:
        print("An error occurred:", e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }
    


        

