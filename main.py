from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.products import models, schemas
from infra.database import db

models.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

def get_db():
    db = db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
