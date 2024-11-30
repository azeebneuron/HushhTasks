# schemas.py
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import List, Optional

class OrderBase(BaseModel):
    product_name: str
    quantity: conint(gt=0)  # Ensures quantity > 0

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    user_id: int
    order_date: datetime
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class User(UserBase):
    id: int
    created_at: datetime
    orders: List[Order] = []
    
    class Config:
        from_attributes = True