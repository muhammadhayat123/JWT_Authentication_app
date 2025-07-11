from fastapi import APIRouter
from config.db import get_db
from models.todo_model import Todo
from validations.validation import TodoCreate
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from utils.util_helper import verify_token



todo_router = APIRouter()


@todo_router.post("/create")
def create_todo(todo: TodoCreate, user = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        # user = verify_token(todo.token)
        # print("Token from user:", user)
        # if  not user:
        #     raise HTTPException(status_code=401, detail="Invalid token")
        user_id = user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        new_todo = Todo(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            user_id=user_id
        )
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)

        return {
            "data": new_todo,
            "message": "Todo created successfully",
            "status": "success"
        }

    except Exception as e:
        print("An error occurred:", e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }
    

# Get all todos
@todo_router.get("/")
def read_todo(db: Session = Depends(get_db)):
    try: 
        todos =  db.query(Todo).all()
        return{
            "data": todos,
            "message": "Todos retrieved successfully",
            "status": "success"
        }
    except Exception as e:
        print("An error occurred:", e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }
    

# Get todos by id
@todo_router.get("/{todo_id}")
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {
            "data": todo,
            "message": "Todo retrieved successfully",
            "status": "success"
        }
    except Exception as e:
        print("An error occurred:", e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }
     

# Update an existing todo
@todo_router.put("/{todo_id}")
def update_todo(todo_id: int, todo_update: TodoCreate, db: Session = Depends(get_db)):
    try:
        user = verify_token(todo_update.token)
        if  not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        # Update fields from the request body
        todo.title = todo_update.title
        todo.description = todo_update.description
        todo.completed = todo_update.completed
        
        db.commit()
        db.refresh(todo)
        return {
            "data": todo,
            "message": "Todo updated successfully",
            "status": "success"
        }
    except Exception as e:
        print("An error occurred:", e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }

# Delete a todo
@todo_router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        db.delete(todo)
        db.commit()

        return {
            "data": None,
            "message": "Todo deleted successfully",
            "status": "success"
        }
    except Exception as e:
        print("An error occurred:", e)
        return {
            "message": str(e),
            "status": "error",
            "data": None    
    }


