
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, field_validator
import json
from pathlib import Path
import os

from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from database import get_db
from models import User

from routers.company import router as company_router

from dotenv import load_dotenv

load_dotenv()
# PASSWORD HASHING

password_hash = PasswordHash.recommended()


def hash_password(plain_password: str) -> str:
    hashed_password = password_hash.hash(plain_password)
    return hashed_password


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password
    )


# FASTAPI APPLICATION

app = FastAPI(
    title="AI-Powered Stock Research System",
    description="Backend API for AI-powered multi-agent stock market analysis and research",
    version="1.0.0"
)


# CORS CONFIGURATION

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# COMPANY SEARCH ROUTER

app.include_router(company_router)


# HOME API

@app.get("/")
def home():
    return {
        "message": "Welcome to AI-Powered Stock Research System!"
    }


class RegisterRequest(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    confirmPassword: str = Field(min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if not value.strip():
            raise ValueError("Username cannot be empty")
        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain an uppercase letter")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain a number")

        return value


# LOGIN REQUEST MODEL

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


# REGISTRATION API

@app.post("/register", status_code=201)
def register_user(
    user: RegisterRequest,
    db: Session = Depends(get_db)
):

    if user.password != user.confirmPassword:
        raise HTTPException(
            status_code=400,
            detail="Password and Confirm Password do not match"
        )

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Registration successful!",
        "username": user.username,
        "email": user.email
    }


# LOGIN API

@app.post("/login")
def login_user(
    user: LoginRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    is_password_correct = verify_password(
        user.password,
        existing_user.hashed_password
    )

    if not is_password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    return {
        "message": "Login successful!",
        "username": existing_user.username,
        "email": existing_user.email
    }
