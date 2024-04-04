from pydantic import BaseModel


class ProductModel(BaseModel):
    title: str
    description: str
    price: float
    count: int
