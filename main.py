from fastapi import FastAPI

app = FastAPI(
    name="Birdvision Submission",
    description="Product apis to manage products",
    version="1.0.0",
)


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/products")
def get_products():
    return {"Api to get all products"}


@app.get("/products/{id}")
def get_products_by_id():
    return {"Api to get product of an id"}


@app.post("/products")
def create_product():
    return {"Api to create a product"}


@app.put("/products/{id}")
def update_product():
    return {"Api to update product of an id"}


@app.delete("/products/{id}")
def delete_product():
    return {"Api to delete product of an id"}


@app.delete("/products")
def delete_all_products():
    return {"Api to delete all products"}
