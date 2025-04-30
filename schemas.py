from pydantic import BaseModel, Field, validator
import re


class RegisterRequest(BaseModel):
    telegram_id: int
    full_name: str
    phone: str


class VerifyRequest(BaseModel):
    code: str



class ResponseMessage(BaseModel):
    message: str


class UserResponse(BaseModel):
    id: int
    telegram_id: int
    phone_number: str
    is_verified: bool

    class Config:
        orm_mode = True