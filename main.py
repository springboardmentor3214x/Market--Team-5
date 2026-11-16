import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator
from stock_data import get_historical_stock_data

app = FastAPI(
    title="AI-powered multi-agent stock market analysis and research",
    description="Backend API for AI-powered multi-agent stock market analysis and research",
    version="1.0.0"
)


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


@app.get("/")
def home():
    return {
        "message": "Welcome to AI-Powered Stock Research System!"
    }


@app.post("/register", status_code=201)
def register_user(user: RegisterRequest):

    if user.password != user.confirmPassword:
        raise HTTPException(
            status_code=400,
            detail="Password and Confirm Password do not match"
        )

    return {
        "message": "Registration successful!",
        "username": user.username,
        "email": user.email
    }

@app.get("/historical/{ticker}")
def historical_stock_data(
    ticker: str,
    period: str = "1mo"
):
    allowed_periods = ["1mo", "3mo", "6mo", "1y", "2y", "5y"]

    if period not in allowed_periods:
        raise HTTPException(
            status_code=400,
            detail="Invalid period. Choose 1mo, 3mo, 6mo, 1y, 2y or 5y."
        )

    try:
        data = get_historical_stock_data(ticker, period)

        if data is None or data.empty:
            raise HTTPException(
                status_code=404,
                detail="No historical stock data found."
            )

        records = json.loads(data.to_json(orient="records"))

        return {
            "ticker": ticker,
            "period": period,
            "total_records": len(records),
            "data": records
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve stock data: {str(e)}"
        )