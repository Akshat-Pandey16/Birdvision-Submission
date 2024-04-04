from pydantic import BaseModel, confloat, conint


class ProductModel(BaseModel):
    title: str
    description: str
    price: confloat(ge=0)
    count: conint(ge=0)
