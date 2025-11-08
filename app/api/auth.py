from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.models.user import User
from fastapi import Depends
from pydantic import BaseModel
import bcrypt

router = APIRouter(prefix="/auth", tags=["Auth"])

class RegisterUser(BaseModel):
    fullName: str
    email: str
    password: str

@router.post("/register")
def register_user(data: RegisterUser, db: Session = Depends(get_db)):

    # Verificar si el email ya existe
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe con ese email")

    # Encriptar contraseña
    hashed = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Crear usuario
    new_user = User(
        fullName=data.fullName,
        email=data.email,
        password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "fullName": new_user.fullName
    }

from app.core.security import create_token

class LoginUser(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginUser, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuario no existe")

    # Verificar contraseña
    if not bcrypt.checkpw(data.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = create_token(user.id)

    return {
        "token": token,
        "user_id": user.id,
        "email": user.email
    }
