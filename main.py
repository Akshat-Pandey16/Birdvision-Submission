from fastapi import FastAPI
from models.db import create_database
from routes import auth
from routes import product

app = FastAPI(
    title="Birdvision Submission",
    description="Product APIs to manage products",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    create_database()


app.include_router(auth.router)
app.include_router(product.router)


@app.get("/")
def index():
    """Root endpoint"""
    return {"message": "Go to /docs to view the APIs documentation."}
