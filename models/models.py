from pydantic import BaseModel, confloat, conint
from typing import Optional
from pydantic.networks import EmailStr

class ProductModel(BaseModel):
    title: str
    description: str
    price: confloat(ge=0)
    count: conint(ge=0)

class SignUpModel(BaseModel):
    username: str
    email: Optional[EmailStr]
    password: str
