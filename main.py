from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app=FastAPI()
models.Base.metadata.create_all(bind=engine)
class PostBase(BaseModel):
    title:str
    content: str
    user_id: int
class UserBase(BaseModel):
    username:str
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Depends(get_db)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}
@app.get("/users/")
async def read_users(db: Session = db_dependency):
    users = db.query(models.User).all()
    return users
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_data: UserBase, db: Session = db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Update user fields with the provided data
    user.username = user_data.username
    
    db.commit()
    db.refresh(user)
    return user
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    # Check if the user already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    # Create a new user
    db_user = models.User(username=user.username)  # You should hash the password in a real-world scenario
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
