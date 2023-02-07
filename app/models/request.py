from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ProductRequest(BaseModel):
    name: str = Field(None, title="Product Name", max_length=5000)
    price: float = Field(..., gt=0, description="Price of product")
    is_available: bool = Field(False, description="Value must be either True or False")
    seller_email: EmailStr = Field(None, title="Seller Email")
    created_by: int = Field(None, title="User id")


class ProductUpdatedRequest(BaseModel):
    product_id: int = Field(None, title="Product ID")
    name: str = Field(None, title="Product Name", max_length=5000)
    price: float = Field(..., gt=0, description="Price of product")
    is_available: bool = Field(False, description="Value must be either True or False")
    seller_email: EmailStr = Field(None, title="Seller Email")
    updated_by: int = Field(None, title="User id")
    